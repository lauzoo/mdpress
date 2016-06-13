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
        Models.Role(id=1, name="READER", permission=Models.Permission.READ).save()
        Models.Role(id=2, name="CREATER",
                    permission=Models.Permission.CREATE | Models.Permission.READ).save()
        Models.Role(id=3, name="UPDATER",
                    permission=Models.Permission.UPDATE | Models.Permission.CREATE |
                    Models.Permission.READ).save()
        Models.Role(id=4, name="DELETER",
                    permission=Models.Permission.DELETE | Models.Permission.UPDATE |
                    Models.Permission.CREATE | Models.Permission.READ).save()
        print "create roles finish..."
    else:
        print "no need to create role..."

    user = Models.User.objects.filter(
        id=10000).first()
    if not user:
        role = Models.Role.objects.filter(id=4).first()
        Models.User(id=10000, username="admin", password="admin",
                    email="liqianglau@outlook.com",
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
