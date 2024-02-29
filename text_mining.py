from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import urllib3
import re
import time
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()




def scrape_oikotie(url):
   max_clicks = 10
   scraped_data = []
   try:
       driver.get(url)
       for _ in range(max_clicks):
           try:
               load_more_button = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/main/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[1]/button/span[1]'))
               )
               load_more_button.click()
               WebDriverWait(driver, 10).until(
                   EC.invisibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/main/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[1]/button/span[1]'))
               )
           except Exception as e:
               print(f"Failed to click 'Load More' button: {str(e)}")
               break 


       soup = BeautifulSoup(driver.page_source, 'html.parser')
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
   finally:
       driver.quit()
   scraped_data = [dict(s) for s in set(frozenset(d.items()) for d in scraped_data)]
   return scraped_data
  
  
def scrape_duunitori(url):
   i = 0
   scraped_data = []
   while i < 10:
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
   with open("data.json", "w", encoding="utf-8") as file:
       json.dump(data, file, ensure_ascii=False, indent=2)


scrape_websites()
