#!/usr/bin/env python
# encoding: utf-8
import subprocess
import sys

from flask_script import Manager
from flask_script.commands import ShowUrls

from application import create_app
from utils.commands import GEventServer, ProfileServer
from utils.init_db import init_db
from utils.init_data import main as init_data

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='mode', required=False)

manager.add_command("showurls", ShowUrls())
manager.add_command("gevent", GEventServer())
manager.add_command("profile", ProfileServer())


@manager.shell
def make_shell_context():
    import application.models as ms
    from application.extensions import redis
    return dict(app=manager.app, Models=ms, rds=redis)


@manager.option('-c', '--config', help='enviroment config')
def create_db(config):
    create_app(config)
    init_db()


@manager.option('-c', '--config', help='enviroment config')
def drop_db(config):
    from application.extensions import redis
    create_app(config)
    redis.flushall()


@manager.option('-c', '--config', help='enviroment config')
@manager.option('-l', '--location', help='wordpress backpack file path')
def wpimport(config=None, location=None):
    create_app(config)
    init_data(location)


@manager.option('-c', '--config', help='enviroment config')
def esindex(config=None):
    from datetime import datetime
    from elasticsearch import Elasticsearch

    import application.models as Models

    create_app(config)

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # 插入
    for post in Models.Post.objects.all():
        d = post.to_json()
        d.update({"timestamp": datetime.utcnow()})
        es.index(index="mdpress", doc_type="post", id=post.id,
                 body=d)


@manager.option('-c', '--config', help='enviroment config')
def simple_run(config):
    app = create_app(config)
    app.run(debug=True)


@manager.option('-c', '--config', help='enviroment config')
def run_fcgi(config):
    from flup.server.fcgi import WSGIServer
    app = create_app(config)
    server = WSGIServer(app, bindAddress='/tmp/mdpress.sock')
    server.run()


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
