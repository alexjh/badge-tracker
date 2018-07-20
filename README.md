# Badge Tracker

* TODO
  [x] User list
  [x] Group list
  [x] Youth list
      * List badges, skills
  [x] Skill list
  [x] Badge list
  [x] Skill Record
  [x] Add user, group, youth
  [x] Badge Progress for youth

  [ ] Merge requirements - paddling, sailing, aquatic
  [ ] Add camp record
  [ ] Handle deleting skill records
    [ ] Cascade to youth's skills
  [ ] Badge consistency warnings
    [x] Earned all skills without having badge
    [x] Earned badge without having all skills
    [x] Earned higher level badge without lower level


## DB Layout

* groups (name, id)
* leaders (name, password, group_id)
* scouts (name, id)
* group_members (id, scout_id)
* badges (name, id)
* badge_skills( badge_id, skill_id)
* skill_details (id, details)
* skill_record (id, date, details, leader_id)
* badge_distribution (id, date, leader_id, state)
* scout_progress (id, badge_skill_id)
* scout_badges (id, badge_id)

- a leader can be in multiple groups
- a scout can only be in one group but can move
- a badge can change requirements
- a badge earned is permanent even if its skills change
- a skill can apply to multiple badges

## Workflows

### Recording skills

* A leader logs in
* Creates a skill record
  * selects a group
  * selects a skill (can filter by badges)
  * enters a date
  * enters details about this skill (location, etc)
* Records participants

If a participant completed a badge requirement, a notification pops up

### Camp Attendance

* select a group
* select participants
* enter camp details
  * name, location, winter?
* enter a camp date range
* select range for each member

### Recording Badge Distribution

* Get a list of Scouts with outstanding badges
* Checks off who has received them
* Applies changes

### Badge Recommendations

* Select a group
* Select a badge
* displays list of skills required for each member of a group
* displays a list of scouts who already have the badge

### Scout View

* select a group
* select a scout
* select a badge
  * if completed, displays details about when the skills were completed
  * if not completed, displays a list of skills required



## Libraries

* https://flask-socketio.readthedocs.io/en/latest/
* https://github.com/lingthio/Flask-User

## Examples

* https://github.com/tanrax/flask-chat-example
