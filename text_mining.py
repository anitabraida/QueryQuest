from bs4 import BeautifulSoup
import requests

def scrape_oikotie(url):
    i = 0
    scraped_data = []
    while i < 50:
        if i == 0:
            URL = url
        else:
            URL= url + "?sivu=" + str(i)
        i += 1
        response = requests.get(URL)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Scraping job titles
            job_ads = soup.find_all('article', class_='job-ad-list-item')
        
            for job_ad in job_ads:
                title_tag = job_ad.find('h2', class_='title')
                if title_tag:
                    job_title = title_tag.text.strip()
                    link_tag = title_tag.find('a', href=True)
                    if link_tag:
                        link = 'https://tyopaikat.oikotie.fi' + link_tag['href']
                        # Get job description
                        description_response = requests.get(link)
                        if description_response.status_code == 200:
                            description_soup = BeautifulSoup(description_response.content, 'html.parser')
                            paragraphs = description_soup.find_all('p')
                            job_paragraphs = [p.text.strip() for p in paragraphs]
                            job_description = '\n'.join(job_paragraphs)    
                            scraped_data.append({'title': job_title, 'link': link, 'description': job_description})
        else:
            print("Failed to fetch data from URL:", url)
            return []
    scraped_data = [dict(s) for s in set(frozenset(d.items()) for d in scraped_data)]
    return scraped_data
    
    
def scrape_duunitori(url):
    i = 0
    scraped_data = []
    while i < 50:
        if i == 0:
            URL = url
        else:
            URL= url + "?sivu=" + str(i)
        i += 1
        response = requests.get(URL)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Scraping job titles
            job_titles = soup.find_all('h3', class_='job-box__title')
            #scraped_data = []
            for title in job_titles:
                job_title = title.text.strip().split(",", 1)[0]
                # Scraping links
                link_tag = title.find_previous('a')
                if link_tag and 'href' in link_tag.attrs:
                    link = 'https://duunitori.fi' + link_tag['href']
                    # Get job description
                description_response = requests.get(link)
                if description_response.status_code == 200:
                    description_soup = BeautifulSoup(description_response.content, 'html.parser')
                    description_div = description_soup.find('div', class_='description-box')
                    job_description = description_div.find('div', class_='description').text.strip()
                    scraped_data.append({'title': job_title, 'link': link, 'description': job_description})
        else:
            print("Failed to fetch data from URL:", url)
            return []
    scraped_data = [dict(s) for s in set(frozenset(d.items()) for d in scraped_data)]
    return scraped_data


def scrape_websites():
    data = []
    data.extend(scrape_oikotie('https://tyopaikat.oikotie.fi/tyopaikat/helsinki'))
    data.extend(scrape_duunitori('https://duunitori.fi/tyopaikat/alue/helsinki'))
    for job in data[:10]:
        print("Title:",job['title'])
        print("Description:", job['description'][:100],"...")
        print("Link:", job['link'])
        print()

    return data

scrape_websites()

# The first line of description is not present on the actual website, do we want to keep it?
