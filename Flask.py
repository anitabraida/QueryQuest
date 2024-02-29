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
import matplotlib.ticker as ticker

# clear the static folder of any remaining plots
os.system("rm -f static/*.png")

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

# create plot that displays trending titles


def generate_trending_plot():
    fig, ax = plt.subplots(figsize=(12, 8))

    # get popular titles
    job_title_frequencies = {}
    for title in scraped_data:
        job_title = title["title"]
        job_title_frequencies[job_title] = job_title_frequencies.get(job_title, 0) + 1

    popular_job_titles = sorted(
        job_title_frequencies.items(), key=lambda x: x[1], reverse=True
    )[:8]
    popular_titles, frequencies = zip(*popular_job_titles)
    ax.barh(popular_titles, frequencies, color="skyblue")

    # Set labels and rotation for better visualization
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_yticklabels(popular_titles, fontsize=12)  # Adjust fontsize as needed
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(fontsize=12)  # Adjust x-axis tick font size as needed
    plt.yticks(fontsize=12)
    plt.tight_layout(pad=3)
    plt.savefig("static/trending_plot.png")


@app.route("/")
def index():
    generate_trending_plot()
    return render_template("index.html", matches=[], show_plot=True)


@app.route("/search")
def search():
    query = request.args.get("query")
    search_method = request.args.get(
        "method", "tfi_df"
    )  # Default to "tfidf" if no method is provided
    matches = []
    if query:
        if search_method == "boolean":
            matches = boolean_search(query=query, scraped_data=scraped_data)
        else:
            matches = tf_idf(query=query, scraped_data=scraped_data)
        return render_template(
            "index.html", query=query.lower(), matches=matches, show_plot=False
        )


if __name__ == "__main__":
    app.run(debug=True)
