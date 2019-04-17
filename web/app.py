#!/usr/bin/env python

from flask import Flask
from flask import jsonify, request, abort

app = Flask(__name__)

from models import test_result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.json:
            abort(400)
        if "name" not in request.json:
            abort(401)
        new_test_case = {"name" : request.json["name"]}
        test_result.append(new_test_case)
        return jsonify({"data" : test_result}), 201

    test = test_result

    return jsonify({"data" : test_result}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
