from flask import Flask, render_template, request
from tfidf_search import tf_idf_return, get_matches
import matplotlib as mlp
import pke
import os
from matplotlib import pyplot as plt
from collections import defaultdict
import nltk
import json
from boolean_search import boolean_search

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


def extract_keyphrases(text):
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=text, language="fi")
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=5)  # Extract top 5 keyphrases
    return [keyphrase for keyphrase, score in keyphrases]


data_keyphrases = {
    post["title"]: extract_keyphrases(post["description"]) for post in scraped_data
}


frequencies = defaultdict(nltk.FreqDist)
for key in data_keyphrases:
    for keyphrase in data_keyphrases[key]:
        frequencies[key][keyphrase.lower()] += 1


def generate_trending_plot():
    fig, ax = plt.subplots()
    ax.set_title("Trending jobtitles")

    # get popular titles
    job_title_frequencies = {}
    for title in scraped_data:
        job_title = title["title"]
        job_title_frequencies[job_title] = job_title_frequencies.get(job_title, 0) + 1

    popular_job_titles = sorted(
        job_title_frequencies.items(), key=lambda x: x[1], reverse=True
    )[:10]
    popular_titles, frequencies = zip(*popular_job_titles)
    ax.barh(popular_titles, frequencies, color="skyblue")

    # Set labels and rotation for better visualization
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Job Titles")
    plt.tight_layout()
    plt.savefig("static/trending_plot.png")


@app.route("/")
def index():
    generate_trending_plot()
    return render_template("index.html", matches=[])

tfidf_matrix, tfidf_vectorizer = tf_idf_return()

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
            query_vector = tfidf_vectorizer.transform([query])
            matches = get_matches(tfidf_matrix=tfidf_matrix, tfidf_vector=query_vector, scraped_data=scraped_data)

        
        return render_template("index.html", query=query.lower(), matches=matches)


if __name__ == "__main__":
    app.run(debug=True)
