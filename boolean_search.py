import json
from sklearn.feature_extraction.text import CountVectorizer

#with open('data.json', 'r', encoding='utf-8') as file:
#    scraped_data = json.load(file)

#query = input("Please enter your query here or hit enter to break: ")


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
            return ""  # or any other default value you prefer


    def rewrite_query(query):  # rewrite every token in the query
        try:
            return " ".join(rewrite_token(t) for t in query.split())
        except KeyError as e:
            print(f"An error occurred: {e}")
            return ""  # or any other default value you prefer

    titles = [data["title"] for data in scraped_data]
    links = [data["link"] for data in scraped_data]
    descriptions = [data["description"] for data in scraped_data]
    
    docs = [f"{data['title']} {data['description']}" for data in scraped_data]

    cv = CountVectorizer(lowercase=True, binary=True)

    sparse_matrix = cv.fit_transform(docs)

    dense_matrix = sparse_matrix.todense()

    td_matrix = dense_matrix.T

    t2i = cv.vocabulary_
    #print(t2i)
    
    rewritten_query = rewrite_query(query)
    print("Rewritten Query:", rewritten_query)
    print(type(rewritten_query))
    print(query)
    hits_matrix = eval(rewritten_query)
    print(hits_matrix)
    
    #print(f"Unknown Term: {query}")
        
    hits_list = list(hits_matrix.nonzero()[1])
    print(hits_list)
    matches = []
    for element in hits_list:
        matches.append((titles[element], links[element], descriptions[element]))
        
    
            #print("Matching doc #{:d}: Title: {:s}, Link: {:s}, Description: {:.100s}...".format(i, titles[doc_idx], links[doc_idx], descriptions[doc_idx]))
       
    return matches


#boolean_search(scraped_data, query)
