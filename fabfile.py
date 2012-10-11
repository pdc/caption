# -*-coding: UTF-8 -*-
# Run these commands with fab

from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

env.hosts = ['caption@spreadsite.org']

def test():
    with settings(warn_only=True):
        result = local('./manage.py test articles', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def push():
    local('git push')

def deploy():
    test()
    push()

    code_dir = '/home/caption/Sites/caption'
    with cd(code_dir):
        run('git pull')
        run('. ~/virtualenvs/bootstrap/bin/activate && ./manage.py collectstatic --noinput')