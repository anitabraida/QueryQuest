from flask import Flask, render_template, request
from tfidf_search import tf_idf_return, get_matches
import matplotlib as mlp
import pke
import os
from matplotlib import pyplot as plt
from collections import defaultdict
import nltk
import json

# clear the static folder of any remaining plots
os.system("rm -f static/*.png")

# redoing commit

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

# use scraped_data, contains 'title' and 'description' and use these in the same way that
# the example uses the wikipedia data
# instead do theme extraction using pke and visualize it somehow


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


def generate_query_plot(query, matches_keyphrases):
    fig, ax = plt.subplots()
    ax.set_title(f"Keyphrase distribution per document \n query: {query}")

    # Create a dictionary to store the frequencies of keyphrases
    keyphrase_frequencies = defaultdict(int)

    # Iterate over each job title and its associated keyphrases
    for keyphrases in matches_keyphrases.values():
        for keyphrase in keyphrases:
            keyphrase_frequencies[keyphrase] += 1

    # Plot the keyphrase distribution
    ax.barh(
        list(keyphrase_frequencies.keys()),
        list(keyphrase_frequencies.values()),
        color="skyblue",
    )

    # Set labels and rotation for better visualization
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Keyphrases")

    plt.tight_layout()
    plt.savefig(f"static/query_{query}_plot.png")


@app.route("/")
def index():
    return render_template("index.html", matches=[])

tfidf_matrix, tfidf_vectorizer = tf_idf_return()

@app.route("/search")
def search():
    query = request.args.get("query")
    #matches = []
    matches_keyphrases = {}
    if query:
        for post in scraped_data:
            if query.lower() in post["title"].lower():
               keyphrases = extract_keyphrases(post["description"])
               matches_keyphrases["title"] = keyphrases
        #matches = tf_idf(query=query, scraped_data=scraped_data)
        query_vector = tfidf_vectorizer.transform([query])
        matches = get_matches(tfidf_matrix=tfidf_matrix, tfidf_vector=query_vector, scraped_data=scraped_data)
        generate_query_plot(query, matches_keyphrases)
        return render_template("index.html", query=query.lower(), matches=matches)


if __name__ == "__main__":
    app.run(debug=True)
