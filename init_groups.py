#!/usr/bin/env python

from app import db
from app.models import Group

for group in ["4th PoCo Cubs", "4th PoCo Scouts", "10th PoCo Beavers"]:
    g = Group(name=group)
    db.session.add(g)
    db.session.commit()
