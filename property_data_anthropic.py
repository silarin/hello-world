import requests
from bs4 import BeautifulSoup
import time

# URL of the webpage you want to scrape
url = "https://www.propertyguru.com.sg/property-for-sale?market=residential&listing_type=sale&search=true"

# Rate limiting parameters
requests_per_minute = 30  # Maximum number of requests per minute
wait_time = 60 / requests_per_minute  # Time to wait between requests in seconds

# Send a request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the elements containing property prices and floor space data
property_listings = soup.find_all("div", class_="listing-item")

# Loop through each property listing and extract the data
for listing in property_listings:
    # Extract property price
    price_element = listing.find("span", class_="price")
    if price_element:
        property_price = price_element.text.strip()
    else:
        property_price = "N/A"
    
    # Extract floor space
    floor_space_element = listing.find("span", class_="floor-area")
    if floor_space_element:
        floor_space = floor_space_element.text.strip()
    else:
        floor_space = "N/A"
    
    # Print the extracted data
    print(f"Price: {property_price}, Floor Space: {floor_space}")
    
    # Wait for the specified time before making the next request
    time.sleep(wait_time)
