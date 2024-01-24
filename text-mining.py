from bs4 import BeautifulSoup
import requests

list_of_urls = ['https://tyopaikat.oikotie.fi/tyopaikat/helsinki']

scraped_data = []

for url in list_of_urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_titles = soup.find_all(attrs={"data-e2e-component": "job-ad-list-item"})
        
        for title in job_titles:
            scraped_data.append(title.text.strip())

for title in scraped_data:
    print(title)

print("What are these? These are job titles in Helsinki from oikotie.fi")