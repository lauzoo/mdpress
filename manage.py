#!/usr/bin/env python
# encoding: utf-8
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
    print config
    create_app(config)
    role = Models.Role.objects.filter(
        permission=Models.Permission.DELETE).first()
    if not role:
        Models.Role(name="READER", permission=Models.Permission.READ).save()
        Models.Role(name="CREATER",
                    permission=Models.Permission.CREATE | Models.Permission.READ).save()
        Models.Role(name="UPDATER",
                    permission=Models.Permission.UPDATE | Models.Permission.CREATE |
                    Models.Permission.READ).save()
        Models.Role(name="DELETER",
                    permission=Models.Permission.DELETE | Models.Permission.UPDATE |
                    Models.Permission.CREATE | Models.Permission.READ).save()
        print "create roles finish..."
    else:
        print "no need to create role..."

    user = Models.User.objects.first()
    if not user:
        role = Models.Role.objects.filter(name='DELETER').first()
        Models.User(username="admin", password="admin", email="liqianglau@outlook.com",
                    role=role).save()
        print "create admin finish..."
    else:
        print "user admin exists..."


@manager.option('-c', '--config', help='enviroment config')
def simple_run(config):
    app = create_app(config)
    app.run(debug=True)

if __name__ == "__main__":
    manager.run()
