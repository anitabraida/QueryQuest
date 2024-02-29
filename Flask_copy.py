from flask import Flask, render_template, request
from tfidf_search import tf_idf
import matplotlib as mlp
import pke
import os
from matplotlib import pyplot as plt
from collections import defaultdict
import nltk
import json
from boolean_search import boolean_search


app = Flask(__name__)

file = "data.json"
scraped_data = []

with open(file, "r") as f:
    json_data = json.load(f)

    for job_data in json_data:
        job_dict = {
            "title": job_data.get("title", ""),
            "description": job_data.get("description", ""),
            "link": job_data.get("link", ""),
        }
        scraped_data.append(job_dict)

mlp.use("Agg")


@app.route("/")
def index():
    return render_template("index.html", matches=[])


@app.route("/search")
def search():
    query = request.args.get("query")
    search_method = request.args.get("method", "tf-idf")  # Default to "tfidf" if no method is provided

    matches = []
    matches_keyphrases = {}
    if query:
        if search_method == "boolean":
            matches = boolean_search(query=query, scraped_data=scraped_data)
        else:     
            matches = tf_idf(query=query, scraped_data=scraped_data)
        return render_template("index.html", query=query.lower(), matches=matches)


if __name__ == "__main__":
    app.run(debug=True)
