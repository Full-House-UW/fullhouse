#!/bin/bash

# http://technomilk.wordpress.com/2011/09/03/publishing-django-test-coverage-reports-in-jenkins/
# clean up previous results:
rm htmlcov/*
rm .coverage

# we do not want coverage data for South migrations:
#PARMS=--omit='*migrations*','*tests*'

# run the tests and collect coverage, only for our applications
coverage run --source=fullhouse/dashboard ./manage.py test

# generate plaintext and HTML report
echo "----------------------------"
echo "Coverage results:"
coverage report $PARMS
coverage html $PARMS
echo "HTML report generated in htmlcov/index.html"

# optionally display an HTML report
if [ "$1" == "-f" ]
then
  firefox htmlcov/index.html
fi
