#!/usr/bin/env python

from app import db
from app.models import User

for user in [
    ("john", "john@example.com"),
    ("bob", "bob@example.com"),
    ("doug", "doug@example.com"),
]:
    u = User(username=user[0], email=user[1])
    db.session.add(u)
    db.session.commit()
