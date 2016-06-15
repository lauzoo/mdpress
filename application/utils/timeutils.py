#!/usr/bin/env python
# encoding: utf-8
import sys
import json
import string
import random
import datetime
import subprocess
from datetime import datetime
from datetime import tzinfo
from dateutil import tz


LOCAL_TZ = pytz.timezone("Asia/Shanghai")


def to_utc(dt):
    local_dt = LOCAL_TZ.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def to_local(dt):
    with_tz = pytz.UTC.localize(dt)
    local_dt = with_tz.astimezone(LOCAL_TZ)
    return local_dt


def convert_datetime_navie_to_aware(dt):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('UTC')

    dt = dt.replace(tzinfo=from_zone)
    return dt.astimezone(to_zone)


def get_beijing_time():
    beijing_timezone = timezone('Asia/Shanghai')
    utc_timezone = timezone('UTC')
    curr_utc_time = utc_timezone.localize(datetime.utcnow())
    return curr_utc_time.astimezone(beijing_timezone)


class GMT_Beijing(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "Asia/Shanghai"


def format_date(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ''
    try:
        value = pytz.UTC.localize(value)
    except ValueError:
        pass
    local_dt = value.astimezone(LOCAL_TZ)
    return local_dt.strftime(format)


def isodate_to_local(datestr):
    datestr = datestr.split('+')[0]
    dt = datetime.datetime.strptime(datestr.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    return format_date(dt)


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds()


def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


def timesince(dt, default=None, reverse=False):
    """
        Returns string representing "time since" e.g.
        3 days ago, 5 hours ago etc.
        Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if not dt:
        return ''

    if default is None:
        default = u'刚刚'
    now = datetime.datetime.utcnow()
    diff = (dt - now) if reverse else now - dt

    if diff < datetime.timedelta(days=0):
        return default

    periods = (
        (diff.days / 365, u'年', u'年'),
        (diff.days / 30, u'月', u'月'),
        (diff.days / 7, u'周', u'周'),
        (diff.days, u'天', u'天'),
        (diff.seconds / 3600, u'小时', u'小时'),
        (diff.seconds / 60, u'分钟', u'分钟'),
        (diff.seconds, u'秒', u'秒'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if reverse:
            if period == 1:
                return u'剩余 %d %s' % (period, singular)
            else:
                return u'剩余 %d %s' % (period, plural)

        else:
            if period == 1:
                return u'%d%s前' % (period, singular)
            else:
                return u'%d%s前' % (period, plural)

    return default

