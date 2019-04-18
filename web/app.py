#!/usr/bin/env python

import os
import time
from flask import Flask
from flask import jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import boto3

from config import BaseConfig

from credentials import aws_access_key_id, aws_secret_access_key, url_bucket

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *


""" HELPER FUNCTIONS """


def filename_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    is_allowed = '.' in filename and \
                 filename_ext(filename) in app.config['ALLOWED_EXTENSIONS']
    return is_allowed


""" ROUTING """


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            abort(400)

        file = request.files['file']

        if file.filename == '':
            abort(400)
        if not allowed_file(file.filename):
            abort(400)

        if file:
            lastUpload = Upload.query.order_by(Upload.id.desc()).first()

            if lastUpload == None:
                id = 1
            else:
                id = lastUpload.id + 1



            new_filename = "Image_{}_{}.{}".format(str(100000 + id),
                                                   str(time.time()).replace(".",""),
                                                   filename_ext(file.filename))
            file_url = "{}{}{}".format(url_bucket,
                                         'uploads/',
                                         new_filename)

            newUpload = Upload(new_filename,
                               file_url)
            db.session.add(newUpload)
            db.session.commit()

            s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

            # file.seek(0) # in case of botocore.exceptions.ClientError: An error occurred (BadDigest) when ...
            s3.put_object(Key='uploads/{}'.format(new_filename),
                          Body=request.files['file'],
                          Bucket='upload-api-task')



            return jsonify({'id': newUpload.id,
                           'filename': new_filename,
                            'url' : file_url}), 201

    return jsonify({'success': 'true'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
