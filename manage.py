#!/usr/bin/env python
# encoding: utf-8
import sys
import subprocess

from flask_script import Manager
from flask_script.commands import ShowUrls

from utils.commands import GEventServer, ProfileServer
from application import create_app
import application.models as Models

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='mode', required=False)

manager.add_command("showurls", ShowUrls())
manager.add_command("gevent", GEventServer())
manager.add_command("profile", ProfileServer())


# @manager.command
@manager.option('-c', '--config', help='enviroment config')
def create_db(config):
    create_app(config)
    role = Models.Role.objects.filter(name="DELETER").first()
    if not role:
        Models.Role.objects.create(name="READER",
                                   permission=Models.Permission.READ)
        Models.Role.objects.create(
            name="CREATER",
            permission=Models.Permission.CREATE | Models.Permission.READ)
        Models.Role.objects.create(
            name="UPDATER",
            permission=(Models.Permission.UPDATE | Models.Permission.CREATE |
                        Models.Permission.READ))
        Models.Role.objects.create(
            name="DELETER",
            permission=(Models.Permission.DELETE | Models.Permission.UPDATE |
                        Models.Permission.CREATE | Models.Permission.READ))
        print "create roles finish..."
    else:
        print "no need to create role..."

    users = Models.User.objects.filter(name='admin')
    if not users:
        role = Models.Role.objects.filter(name='DELETER').first()
        Models.User(name="admin", password="admin",
                    email="liqianglau@outlook.com", role=[role]).save()
        print "create admin finish..."
    else:
        print "user admin exists..."


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
