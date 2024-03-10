# Job Search

This is a search engine for job listings. With our Job Search, you can search jobs from multiple websites at the same time. In addition, you can use three different types of search methods. The default search is based on TF-IDF vectors, and it finds the most similar job titles and descriptions to the query using cosine similarity. The boolean search allows to use logical operators "and", "or" and "not". Note that the "not" operator needs to be typed as "and not". Lastly, the Fuzzy search allows for non-exact matches, such as different spelling. You can select your preferred search method by ticking the box, and it is also possible to select multiple search methods at the same time.

Matches are based on job titles and descriptions. You can click on the job title to open the description to the right, and click on the link to open the corresponding job listing in its original website. Currently the job search retrieves job listings based in Helsinki from Oikotie and Duunitori.

In addition, our website displays a plot of currectly trending job titles using Named Entity Recognition when you click on the "What's trending" button. 

To start the flask application, run the following commands:

```bash
python3 -m venv venv
```
```bash
. venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
python -m spacy download en_core_web_sm
python -m spacy download fi_core_news_sm
```
```bash
export FLASK_APP=Flask.py      
export FLASK_DEBUG=True
export FLASK_RUN_PORT=8000
```
```bash
flask run
```
