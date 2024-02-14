from bs4 import BeautifulSoup
import requests

def scrape_oikotie(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Scraping job titles
        job_titles = soup.find_all(attrs={"data-e2e-component": "job-ad-list-item"})
        scraped_data = []
        for title in job_titles:
            job_title = title.text.strip().split(",", 1)[0]
            # Scraping links
            link_tag = title.find_previous('a')
            if link_tag and 'href' in link_tag.attrs:
                link = 'https://tyopaikat.oikotie.fi' + link_tag['href']

                scraped_data.append({'title': job_title, 'link': link})  # Append both title and link
        
        return scraped_data
    else:
        print("Failed to fetch the page.")
        return []


def scrape_duunitori(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Scraping job titles
        job_titles = soup.find_all('h3', class_='job-box__title')
        scraped_data = []
        for title in job_titles:
            job_title = title.text.strip().split(",", 1)[0]
            # Scraping links
            link_tag = title.find_previous('a')
            if link_tag and 'href' in link_tag.attrs:
                link = 'https://duunitori.fi' + link_tag['href']

                scraped_data.append({'title': job_title, 'link': link})

        return scraped_data
    else:
        print("Failed to fetch data from URL:", url)
        return []


def scrape_websites():
    data = []
    data.extend(scrape_oikotie('https://tyopaikat.oikotie.fi/tyopaikat/helsinki'))
    data.extend(scrape_duunitori('https://duunitori.fi/tyopaikat/alue/helsinki'))

    return data

    #for i in data:
     #   print("Title:", title['title'])
      #  print("Link:", title['link'])
       # print() 

scrape_websites()
