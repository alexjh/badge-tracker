#!/usr/bin/env python

from app import db
from app.models import Youth, Badge, BadgeState, SkillRecord, User
from app.models import BadgeProgress

matt = Youth.query.filter_by(name="Matthew").first()
andrew = Youth.query.filter_by(name="Andrew").first()

scouter = User.query.filter_by(username="john").first()

winter1 = Badge.query.filter_by(description="Winter", level=1).first()

for requirement in winter1.requirements:
    record = SkillRecord(
        notes="Winter Camp 2017",
        scouter=scouter,
        skill=requirement.skill,
        youth=[matt, andrew],
    )
    db.session.add(record)

winter2 = Badge.query.filter_by(description="Winter", level=2).first()

for requirement in winter2.requirements:
    record = SkillRecord(
        notes="Winter Camp 2016", scouter=scouter, skill=requirement.skill, youth=[matt]
    )
    db.session.add(record)

db.session.commit()


# For each of Matt's skills records
youth_skills = {record.skill for record in matt.skill_records}

for badge in Badge.query.all():
    badge_skills = {requirement.skill for requirement in badge.requirements}
    if badge_skills.issubset(youth_skills):
        badges = [badgeprogress.badge for badgeprogress in matt.badgeprogress]
        if badge not in badges:
            print(f"{badge} achieved!")
            progress = BadgeProgress(
                badge_state=BadgeState.ACHIEVED, badge=badge, youth=matt
            )
            db.session.add(progress)
            db.session.commit()
        else:
            print(f"{badge} already achieved")
