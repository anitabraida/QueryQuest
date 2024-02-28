import json
from sklearn.feature_extraction.text import CountVectorizer

def boolean_search(file_path):
    d = {"and": "&", "AND": "&",
         "or": "|", "OR": "|",
         "not": "1 -", "NOT": "1 -",
         "(": "(", ")": ")"}          # operator replacements

    def rewrite_token(t):
        if t in t2i_title:
            return d.get(t, 'td_matrix_title[t2i_title["{:s}"]]'.format(t))
        elif t in t2i_description:
            return d.get(t, 'td_matrix_description[t2i_description["{:s}"]]'.format(t))
        else:
            return ""

    def rewrite_query(query): # rewrite every token in the query
        try:
            return " ".join(rewrite_token(t) for t in query.split())
        except TypeError as e:
            print(f"An error occurred: {e}")
            return ""  # or any other default value you prefer

    with open(file_path, 'r', encoding='utf-8') as file:
        scraped_data = json.load(file)
   

    titles = [data['title'] for data in scraped_data]
    links = [data['link'] for data in scraped_data]
    descriptions = [data['description'] for data in scraped_data]

    cv_title = CountVectorizer(lowercase=True, binary=True)
    cv_description = CountVectorizer(lowercase=True, binary=True)

    sparse_matrix_title = cv_title.fit_transform(titles)
    sparse_matrix_description = cv_description.fit_transform(descriptions)

    dense_matrix_title = sparse_matrix_title.todense()
    dense_matrix_description = sparse_matrix_description.todense()

    td_matrix_description = dense_matrix_description.T
    td_matrix_title = dense_matrix_title.T

    t2i_title = cv_title.vocabulary_ 
    t2i_description = cv_description.vocabulary_

    while True:
        query = input("Please enter your query here or hit enter to break: ")
        if query == "":    
            break    

        try:
            hits_matrix = eval(rewrite_query(query))
        except Exception as e:
            print(f"Unknown term: {query}")
            continue    
        hits_list = list(hits_matrix.nonzero()[1])
        for i, doc_idx in enumerate(hits_list):
            print("Matching doc #{:d}: Title: {:s}, Link: {:s}, Description: {:.100s}...".format(i, titles[doc_idx], links[doc_idx], descriptions[doc_idx]))
            if i > 5:
                break

boolean_search('data.json')