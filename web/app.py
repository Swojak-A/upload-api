#!/usr/bin/env python

import os
from flask import Flask
from flask import jsonify, request, abort
import boto3

from config import BaseConfig

from credentials import aws_access_key_id, aws_secret_access_key

app = Flask(__name__)
app.config.from_object(BaseConfig)

from models import *


""" HELPER FUNCTIONS """


def allowed_file(filename):
    is_allowed = '.' in filename and \
                 filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
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
            s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

            # file.seek(0) # in case of botocore.exceptions.ClientError: An error occurred (BadDigest) when ...
            s3.put_object(Key='uploads/file_name.jpg',
                          Body=request.files['file'],
                          Bucket='upload-api-task')

            return jsonify({'success': 'true'}), 201

    return jsonify({'success': 'true'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
