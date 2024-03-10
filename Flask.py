from flask import Flask, render_template, request, jsonify
from tfidf_search import get_matches
import matplotlib as mlp
import os
from matplotlib import pyplot as plt
import json
from boolean_search import boolean_search
import matplotlib.ticker as ticker
from fuzzy_search import fuzzy_search
import spacy
import re

# clear the static folder of any remaining plots
os.system("rm -f static/*.png")

app = Flask(__name__)

nlp_finnish = spacy.load("fi_core_news_sm")
nlp_english = spacy.load("en_core_web_sm")

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

# create plot that displays trending titles with NER

regex_pattern = r".* oy\b"


def generate_trending_plot():
    fig, ax = plt.subplots(figsize=(10, 5))

    custom_stop_words = [
        "Helsinki",
        "Leijona Catering",
        "korko-",
        "HUSin",
        "lle",
        "Tähti",
    ]

    # get popular titles using NER
    job_title_frequencies = {}
    for data in scraped_data:
        if data["title"]:
            doc_finnish = nlp_finnish(data["title"])
            doc_english = nlp_english(data["title"])

            for entity in doc_finnish.ents:
                if (
                    entity.label_ not in ["CARDINAL", "GPE", "LOC"]
                    and not entity.text.isdigit()
                    and entity.text not in custom_stop_words
                    and not re.match(regex_pattern, entity.text, re.IGNORECASE)
                ):
                    job_title = entity.text
                    job_title_frequencies[job_title] = (
                        job_title_frequencies.get(job_title, 0) + 1
                    )

            for entity in doc_english.ents:
                if (
                    entity.label_ not in ["CARDINAL", "GPE", "LOC"]
                    and not entity.text.isdigit()
                    and entity.text not in custom_stop_words
                    and not re.match(regex_pattern, entity.text, re.IGNORECASE)
                ):
                    job_title = entity.text
                    job_title_frequencies[job_title] = (
                        job_title_frequencies.get(job_title, 0) + 1
                    )

    popular_job_titles = sorted(
        job_title_frequencies.items(), key=lambda x: x[1], reverse=True
    )[:5]
    popular_titles, frequencies = zip(*popular_job_titles)
    ax.barh(popular_titles, frequencies, color="skyblue", height=0.6)

    ax.set_xlabel("Frequency", fontsize=14)
    ax.set_yticklabels(popular_titles, fontsize=14)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout(pad=3)
    plt.savefig("static/trending_plot.png")


@app.route("/")
def index():
    generate_trending_plot()
    return render_template("index.html", matches=[], show_plot=True)


@app.route("/search")
def search():
    return render_template(
        "index.html",
        show_plot=False,
    )


@app.route("/trending")
def trending():
    generate_trending_plot()
    return render_template("trending.html", matches=[], show_plot=True)


@app.route("/search-json")
def search_json():
    query = request.args.get("query")
    search_method = request.args.get(
        "method", "tfi_df"
    )  # Default to "tfidf" if no method is provided
    # matches = []
    statement = ""
    if query:
        if search_method == "boolean":
            matches, statement = boolean_search(
                query=query, scraped_data=scraped_data, try_switch=False
            )
        elif search_method == "fuzzy":
            matches = fuzzy_search(query=query, scraped_data=scraped_data)
        else:
            matches, statement = get_matches(
                scraped_data=scraped_data, query=query, try_switch=False
            )
        matches_as_dict_list = [
            dict(zip(["title", "link", "description"], values)) for values in matches
        ]
    else:
        matches_as_dict_list = scraped_data[-15:]

    response_data = {"matches": matches_as_dict_list, "statement": statement}
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
