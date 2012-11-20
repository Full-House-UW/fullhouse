#!/bin/bash

# This script simply assists in converting existing databases to use South.
# Because existing databases already have the original models set up, we tell
# South to skip this initial setup, and then tell it to apply all remaining
# changes

./manage.py syncdb
./manage.py migrate dashboard 0001 --fake
./manage.py migrate dashboard
