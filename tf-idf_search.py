from sklearn.feature_extraction.text import CountVectorizer

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

 
with open('enwiki-20181001-corpus.100-articles.txt', 'r') as file:
    texts = file.read()

documents = texts.split('</article>')

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)
dense_matrix = sparse_matrix.todense()
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
        print("Matching doc #{:d}: {:s}...".format(i, documents[doc_idx][:100]))
        if i > 5:
            break