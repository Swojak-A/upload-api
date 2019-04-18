#!/usr/bin/env python

import os
from flask import Flask
from flask import jsonify, request, abort
from werkzeug.utils import secure_filename

from config import BaseConfig

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
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify({"success": "true"}), 201

    return jsonify({"success": "true"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
