#!/usr/bin/env python

from app import db
from app.models import Skill, Badge, BadgeRequirement

badges = [
    "Aquatic",
    "Camping",
    "Emergency",
    "Paddling",
    "Sailing",
    "Scoutcraft",
    "Trail",
    "Vertical",
    "Winter",
]

skills = [
    ("Aquatic", 1, 1, "I know when to use a PFD (Personal Floatation Device)."),
    (
        "Aquatic",
        1,
        2,
        "I can float for five seconds and glide for five metres on my front and back without assistance.",
    ),
    ("Aquatic", 1, 3, "I can put my face in the water and blow bubbles."),
    (
        "Aquatic",
        1,
        4,
        "I understand the importance of the buddy system, and how it works for swimming and water activities. ",
    ),
    ("Aquatic", 1, 5, "I know how to stay safe while playing around water."),
    ("Aquatic", 1, 6, "I can get an object off the bottom in chest-deep water."),
    ("Aquatic", 1, 7, "I know three different animals that live in the ocean."),
    ("Aquatic", 2, 1, "I can swim with my head in the water."),
    ("Aquatic", 2, 2, "I can swim 10 metres (any stroke) without assistance."),
    ("Aquatic", 2, 3, "I know how to put on a PFD by myself."),
    ("Aquatic", 2, 4, "I know how snorkel gear works."),
    ("Aquatic", 2, 5, "I have snorkeled in a pool or open water (such as a lake)."),
    ("Aquatic", 3, 1, "I can explain common water safety risks and how to avoid them."),
    ("Aquatic", 3, 2, "I can use a snorkel and adjust my mask to fit comfortably."),
    ("Aquatic", 3, 3, "I know how to remove a cramp in my leg with a buddy’s help."),
    (
        "Aquatic",
        3,
        4,
        "I can put on a PFD while in the water and use the HELP and huddle positions.",
    ),
    ("Aquatic", 3, 5, "I can swim 25 metres in a pool (using any stroke)."),
    (
        "Aquatic",
        3,
        6,
        "I can recognize the signs of a panicked snorkeler or diver and know how to call for help.",
    ),
    (
        "Aquatic",
        4,
        1,
        "I have achieved Aquaquest Stage 6, YMCA Swimmer Level, Red Cross Swim Kids Stage 5, or I can demonstrate equivalent skills.",
    ),
    (
        "Aquatic",
        4,
        2,
        "I can free dive with snorkel and mask to 1.5 metres and fetch an item from the bottom, and clear my snorkel upon surfacing—without lifting my head out of the water.",
    ),
    ("Aquatic", 4, 3, "I can explain the hazards of shallow water blackout."),
    (
        "Aquatic",
        4,
        4,
        "I know what gear is necessary for a water-based snorkel adventure, including protective clothing, masks and sunscreen.",
    ),
    ("Aquatic", 4, 5, "I know how to select a safe place to snorkel."),
    (
        "Aquatic",
        4,
        6,
        "I have snorkeled in open water and observed at least one marine creature.",
    ),
    (
        "Aquatic",
        4,
        7,
        "I know why ear equalization is necessary when snorkelling or diving at depth.",
    ),
    (
        "Aquatic",
        5,
        1,
        "I have tried an introductory Scuba experience in a pool (Bubblemaker/SEAL Team/Discover Scuba Diving).",
    ),
    (
        "Aquatic",
        5,
        2,
        "I can identify five species in my local aquatic environment (either on the surface or underwater), including hazardous species.",
    ),
    ("Aquatic", 5, 3, "I can achieve the “Swim to Survive” standard."),
    (
        "Aquatic",
        6,
        1,
        "I have completed at least Emergency First Aid, or an equivalent course.",
    ),
    ("Aquatic", 6, 2, "I have completed the Open Water Diver Certification."),
    (
        "Aquatic",
        6,
        3,
        "I have gone for two additional dives after the Open Water Diver Certification dive.",
    ),
    (
        "Aquatic",
        6,
        4,
        "I have talked with a younger Section about my diving experience.",
    ),
    (
        "Aquatic",
        6,
        5,
        "I have assisted with Scouts (who are at Stage 3 or 4) learning to snorkel in open water.",
    ),
    (
        "Aquatic",
        7,
        1,
        "I have logged at least five open water dives and assisted in the planning.",
    ),
    (
        "Aquatic",
        7,
        2,
        "I can navigate with a compass underwater and understand the specific challenges of underwater navigation (currents, lack of landmarks, etc.).",
    ),
    (
        "Aquatic",
        7,
        3,
        "I have participated in a marine environmental service project, cleaning up a body of water.",
    ),
    (
        "Aquatic",
        7,
        4,
        "I have two of the following experiences: • I can shoot an underwater photo or video and understand the impacts of water on light.  • I have either found or placed an underwater geocache.  • I have used a dry suit (in cooler waters).  • I have performed basic repairs on my gear (replacing a mouthpiece with a spare etc.).  • I have taken part in a non-penetration wreck dive or any other specialty dive course.  • I have helped a younger Scout at Stage 4 or 5 learn how to...(Scout’s choice).",
    ),
    ("Aquatic", 8, 1, "I have completed an Advanced Open Water Certification."),
    (
        "Aquatic",
        8,
        2,
        "I have led a less experienced buddy on a dive through a site that is new to the buddy.",
    ),
    ("Aquatic", 8, 3, "I have drawn a rough map of a dive site."),
    ("Aquatic", 8, 4, "I have assisted Scouts with their dives at Stage 5 or 6."),
    ("Aquatic", 9, 1, "I have organized a dive trip for a Rover Crew."),
    (
        "Aquatic",
        9,
        2,
        "I have completed a Rescue Diver Certification course, or have learned and mastered the curriculum to demonstrate the equivalent skills.",
    ),
    (
        "Aquatic",
        9,
        3,
        "I have assisted Scouts at Stage 6 or 7 with learning dive navigation or other advanced dive skills.",
    ),
    (
        "Aquatic",
        9,
        4,
        "I have completed one of the following dives: • A “deep dive” to more than 80 feet/24.36m • An altitude dive • A dive on nitrox • A DPV dive • A search-and-recovery dive",
    ),
]

for badge in badges:
    for level in range(1, 10):
        b = Badge(description=badge, level=level)
        db.session.add(b)

db.session.commit()

for skill in skills:
    badge = Badge.query.filter_by(description=skill[0], level=skill[1]).first()
    s = Skill(description=skill[3])
    requirement = BadgeRequirement(position=skill[2], badges=badge, skills=s)
    db.session.add(s)
    db.session.add(requirement)
    db.session.commit()
