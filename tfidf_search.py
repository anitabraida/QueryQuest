from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
# from text_mining import scrape_websites


def tf_idf_return():
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.joblib")
    tfidf_matrix = joblib.load("tfidf_matrix.joblib")
    return tfidf_matrix, tfidf_vectorizer


def get_matches(tfidf_matrix, tfidf_vector, scraped_data):
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
        matches.append((scraped_data[doc_idx]["title"], scraped_data[doc_idx]["link"]))
    return matches
