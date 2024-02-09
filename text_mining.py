from bs4 import BeautifulSoup
import requests

def scrape_job_titles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_titles = soup.find_all(attrs={"data-e2e-component": "job-ad-list-item"})
        
        scraped_data = []
        for title in job_titles:
            job_title = title.text.strip().split(",", 1)[0]
            scraped_data.append(job_title)
            
        return scraped_data
    else:
        print("Failed to fetch data from URL:", url)
        return []

list_of_urls = ['https://tyopaikat.oikotie.fi/tyopaikat/helsinki']

for url in list_of_urls:
    job_titles = scrape_job_titles(url)
    for title in job_titles:
        print(title)

print("What are these? These are job titles in Helsinki from oikotie.fi")
