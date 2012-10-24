from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

# TODO pull out more functions and string constants

SERVER = 'fullhousemanager.com'
USER = 'heff'
SSH_STRING = USER + '@' + SERVER
env.hosts = [SSH_STRING]

QA_APPS = ('qa_fullhouse/', 'qa_fullhouse_static/')
PROD_APPS = ('fullhouse/', 'fullhouse_static/')

APP_PATH = 'webapps/'

def get_release_apps(stack):
    if (stack == 'qa'):
        return QA_APPS
    elif (stack == 'prod'):
        confirm = raw_input('Release to production? [y/n]: ')
        if (confirm == 'y'):
          return PROD_APPS
        else:
          return None
    else:
        print("stack must be qa or prod")
        return None

def get_app_paths(stack):
    apps = get_release_apps(stack)
    dynamic_app_path = APP_PATH + apps[0]
    static_app_path = APP_PATH + apps[1]
    return (dynamic_app_path, static_app_path)

# arguments:
# - stack: qa or prod -- the stack to release to
# - branch: the github branch or tag to release
def release(stack, branch):
    dynamic, static = get_app_paths(stack)

    with cd(dynamic):
        with cd("fullhouse/"):
            run("git fetch --tags")
            run("git checkout " + branch)

        run("source env/bin/activate && pip install -r fullhouse/requirements.txt")

    run("cp -r " + dynamic + "fullhouse/fullhouse/static/* " + static)

    run(dynamic + "apache2/bin/restart")
