#!/usr/bin/env python
# encoding: utf-8
from flask import current_app
from flask.ext.mail import Message

from application.extensions import mail


def send_mail(receiver, title, content):
    msg = Message(title, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[receiver])
    msg.body = content
    mail.send(msg)
