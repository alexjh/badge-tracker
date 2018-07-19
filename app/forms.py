from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, SelectMultipleField, DateField, TextAreaField
from wtforms.validators import DataRequired
from app.models import User, Youth, Group
from app.models import Skill, Badge


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


def get_youth():
    groups = Group.query.all()

    youth_list = []

    for group in groups:
        youth_list.append(("", f"{group.name}"))

        youth_list.extend([(int(youth.id), f"* {youth.name}") for youth in group.youth])
    return youth_list


def get_leaders():
    leaders = User.query.all()
    return [(leader.username, leader.username) for leader in leaders]


def get_skills():
    badges = Badge.query.all()
    skills = []

    for badge in badges:
        skills.append(("", f"{badge.description} - {badge.level}"))

        for requirement in badge.requirements:
            skills.append(
                (int(requirement.skill.id), f"* {requirement.skill.description}")
            )
    return skills


class SkillRecordForm(FlaskForm):
    date = DateField("Event Date", validators=[DataRequired()])
    notes = TextAreaField("Event Info", validators=[DataRequired()])
    leader = SelectField("Leader", choices=get_leaders(), validators=[DataRequired()])
    participants = SelectMultipleField(
        "Participants", choices=get_youth(), coerce=int, validators=[DataRequired()]
    )
    skills = SelectMultipleField(
        "Skills", choices=get_skills(), coerce=int, validators=[DataRequired()]
    )
    submit = SubmitField("Record Skills")
