#!/bin/bash

apt-get install -y python-dev libxml2 libxml2-dev libxslt-dev
apt-get install -y python-lxml
apt-get install -y libmysqlclient-dev
apt-get install -y libffi-dev

pip install urllib3 --upgrade
