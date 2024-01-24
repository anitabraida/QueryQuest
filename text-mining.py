from bs4 import BeautifulSoup
import requests

list_of_urls = ['https://tyopaikat.oikotie.fi/tyopaikat/helsinki']

scraped_data = []

for url in list_of_urls:
    ## Send Request
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_titles = soup.select('h2')
        
        for title in job_titles:
            job_title = title.text.strip()
            job_title = job_title.split(",", 1)[0]
            scraped_data.append(job_title)  # Extract text content and strip any leading/trailing whitespaces


        ## Add To Data Output

for title in scraped_data:
    print(title)
