#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request

from ceneo import get_sumed_offers


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ceneo", methods=["POST"])
def ceneo():
    urls = [url for url in request.form.getlist('url') if url != ""]
    sums = get_sumed_offers(urls)
    return jsonify(result=sums)


if __name__ == "__main__":
    app.run(debug=True)
