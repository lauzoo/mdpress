#!/usr/bin/env python
# encoding: utf-8
import os

from flask import Blueprint, jsonify, current_app, request
from werkzeug.utils import secure_filename

from application.services.upload import upload_to_cloud


upload_bp = Blueprint('upload', __name__, url_prefix='/uploads')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FILENAME = "editormd-image-file"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload_bp.route('/', methods=['POST'])
def upload_file():
    if UPLOAD_FILENAME not in request.files:
        return jsonify(success=0, message=u"没有找到文件")
    file = request.files[UPLOAD_FILENAME]
    if file.filename == '':
        return jsonify(success=0, message=u"没有找到文件名")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        local_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                    filename)
        file.save(local_path)
        image = upload_to_cloud(0, local_path)
        if image:
            current_app.logger.debug(image.to_json())
            return jsonify(success=1, message=u"上传成功", url=image.url)
        else:
            return jsonify(success=0, message=u"上传云失败")
    else:
        return jsonify(success=0, message=u"非允许的文件类型")
