import json
from sklearn.feature_extraction.text import CountVectorizer

def boolean_search(file_path):
    d = {"and": "&", "AND": "&",
         "or": "|", "OR": "|",
         "not": "1 -", "NOT": "1 -",
         "(": "(", ")": ")"}          # operator replacements

    def rewrite_token(t):
        return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))

    def rewrite_query(query): # rewrite every token in the query
        return " ".join(rewrite_token(t) for t in query.split())

    with open(file_path, 'r', encoding='utf-8') as file:
        scraped_data = json.load(file)

    titles = [data['title'] for data in scraped_data]
    descriptions = [data['description'] for data in scraped_data]

    cv_title = CountVectorizer(lowercase=True, binary=True)
    cv_description = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix_title = cv.fit_transform(title)
    sparse_matrix_description = cv.fit_transform(description)
    dense_matrix_title = sparse_matrix_title.todense()
    dense_matrix_description = sparse_matrix_description.todense()
    td_matrix = dense_matrix.T
    t2i = cv.vocabulary_ 

    while True:
        query = input("Please enter your query here or hit enter to break: ")
        if query == "":    
            break    

        try:
            hits_matrix = eval(rewrite_query(query))
        except KeyError as e:
            print(f"Unknown term: {e}")
            continue    
        hits_list = list(hits_matrix.nonzero()[1])
        for i, doc_idx in enumerate(hits_list):
            print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))
            if i > 5:
                break

boolean_search('data copy.json')