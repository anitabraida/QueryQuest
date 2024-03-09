from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
from nltk.metrics import edit_distance

# from text_mining import scrape_websites


def tf_idf_return():
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.joblib")
    tfidf_matrix = joblib.load("tfidf_matrix.joblib")
    return tfidf_matrix, tfidf_vectorizer


def get_matches(scraped_data, query, try_switch):
    
    tfidf_matrix, tfidf_vectorizer = tf_idf_return()
    tfidf_vector = tfidf_vectorizer.transform([query])
    cosine_similarities = cosine_similarity(tfidf_vector, tfidf_matrix)

    sorted_indices = np.argsort(cosine_similarities[0])[::-1]

    matches = []
    for i, doc_idx in enumerate(sorted_indices):
        if cosine_similarities[0][doc_idx] == 0:
            break
        matches.append(
            (
                scraped_data[doc_idx]["title"],
                scraped_data[doc_idx]["link"],
                scraped_data[doc_idx]["description"],
            )
        )
    statement = ""
    if len(matches) == 0 and try_switch == False:
        new_query, try_switch = get_closest_word(scraped_data, query, try_switch)
        if new_query != query:
            matches, statement = get_matches(scraped_data, new_query, try_switch)
            statement = "No results for \"{}\", showing results for \"{}\"".format(query, new_query)
            
    return matches, statement

def get_closest_word(data, query, try_switch):
    
    try_switch = True
    title_list = []
    for i in range(len(data)):
        title = data[i]["title"]
        title_list.append(title)
    title_list = [word for sentence in title_list for word in sentence.split()]

    distances = [(word, edit_distance(query, word)) for word in title_list]
    min_distance = min(distances, key=lambda x: x[1])[1]
    
    if min_distance <= 2:
        closest_words = [word for word, distance in distances if distance == min_distance]
        query = closest_words[0]
        
    
    return query, try_switch