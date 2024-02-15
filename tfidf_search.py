from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from text_mining import scrape_websites

#def rewrite_token(t):
#    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))

#def rewrite_query(query): # rewrite every token in the query
#    return " ".join(rewrite_token(t) for t in query.split())

 
#with open('enwiki-20181001-corpus.100-articles.txt', 'r') as file:
#    texts = file.read()

#documents = texts.split('</article>')



def tf_idf(query, scraped_data):
    stemmer = PorterStemmer()

    #scraped_data = scrape_websites()
    documents = [data['title'] for data in scraped_data]

    stemmed_documents = []
    for document in documents:
        tokens = nltk.word_tokenize(document)
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        stemmed_document = " ".join(stemmed_tokens)
        stemmed_documents.append(stemmed_document)

              
    querylen = len(query.split(" "))

        

    tfidf_vectorizer = TfidfVectorizer(ngram_range=(querylen, querylen), lowercase=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(stemmed_documents)    
        
        #I don't think this is used anywhere after
        #t2i = tfidf_vectorizer.vocabulary_
        #i2t = {i: t for t, i in t2i.items()}
  
    query_vector = tfidf_vectorizer.transform([query])

    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)

        # Sort the documents based on similarity
    sorted_indices = np.argsort(cosine_similarities[0])[::-1]
        # Print the top matching documents
        
    matches = []
    for i, doc_idx in enumerate(sorted_indices):
        if cosine_similarities[0][doc_idx] == 0:
            break
            
        matches.append((scraped_data[doc_idx]['title'], scraped_data[doc_idx]['link']))
        #print("Matching doc #{:d}: {:s}... (Cosine Similarity: {:.4f})".format(i, documents[doc_idx][:100], cosine_similarities[0][doc_idx]))
        #if i >= 5:
        #    break
    return matches