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

GIT_REPO = 'git://github.com/Full-House-UW/fullhouse.git'

APP_PATH = '/home/heff/webapps/'


# arguments:
# - stack: qa or prod -- the stack to release to
#
# returns:
# - a pair where the first element is name of the dynamic app folder, and the
#   second element is the name of the static folder
def get_release_apps(stack):
    """
    >>> get_release_apps('qa')
    ('qa_fullhouse/', 'qa_fullhouse_static/')
    """

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


# arguments:
# - stack: qa or prod -- the stack to release to
#
# returns:
# - a pair where the first element is path to the dynamic app folder, and the
#   second element is the path to the static folder
def get_app_paths(stack):
    """
    >>> get_app_paths('qa')
    ('/home/heff/webapps/qa_fullhouse/', '/home/heff/webapps/qa_fullhouse_static/')
    """
    apps = get_release_apps(stack)
    dynamic_app_path = APP_PATH + apps[0]
    static_app_path = APP_PATH + apps[1]
    return (dynamic_app_path, static_app_path)


def get_repo(path, commit, repo):
    run("mkdir -p %s" % path)
    with cd(path):
        run("rm -rf fullhouse/")
        run("git clone " + repo)
        with cd("fullhouse/"):
            run("git checkout " + commit)


@task
def release(stack, commit):
    """
    release a specific commit to qa or prod

    Usage: fab release:stack,commit
    arguments:
    - stack: qa or prod -- the stack to release to
    - commit: the github branch, tag, or commit hash to release
    """
    dynamic, static = get_app_paths(stack)

    print "Checking for existence of '%s'" % commit
    # errors out on failure
    get_repo("tmp", commit, GIT_REPO)
    print "'%s' is a valid commit -- continuing" % commit
    print

    get_repo(dynamic, commit, GIT_REPO)
    with cd(dynamic):

        run("source env/bin/activate && pip install -r fullhouse/requirements.txt")
        run("source env/bin/activate && pip install -r fullhouse/server_requirements.txt")

    run("STACK=" + stack + " STATIC_ROOT=" + static + " erb local.py.erb > " + dynamic + "fullhouse/fullhouse/settings/local.py")

    with cd(dynamic):
        run("source env/bin/activate && fullhouse/manage.py collectstatic -l --noinput")

    run("rm -f " + dynamic + "fullhouse/initial_data.json")

    with cd(dynamic + "fullhouse/"):
        run("source ../env/bin/activate && ./manage.py syncdb")
        run("source ../env/bin/activate && ./manage.py migrate")

    run(dynamic + "apache2/bin/restart")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
