import requests
from bs4 import BeautifulSoup

# Step 1: Download the Web Page
url = "https://tyopaikat.oikotie.fi/tyopaikat/helsinki"
response = requests.get(url)
html_content = response.text

# Step 2: Extract Plain Text with Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')
plain_text = soup.get_text()

# Step 3: Print Some of the Text
print("First 500 characters of the extracted text:")
print(plain_text[:500])  # Print the first 500 characters as an example