import json
from sklearn.feature_extraction.text import CountVectorizer
from tfidf_search import get_closest_word

def boolean_search(scraped_data, query, try_switch):
    d = {
        "and": "&",
        "AND": "&",
        "or": "|",
        "OR": "|",
        "not": "1 -",
        "NOT": "1 -",
        "(": "(",
        ")": ")",
    }  # operator replacements

    query = query.lower()


    def rewrite_token(t):
        try:
            return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))
        
        except KeyError as e:
            print(f"An error occurred: {e}")
            return ""


    def rewrite_query(query):  # rewrite every token in the query
        try:
            return " ".join(rewrite_token(t) for t in query.split())
        except KeyError as e:
            print(f"An error occurred: {e}")
            return "" 


    titles = [data["title"] for data in scraped_data]
    links = [data["link"] for data in scraped_data]
    descriptions = [data["description"] for data in scraped_data]
    
    docs = [f"{data['title']} {data['description']}" for data in scraped_data]

    cv = CountVectorizer(lowercase=True, binary=True)

    sparse_matrix = cv.fit_transform(docs)

    dense_matrix = sparse_matrix.todense()

    td_matrix = dense_matrix.T

    t2i = cv.vocabulary_
    
    rewritten_query = rewrite_query(query)

    try:
        hits_matrix = eval(rewritten_query)
        hits_list = list(hits_matrix.nonzero()[1])
    except Exception as e:
        hits_list = []
        
        
    
    print(hits_list)
    matches = []
    for element in hits_list:
        matches.append((titles[element], links[element], descriptions[element]))
    statement = ""
    if len(matches) == 0 and try_switch == False:
        new_query, try_switch = get_closest_word(scraped_data, query, try_switch)
        if new_query != query:
            matches, statement = boolean_search(scraped_data, new_query, try_switch)
            statement = "No results for \"{}\", showing results for \"{}\"".format(query, new_query)
            
    return matches, statement
    