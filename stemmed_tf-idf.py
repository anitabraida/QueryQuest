from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from text_mining import scrape_job_titles


def rewrite_token(t):
    stemmed_token = stemmer.stem(t)
    return stemmed_token

def rewrite_query(query):
    tokens = nltk.word_tokenize(query)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return " ".join(rewrite_token(t) for t in stemmed_tokens)

# URL to scrape job titles from
list_of_urls = ['https://tyopaikat.oikotie.fi/tyopaikat/helsinki']

# Scraping job titles from the specified URL
data = []
for url in list_of_urls:
    data.extend(scrape_job_titles(url))

stemmer = PorterStemmer()

documents = data
stemmed_documents = []
for document in documents:
    tokens = nltk.word_tokenize(document)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    stemmed_document = " ".join(stemmed_tokens)
    stemmed_documents.append(stemmed_document)

tfidf_vectorizer = TfidfVectorizer(lowercase=True)

tfidf_matrix = tfidf_vectorizer.fit_transform(stemmed_documents)


t2i = tfidf_vectorizer.vocabulary_
i2t = {i: t for t, i in t2i.items()}


while True:
    stemmed_terms = []

    query = input("Please enter your query here or hit enter to break: ")
    if query == "":    
        break    

    # Rewrite the query with stemming
    rewritten_query = rewrite_query(query)
    print(rewritten_query)
    
    query_vector = tfidf_vectorizer.transform([rewritten_query])

    # Compute cosine similarity between query and documents
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

    # Sort the documents based on similarity
    sorted_indices = np.argsort(cosine_similarities[0])[::-1]

    # Print the top matching documents
    for i, doc_idx in enumerate(sorted_indices):
        print("Matching doc #{:d}: {} (Cosine Similarity: {:.4f})".format(i, documents[doc_idx], cosine_similarities[0][doc_idx]))
        if i >= 5:
            break
