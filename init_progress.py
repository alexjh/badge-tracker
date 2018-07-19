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
