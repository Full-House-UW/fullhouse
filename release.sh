#!/bin/bash

if [ $# -eq 0 ]; then
  echo must specify a release branch
  exit
fi

ssh heff@heff.webfactional.com "
source webapps/fullhouse/env/bin/activate
cd webapps/fullhouse/fullhouse

echo
echo ----------------------------------------------------------
echo

echo fetching changes from branch \'$1\'

git pull origin $1
git checkout $1

echo
echo ----------------------------------------------------------
echo

echo installing new dependencies

pip install -r requirements.txt

echo
echo ----------------------------------------------------------
echo

echo copying static files

cp -r ~/webapps/fullhouse/fullhouse/fullhouse/static/* ~/webapps/fullhouse_static/

echo
echo ----------------------------------------------------------
echo

echo restarting apache web server

~/webapps/fullhouse/apache2/bin/restart

echo
echo ----------------------------------------------------------
echo

echo release complete
echo
"
