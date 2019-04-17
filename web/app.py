#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():

	html = "<h3>Upload API!</h3>"

	return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
