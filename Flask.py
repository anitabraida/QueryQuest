from flask import Flask, render_template, request
from text_mining import scrape_websites
from tfidf_search import tf_idf
import matplotlib as mlp
import pke
import os
from matplotlib import pyplot as plt
from collections import defaultdict
import nltk


# clear the static folder of any remaining plots
os.system("rm -f static/*.png")


app = Flask(__name__)

# Scraping job listings
scraped_data = scrape_websites()

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


@app.route("/search")
def search():
    query = request.args.get("query")

    matches = []
    matches_keyphrases = {}
    if query:
        for post in scraped_data:
            if query.lower() in post["title"].lower():
                title = post["title"]
                keyphrases = extract_keyphrases(post["description"])
                matches_keyphrases[title] = keyphrases
        # Filter job titles based on the query
        # for data in scraped_data:
        #    if query.lower() in data['title'].lower():
        #        matches.append((data['title'], data['link']))
        matches = tf_idf(query=query, scraped_data=scraped_data)

        generate_query_plot(query, matches_keyphrases)
        return render_template("index.html", query=query.lower(), matches=matches)


if __name__ == "__main__":
    app.run(debug=True)
