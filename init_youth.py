#!/usr/bin/env python

from app import db
from app.models import Youth, Group

for youth in [("Matthew", "4th PoCo Scouts"), ("Andrew", "4th PoCo Cubs")]:
    group = Group.query.filter_by(name=youth[1]).first()
    y = Youth(name=youth[0])
    y.group = group
    db.session.add(y)
    db.session.commit()
