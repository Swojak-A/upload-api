#!/usr/bin/env python

from flask import Flask
from flask import jsonify, request

app = Flask(__name__)

from models import test_result

@app.route("/", methods=["GET"])
def index():

    test = test_result

    return jsonify({"data" : test_result}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
