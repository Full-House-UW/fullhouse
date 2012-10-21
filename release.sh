#!/bin/bash

ssh heff@heff.webfactional.com "
source webapps/fullhouse/env/bin/activate

cd webapps/fullhouse/fullhouse

echo fetching changes from branch '$1'
git pull origin $1

echo
echo installing new dependencies
pip install -r requirements.txt

echo
echo copying static files
cp -r ~/webapps/fullhouse/fullhouse/fullhouse/static/* ~/webapps/fullhouse_static/
"
