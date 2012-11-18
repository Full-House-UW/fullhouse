Instruction for username-email migration


IMPORTANT: You must run the commands in the exact order
specified. If the order is changed or a step missed,
the migration will fail and very probably break the database.

Steps:

1. Pull changes as usual. You must have the change which
includes the updated migrate_fullhouse_usernames script

2. Edit your local.py to add the following:
```python
from os.path import abspath, join
from default import PROJECT_ROOT, TEMPLATE_PATH

tool_template_path = abspath(join(PROJECT_ROOT, 'tools'))

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
    tool_template_path,
)
```
This is to add give the template loader access to 2 templates
used by the migration script in the next step.

3. Run the following sequence of commands:
```bash
./manage.py shell
```
```python
from tools import migrate_fullhouse_usernames
migrate_fullhouse_usernames()
```

This runs the initial migration script that handles existing
duplicate users (it uses the '+' trick to change the emails of
users who have duplicate emails to to an equivalent email,
e.g. herp@derp.com -> herp+herp2@derp.com). It will also send
and email to each user whose email it changes, notifying them
of the change and reason for it (see auth_update_email.txt).

If this script finishes successfully you should see a message
like the following one:
```
Updated duplicate emails for 2 of 4 accounts
Successfully migrated usernames for all 6 users
```
4. Run
```bash
./convert_to_south.sh
```
To complete the migration

5. Congratulations, migration complete. Go have a drink or a
nap or something.


