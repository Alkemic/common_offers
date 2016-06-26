#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request

import ceneo
import allegro


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ceneo", methods=["POST"])
def view_ceneo():
    urls = [url for url in request.form.getlist("url") if url != ""]
    sums = ceneo.get_sumed_offers(urls)
    return jsonify(result=sums)


@app.route("/allegro", methods=["POST"])
def view_allrgo():
    sums = allegro.get_sumed_offers(
        filter(None, request.form.getlist("user")),
        filter(None, request.form.getlist("item_name"))
    )
    return jsonify(result=sums)


if __name__ == "__main__":
    app.run(debug=True)
