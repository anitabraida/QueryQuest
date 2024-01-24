from bs4 import BeautifulSoup
import requests

list_of_urls = [
    'https://tyopaikat.oikotie.fi/tyopaikat/helsinki',
        ]

scraped_data = []

## Scraping Function
def start_scrape():
    
    ## Loop Through List of URLs
    for url in list_of_urls:
        
        ## Send Request
        response = requests.get(url)
        
        if response.status_code == 200:
            
            ## Parse Data
            print(response.text)

            ## Add To Data Output
        
        pass