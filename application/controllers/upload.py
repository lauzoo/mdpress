#!/usr/bin/env python
# encoding: utf-8
import os

import requests
from flask import (current_app, Blueprint, request,
                   url_for, send_from_directory)
from werkzeug.utils import secure_filename

import application.models as Models


upload_bp = Blueprint('upload', __name__, url_prefix='/uploads')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_to_sm(local_path):
    url = 'https://sm.ms/api/upload'
    files = {'smfile': open(local_path, 'rb')}
    r = requests.post(url, files=files)
    data1 = eval(r.text.encode('utf-8'))
    url1 = data1['data']['url']
    return url1


@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'uploadimage' not in request.files:
            return "no upload images"
        file = request.files['uploadimage']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "no filenames"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            local_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                      filename)
            file.save(local_path)
            url = upload_to_sm(local_path)
            Models.Upload(filename=file.filename,
                          local_path=local_path,
                          url=url).save()
            return '"{}"'.format(url_for('upload.uploaded_file',
                                         filename=filename))


@upload_bp.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
