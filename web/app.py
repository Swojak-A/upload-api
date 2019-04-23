#!/usr/bin/env python

import os
import time
from flask import Flask
from flask import jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import boto3
from PIL import Image, ImageOps
from io import BytesIO

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

            file_content = file.read()

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
                        abort(400)
                else:
                    size = medium_size

                if img.size[0] >= size[0] and img.size[1] >= size[1]:
                    img = ImageOps.fit(img, size, method=Image.ANTIALIAS, centering=(0.5, 0.5))
                else:
                    abort(422)

            except OSError as err: # OSError catches files that have corrupted content, but proper ext
                abort(422)
            except Exception as err:
                raise err


            newUpload = Upload(filename=new_filename,
                               url=file_url,
                               original_filename=file.filename,
                               file=file_content)
            db.session.add(newUpload)
            db.session.commit()


            s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

            out_img = BytesIO()
            img.save(out_img, filename_ext(new_filename).replace('jpg', 'jpeg')) # PIL only accepts "JPEG" file format

            out_img.seek(0) # in case of botocore.exceptions.ClientError: An error occurred (BadDigest) when ...
            s3.put_object(Key='uploads/{}'.format(new_filename),
                          Body=out_img,
                          Bucket='upload-api-task')



            return jsonify({'id': newUpload.id,
                           'filename': new_filename,
                            'url' : file_url}), 201

    return jsonify({'success': 'true'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
