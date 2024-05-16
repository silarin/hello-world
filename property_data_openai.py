import requests
from bs4 import BeautifulSoup
import time

# URL of the PropertyGuru page you want to scrape
url = 'https://www.propertyguru.com.sg/property-for-sale'

# Function to get the HTML content of a page
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Function to scrape property data from a page
def scrape_properties(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    listings = soup.find_all('div', class_='listing-card')

    for listing in listings:
        price_tag = listing.find('span', class_='price')
        price = price_tag.get_text(strip=True) if price_tag else 'N/A'

        floor_space_tag = listing.find('span', class_='floor-area')
        floor_space = floor_space_tag.get_text(strip=True) if floor_space_tag else 'N/A'

        print(f'Price: {price}, Floor Space: {floor_space}')

# Fetch the initial page
page_content = fetch_page(url)
if page_content:
    scrape_properties(page_content)

    # Introduce a delay between requests
    time.sleep(5)  # 5 seconds delay

    # Fetch additional pages if needed
    # Example: if the website has pagination
    next_page_url = 'https://www.propertyguru.com.sg/property-for-sale?page=2'
    next_page_content = fetch_page(next_page_url)
    if next_page_content:
        scrape_properties(next_page_content)