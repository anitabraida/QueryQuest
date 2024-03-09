import json
from sklearn.feature_extraction.text import CountVectorizer


def boolean_search(scraped_data, query):
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

    hits_matrix = eval(rewritten_query)
        
    hits_list = list(hits_matrix.nonzero()[1])
    print(hits_list)
    matches = []
    for element in hits_list:
        matches.append((titles[element], links[element], descriptions[element]))
       
    return matches