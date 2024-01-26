while True:
    query = input("Please enter your query here: ")
    if query == "?":
        break
    print(query)

with open('enwiki-20181001-corpus.100-articles.txt', 'r') as file:
    texts = file.read()

documents = texts.split('</article>')
