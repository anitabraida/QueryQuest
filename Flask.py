from flask import Flask, render_template, request
from text_mining import scrape_job_titles

app = Flask(__name__, static_url_path="", static_folder="static")

# URL to scrape job titles from
list_of_urls = ['https://tyopaikat.oikotie.fi/tyopaikat/helsinki']

# Scraping job titles from the specified URL
data = []
for url in list_of_urls:
    data.extend(scrape_job_titles(url))


@app.route('/')
def index():
    return render_template('index.html', matches=[])


@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Filter job titles based on the query
        matches = [title for title in data if query.lower() in title.lower()]
    else:
        matches = []
    return render_template('index.html', matches=matches)


if __name__ == '__main__':
    app.run(debug=True)
