from datetime import datetime
from enum import Enum
from app import db

group_leaders = db.Table(
    "group_leaders",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    groups = db.relationship(
        "Group",
        secondary=group_leaders,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def __repr__(self):
        return "<User {}>".format(self.username)


skill_achievements = db.Table(
    "skill_achievements",
    db.Column(
        "skill_record_id",
        db.Integer,
        db.ForeignKey("skill_record.id"),
        primary_key=True,
    ),
    db.Column("youth_id", db.Integer, db.ForeignKey("youth.id"), primary_key=True),
)


class Youth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    group = db.relationship("Group", backref="youth", lazy=True, uselist=False)

    skill_records = db.relationship(
        "SkillRecord",
        secondary=skill_achievements,
        lazy="subquery",
        backref=db.backref("youth", lazy=True),
    )

    def __repr__(self):
        return "<Youth {} ({})>".format(self.name, self.group)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return "<Group {}>".format(self.name)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))

    requirements = db.relationship("BadgeRequirement", lazy=True, backref="skill")

    def __repr__(self):
        return "<Skill {}>".format(self.description)


class SkillRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    notes = db.Column(db.String(128))
    scouter_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"))

    # TODO There should be a unique constraint on skill_id and youth id

    scouter = db.relationship("User", backref="skillrecord", lazy=True, uselist=False)
    skill = db.relationship("Skill", backref="skillrecord", lazy=True, uselist=False)

    def __repr__(self):
        return "<Skill Record for {}>".format(self.skill.description)


class BadgeRequirement(db.Model):
    badge_id = db.Column(db.Integer, db.ForeignKey("badge.id"), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"))
    position = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<BadgeRequirement {} {} {} ({})>".format(
            self.badge.description,
            self.badge.level,
            self.position,
            self.skill.description,
        )


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    level = db.Column(db.Integer)

    requirements = db.relationship("BadgeRequirement", lazy=True, backref="badge")

    def __repr__(self):
        return "<Badge {} {}>".format(self.description, self.level)


class BadgeState(Enum):
    ACHIEVED = "Achieved"
    AWARDED = "Awarded"


class BadgeProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey("badge.id"))
    youth_id = db.Column(db.Integer, db.ForeignKey("youth.id"))
    badge_state = db.Column(db.Enum(BadgeState))
    badge = db.relationship("Badge", backref="badgeprogress", lazy=True, uselist=False)
    youth = db.relationship("Youth", backref="badgeprogress", lazy=True, uselist=False)

    def __repr__(self):
        return "<{}'s Badge Progress for {}: {}>".format(
            self.youth.name, self.badge.description, self.badge_state
        )
