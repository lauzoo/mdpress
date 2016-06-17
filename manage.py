#!/usr/bin/env python
# encoding: utf-8
import sys
import subprocess

from flask_script import Manager
from flask_script.commands import ShowUrls

from utils.init_db import init_db
from utils.commands import GEventServer, ProfileServer
from application import create_app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='mode', required=False)

manager.add_command("showurls", ShowUrls())
manager.add_command("gevent", GEventServer())
manager.add_command("profile", ProfileServer())


# @manager.command
@manager.option('-c', '--config', help='enviroment config')
def create_db(config):
    create_app(config)
    init_db()


@manager.option('-c', '--config', help='enviroment config')
def simple_run(config):
    app = create_app(config)
    app.run(debug=True)


@manager.command
def lint():
    """Runs code linter."""
    lint = subprocess.call(['flake8', '--ignore=E402,F403,E501', 'application/',
                            'manage.py', 'tests/']) == 0
    if lint:
        print('OK')
    sys.exit(lint)

if __name__ == "__main__":
    manager.run()
