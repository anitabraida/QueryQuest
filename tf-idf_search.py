from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

 
with open('enwiki-20181001-corpus.100-articles.txt', 'r') as file:
    texts = file.read()

documents = texts.split('</article>')

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(lowercase=True)

# Fit and transform the documents
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

# Get the vocabulary and inverse vocabulary
t2i = tfidf_vectorizer.vocabulary_
i2t = {i: t for t, i in t2i.items()}

while True:
    query = input("Please enter your query here or hit enter to break: ")
    if query == "":    
        break    
    
    query_vector = tfidf_vectorizer.transform([query])

    # Compute cosine similarity between query and documents
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

    # Sort the documents based on similarity
    sorted_indices = np.argsort(cosine_similarities[0])[::-1]

    # Print the top matching documents
    for i, doc_idx in enumerate(sorted_indices):
        print("Matching doc #{:d}: {:s}... (Cosine Similarity: {:.4f})".format(i, documents[doc_idx][:100], cosine_similarities[0][doc_idx]))
        if i >= 5:
            break
            