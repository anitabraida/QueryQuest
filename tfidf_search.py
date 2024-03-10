from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import joblib
from nltk.metrics import edit_distance
from nltk.stem.snowball import SnowballStemmer


# from text_mining import scrape_websites




def get_matches(scraped_data, query, try_switch):
    docs = [f"{data['title']} {data['description']}" for data in scraped_data]

    original_query = query
    
  
    if "\"" not in query:
        query, docs = stem_docs(query, docs)
        
    else:
        query = query.replace('"', '')
        
        
        original_query = query
    
    
    
    tfidf_vectorizer = TfidfVectorizer(lowercase=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs)
    
    
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
        new_query, try_switch = get_closest_word(scraped_data, original_query, try_switch)
        if new_query != original_query:
            matches, statement = get_matches(scraped_data, new_query, try_switch)
            statement = "No results for \"{}\", showing results for \"{}\"".format(original_query, new_query)
            
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


def stem_docs(query, documents):
    stemmer = SnowballStemmer("finnish")
    query = query.lower().split()
    stemmed_tokens = [stemmer.stem(token) for token in query]
    
    query_stemmed = ' '.join(stemmed_tokens)


    docs_stemmed = []
    for sentence in documents:
        sentence = sentence.lower().split()
        #print(sentence)
        stemmed_sentence = [stemmer.stem(word) for word in sentence]
        stemmed_sentence = ' '.join(stemmed_sentence)
        docs_stemmed.append(stemmed_sentence)

    
    
    return query_stemmed, docs_stemmed