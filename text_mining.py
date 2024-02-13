from bs4 import BeautifulSoup
import requests

def scrape_oikotie(url):
    # Scrapes job titles from oikotie.fi website
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_titles = soup.find_all(
            attrs={"data-e2e-component": "job-ad-list-item"}
        )

        scraped_data = []
        for title in job_titles:
            job_title = title.text.strip().split(",", 1)[0]
            scraped_data.append(job_title)

        return scraped_data
    else:
        print("Failed to fetch data from URL:", url)
        return []

def scrape_duunitori(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_titles = soup.find_all('h3', class_='job-box__title')

        scraped_data = []
        for title in job_titles:
            job_title = title.text.strip().split(",", 1)[0]
            scraped_data.append(job_title)

        return scraped_data
    else:
        print("Failed to fetch data from URL:", url)
        return []

def scrape_job_titles():
    job_titles = []
   # job_titles.extend(scrape_oikotie('https://tyopaikat.oikotie.fi/tyopaikat/helsinki'))
    job_titles.extend(scrape_duunitori('https://duunitori.fi/tyopaikat/alue/helsinki'))

    for title in job_titles:
        print(title)     

scrape_job_titles()