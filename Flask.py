from flask import Flask, render_template, request
from text-mining import scrape_job_titles

#Initialize Flask instance
app = Flask(__name__)

list_of_urls = ['https://tyopaikat.oikotie.fi/tyopaikat/helsinki']

for url in list_of_urls:
    data = job_titles = scrape_job_titles(url)

@app.route('/')
def hello_world():
   return "Hello, World!"

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        #Look at each entry in the example data
        for entry in data:
            #If an entry name contains the query, add the entry to matches
            if query.lower() in entry['name'].lower():
                matches.append(entry)

    #Render index.html with matches variable
    return render_template('index.html', matches=matches)