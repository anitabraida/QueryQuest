from flask import Flask, render_template, request
from text_mining import scrape_websites
from tfidf_search import tf_idf

app = Flask(__name__, static_url_path="", static_folder="static")

# Scraping job listings
scraped_data = scrape_websites()


@app.route('/')
def index():
    return render_template('index.html', matches=[])


@app.route('/search')
def search():
    query = request.args.get('query')
    matches = []
    if query:
        # Filter job titles based on the query
        #for data in scraped_data:
        #    if query.lower() in data['title'].lower():
        #        matches.append((data['title'], data['link']))
        matches = tf_idf(query=query, scraped_data=scraped_data)
    if len(matches) == 0:
        return "No results found"
    else:
        return render_template('index.html', matches=matches)


if __name__ == '__main__':
    app.run(debug=True)
