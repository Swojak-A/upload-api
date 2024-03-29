#!/usr/bin/env python

import os
import time
from flask import Flask
from flask import jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import boto3
from PIL import Image, ImageOps
from io import BytesIO

from config import BaseConfig

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
bucket_url = os.environ['BUCKET_URL']

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

from models import *


""" HELPER FUNCTIONS """


def filename_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    is_allowed = '.' in filename and \
                 filename_ext(filename) in app.config['ALLOWED_EXTENSIONS']
    return is_allowed


""" AUTH FUNCTIONS """


@auth.get_password
def get_password(input_username):
    username = os.environ['AUTH_USER']
    password = os.environ['AUTH_PASS']

    if input_username == username:
        return password
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'status': 'error: unauthorized access'}), 401




""" ROUTING """


@app.route("/", methods=["GET", "POST"])
@auth.login_required
def index():
    if request.method == "POST":
        # check if request is correct
        if 'file' not in request.files:
            return jsonify({"status": "error: no file detected"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"status": "error: empty filename detected"}), 400
        if not allowed_file(file.filename):
            return jsonify({"status": "error: file with that extension is not allowed"}), 400

        # if input is correct then...
        if file:
            # prepare image data to record it in db
            lastUpload = Upload.query.order_by(Upload.id.desc()).first()

            if lastUpload == None:
                id = 1
            else:
                id = lastUpload.id + 1

            new_filename = "Image_{}_{}.{}".format(str(100000 + id),
                                                   str(time.time()).replace(".",""),
                                                   filename_ext(file.filename))
            file_url = "{}{}{}".format(bucket_url,
                                         'uploads/',
                                         new_filename)

            file_content = file.read()

            # resize inputted image file
            try:
                img = Image.open(file)

                medium_size = (400, 300)
                small_size = (120, 90)

                if 'size' in request.args:
                    size_param = request.args.get('size')
                    if size_param.lower() == 'small':
                        size = small_size
                    elif size_param.lower() == 'medium':
                        size = medium_size
                    else:
                        return jsonify({"status": "error: the only values allowed for 'size' key are: 'medium' and 'small'"}), 400
                else:
                    size = medium_size

                if img.size[0] >= size[0] and img.size[1] >= size[1]:
                    img = ImageOps.fit(img, size, method=Image.ANTIALIAS, centering=(0.5, 0.5))
                else:
                    return jsonify({"status": "error: file is too small to resize it"}), 422

            except OSError as err: # OSError catches files that have corrupted content, but proper ext
                return jsonify({"status": "error: the file is corrupted or is not a proper image file"}), 422
            except Exception as err:
                raise err

            # write record to db
            newUpload = Upload(filename=new_filename,
                               url=file_url,
                               original_filename=file.filename)
                               # file=file_content) # we temporarily don't save orig file content due to limited db capacity
            db.session.add(newUpload)
            db.session.commit()

            # uploade resized image to aws s3
            s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

            out_img = BytesIO()
            img.save(out_img, filename_ext(new_filename).replace('jpg', 'jpeg')) # PIL only accepts "JPEG" file format

            out_img.seek(0) # in case of botocore.exceptions.ClientError: An error occurred (BadDigest) when ...
            s3.put_object(Key='uploads/{}'.format(new_filename),
                          Body=out_img,
                          Bucket='upload-api-task')

            # return a succesfull response
            return jsonify({"status": "success",
                            "id": newUpload.id,
                            "filename": new_filename,
                            "url": file_url,
                            "original_filename": file.filename}), 201

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
