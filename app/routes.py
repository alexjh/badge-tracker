from flask import render_template, flash, redirect, url_for, request
from sqlalchemy.sql.expression import or_
from app import app, db
from app.forms import LoginForm, SkillRecordForm
from app.models import User, Group, Youth
from app.models import Skill, Badge, SkillRecord
from app.models import BadgeState, BadgeProgress


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Alex"}
    return render_template("index.html", title="Home", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            "Login requested for user {}, remember_me={}".format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", title="Users", users=users)


@app.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", title=user.username, user=user)


@app.route("/groups")
def groups():
    groups = Group.query.all()
    return render_template("groups.html", title="Groups", groups=groups)


@app.route("/group/<group_id>")
def group(group_id):
    group = Group.query.filter_by(id=group_id).first_or_404()
    return render_template("group.html", title=group.name, group=group)


@app.route("/youth")
def youth():
    youth = Youth.query.all()
    return render_template("youth.html", title="Youth", youth=youth)


@app.route("/skills")
def skills():
    badges = Badge.query.all()
    return render_template("skills.html", title="Skills", badges=badges)


@app.route("/badges")
def badges():
    badges = Badge.query.all()
    return render_template("badges.html", title="Badges", badges=badges)


@app.route("/badge_progress")
def badge_progress():
    progress = BadgeProgress.query.all()
    return render_template(
        "badge_progress.html", title="Badge Progress", progress=progress
    )


@app.route("/badge/<badge_id>")
def badge(badge_id):
    badge = Badge.query.filter_by(id=badge_id).first_or_404()
    return render_template("badge.html", title="Badge", badge=badge)


@app.route("/skill/<skill_id>")
def skill(skill_id):
    skill = Skill.query.filter_by(id=skill_id).first_or_404()
    return render_template("skill.html", title="Skill", skill=skill)


@app.route("/skill_records")
def skill_records():
    skill_records = SkillRecord.query.all()
    return render_template(
        "skill_records.html", title="Skill Records", skill_records=skill_records
    )


@app.route("/skill_record/<record_id>")
def skill_record(record_id):
    skill_record = SkillRecord.query.filter_by(id=record_id).first_or_404()
    return render_template(
        "skill_record.html", title="Skill Record", skill_record=skill_record
    )


def get_participants(form):
    # TODO filter youth that already have the skill
    return Youth.query.filter(or_(Youth.id == v for v in form.participants.data)).all()


def get_skills(form):
    return Skill.query.filter(or_(Skill.id == v for v in form.skills.data)).all()


def get_youth_without_skill(youth, skill):
    filtered_youth = []

    for y in youth:
        for r in y.skill_records:
            if r.skill == skill:
                print(f"{skill} already exists for {y}")
                break
        else:
            print(f"{y} doesn't have {skill} yet")
            filtered_youth.append(y)

    return filtered_youth


def check_youth_badges(youth, badges):
    youth_skills = {record.skill for record in youth.skill_records}

    for badge in badges:
        badge_skills = {requirement.skill for requirement in badge.requirements}
        if badge_skills.issubset(youth_skills):
            youth_badges = [
                badgeprogress.badge for badgeprogress in youth.badgeprogress
            ]
            if badge not in youth_badges:
                print(f"{badge} achieved!")
                progress = BadgeProgress(
                    badge_state=BadgeState.ACHIEVED, badge=badge, youth=youth
                )
                db.session.add(progress)
            else:
                print(f"{badge} already achieved")
    db.session.commit()


def check_badges(youth):
    badges = Badge.query.all()
    for y in youth:
        check_youth_badges(y, badges)


@app.route("/record_skill", methods=["GET", "POST"])
def record_skill():
    form = SkillRecordForm()

    if form.validate_on_submit():
        all_youth = get_participants(form)
        skills = get_skills(form)
        updated_youth = set()
        for skill in skills:
            youth = get_youth_without_skill(all_youth, skill)
            if len(youth):
                leader = User.query.filter_by(username=form.leader.data).first()
                print(f"{leader} adding {youth} for {skill} on {form.date.data}")
                record = SkillRecord(
                    notes=form.notes.data,
                    scouter=leader,
                    skill=skill,
                    youth=youth,
                    timestamp=form.date.data,
                )
                db.session.add(record)

                updated_youth.update(youth)
            else:
                print(f"No one to add for {skill}")
        db.session.commit()

        check_badges(updated_youth)

        flash("Your changes have been saved.")
        return redirect(url_for("skill_records"))

    return render_template("record_skill.html", title="Add Skill Record", form=form)


def get_next_badges(youth):
    # Returns a dict of {badge: (earned, total)} for the next level of badge
    # that hasn't been achieved yet.
    badges = Badge.query.order_by(Badge.description, Badge.level).all()
    youth_badges = [progress.badge for progress in youth.badgeprogress]
    youth_skills = {record.skill for record in youth.skill_records}

    # Add badge to next_badges only if there isn't already a lower level of
    # this already added
    next_badges = {}

    for badge in badges:
        if badge in youth_badges:
            continue

        descriptions = [badge.description for badge in next_badges.keys()]

        if badge.description in descriptions:
            continue

        skills = {requirement.skill for requirement in badge.requirements}
        earned_skills = skills.intersection(youth_skills)
        next_badges[badge] = (len(earned_skills), len(skills))

    return next_badges


def check_for_missing_badges(earned_skills, badges):
    warnings = []

    all_badges = Badge.query.all()

    # Check unearned badges
    for badge in set(all_badges).difference(badges):
        skills = {r.skill for r in badge.requirements}

        if set(earned_skills).issuperset(skills):
            warnings.append(
                f"Skills completed for {badge.description} {badge.level} but badge isn't earned"
            )

    return warnings


def check_for_unearned_badges(skills, badges):
    warnings = []

    # For each badge
    #   Get its skill list
    #   Compare with the earned skills
    #   Add a warning for every extra skill in the badge list

    for badge in badges:
        badge_skills = {r.skill for r in badge.requirements}

        for skill in badge_skills.intersection(set(skills)):
            warnings.append(
                f"{badge.description} {badge.level} completed but {skill} isn't earned"
            )
    return warnings


def check_for_skipped_badges(badges):
    warnings = []

    earned = {}

    for badge in badges:
        if badge.description in earned.keys():
            earned[badge.description].append(badge.level)
        else:
            earned[badge.description] = [badge.level]

    # Earned higher level badge without lower level
    for badge, levels in earned.items():
        if len(levels) != sorted(levels)[-1]:
            # TODO more details about missing level
            warnings.append(f"{badge} has not earned all prior levels")

    return warnings


def validate_badge_information(youth):
    youth_skills = {record.skill for record in youth.skill_records}
    youth_badges = [progress.badge for progress in youth.badgeprogress]

    warnings = []

    skipped = check_for_skipped_badges(youth_badges)
    if skipped is not None:
        warnings.extend(skipped)

    missing = check_for_missing_badges(youth_skills, youth_badges)
    if missing is not None:
        warnings.extend(missing)

    unearned = check_for_unearned_badges(youth_skills, youth_badges)
    if unearned is not None:
        warnings.extend(unearned)

    return warnings


@app.route("/youth/<youth_id>")
def youth_details(youth_id):
    youth = Youth.query.filter_by(id=youth_id).first_or_404()
    badges = get_next_badges(youth)
    warnings = validate_badge_information(youth)
    return render_template(
        "youth_detail.html",
        title="Youth Details",
        youth=youth,
        next_badges=badges,
        warnings=warnings,
    )
