#  Install the Python Requests library:
# `pip install requests`
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('SCRAPINGBEE_API_KEY')

def send_request():
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1',
        params={
            'api_key': api_key,
            'url': 'https://www.zillow.com/cleveland-oh/',
            'render_js': 'true'
        },
    )
    print('Response HTTP Status Code: ', response.status_code)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all property card data wrappers using the exact class name
        property_cards = soup.find_all('div', class_='StyledPropertyCardDataWrapper-c11n-8-107-0__sc-hfbvv9-0')
        
        print(f"Found {len(property_cards)} properties")
        
        for card in property_cards:
            try:
                # Price - using the exact class and data-test attribute
                price_element = card.find('span', {'data-test': 'property-card-price'})
                price = price_element.text.strip() if price_element else "Price not found"
                
                # Address - using the exact data-test attribute
                address_element = card.find('address', {'data-test': 'property-card-addr'})
                address = address_element.text.strip() if address_element else "Address not found"
                
                # Property details (beds, baths, sqft)
                details_element = card.find('ul', class_='StyledPropertyCardHomeDetailsList-c11n-8-107-0__sc-1j0som5-0')
                beds = baths = sqft = "N/A"
                if details_element:
                    details = details_element.find_all('li')
                    for detail in details:
                        text = detail.text.strip()
                        if 'bd' in text:
                            beds = detail.find('b').text.strip()
                        elif 'ba' in text:
                            baths = detail.find('b').text.strip()
                        elif 'sqft' in text:
                            sqft = detail.find('b').text.strip()
                
                # Broker/Agent information
                broker_element = card.find('div', class_='StyledPropertyCardDataArea-c11n-8-107-0__sc-10i1r6-0 bziRDw')
                broker = broker_element.text.strip() if broker_element else "Broker not found"
                
                # Property type/status (e.g., "House for sale")
                status_container = details_element.parent if details_element else None
                status = status_container.text.split('-')[-1].strip() if status_container else "Status not found"
                
                # Print all information
                print(f"\nProperty Details:")
                print(f"Price: {price}")
                print(f"Address: {address}")
                print(f"Beds: {beds}")
                print(f"Baths: {baths}")
                print(f"Square Feet: {sqft}")
                print(f"Status: {status}")
                print(f"Broker: {broker}")
                print("-" * 50)
                
            except Exception as e:
                print(f"Error processing property card: {str(e)}")
                continue
    else:
        print('Failed to fetch data from Zillow')

if __name__ == "__main__":
    send_request()
  