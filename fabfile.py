from fabric.api import task, local, lcd
from fabric.context_managers import warn_only
import os


fabfile_dir = os.path.realpath(os.path.dirname(__file__))


def db_commands(username):
    cmds =  [
        "python manage.py migrate",
        "python manage.py load_lookup_lists -f data/lookuplists/lookuplists.json",
    ]
    python_cmd = "echo '"
    python_cmd += "from django.contrib.auth.models import User; "
    python_cmd += "User.objects.create_superuser(\"{0}\", \"{0}@example.com\", \"{0}1\")".format(username)
    python_cmd += "' | python ./manage.py shell"
    cmds.append(python_cmd)
    return cmds


def push_to_heroku(remote_name):
    with lcd(fabfile_dir):
        current_branch_name = local(
            "git rev-parse --abbrev-ref HEAD", capture=True
        )
        local("git push {0} {1}:master".format(
            remote_name, current_branch_name)
        )


@task
def create_heroku_instance(name, username):
    """
    creates and populates a heroku instance
    TODO make sure that we're fully committed git wise before pushing
    """
    with lcd(fabfile_dir):
        local("heroku apps:create {}".format(name))
        git_url = "https://git.heroku.com/{}.git".format(name)
        local("git remote add {0} {1}".format(name, git_url))
        push_to_heroku(name)
        with warn_only():
        #     # heroku somtimes has memory issues doing migrate
        #     # it seems to work fine if we just migrate opal first
        #     # it will later fail because content types haven't
        #     # been migrated, but that's fine we'll do that later
            local("heroku run --app {0} python manage.py migrate opal".format(
                name
            ))
        for db_command in db_commands(username):
            local("heroku run --app {0} {1}".format(name, db_command))
