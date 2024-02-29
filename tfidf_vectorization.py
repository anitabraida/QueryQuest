from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.stem import PorterStemmer
import joblib
import json

def tf_idf(scraped_data, save_to_file=True):
    stemmer = PorterStemmer()

    documents = [(data["title"], data["description"]) for data in scraped_data]

    stemmed_documents = []
    
    for title, description in documents:  # Access title and description separately
        tokens = nltk.word_tokenize(description)  # Tokenize only the description
        tokens.extend(nltk.word_tokenize(title))
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        stemmed_document = " ".join(stemmed_tokens)
        stemmed_documents.append(stemmed_document)
  
    tfidf_vectorizer = TfidfVectorizer(lowercase=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(stemmed_documents)

    joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
    joblib.dump(tfidf_matrix, 'tfidf_matrix.joblib')




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

tf_idf(scraped_data=scraped_data)
    