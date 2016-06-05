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


@manager.command
def create_db():
    role = Models.Role.objects.filter(
        permission=Models.Permission.DELETE).first()
    if not role:
        Models.Role(id=1, name="READER", permission=Models.Permission.READ).save()
        Models.Role(id=2, name="CREATER", permission=Models.Permission.CREATE).save()
        Models.Role(id=3, name="UPDATER", permission=Models.Permission.UPDATE).save()
        Models.Role(id=4, name="DELETER", permission=Models.Permission.DELETE).save()
        print "create roles finish..."
    else:
        print "no need to create role"


if __name__ == "__main__":
    manager.run()
