import requests 
import json
from bs4 import BeautifulSoup 
from fakeUserAgent import generate_agent, random_proxy

class RocketHomesBot:
    def __init__(self):
        self.base_url = "https://www.rockethomes.com/"
    def make_request(self, searchQuery):
        link =f"{self.base_url}{searchQuery}"
        proxies = {
            'http': '103.1.93.184'
        }
        Headers = ({'User-Agent': generate_agent()})
        response = requests.get(link, headers=Headers, proxies=proxies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')
            return soup
        else:
            json = {
                "Error Message": f"Failed to Pull Data From {link}, return responce code of {response.status_code}"
            }
            return json
    def pull_house_data(self, state, city, pageNumber):
        scraper = self.make_request(f"{state}/{city}?page={pageNumber}")
        house_prices =scraper.findAll('p', attrs = {"data-testid":'list-price'})
        addresses =scraper.findAll('p', attrs = {"data-testid":'address'})
        property_size =scraper.findAll('p', attrs = {"data-testid":'property-size'})
        beds =scraper.findAll('p', attrs = {"data-testid":'beds'})
        baths =scraper.findAll('p', attrs = {"data-testid":'baths'})
        property_image =scraper.find_all('img', attrs = {"style":'height:264px'})
        property_links = scraper.findAll('a', attrs={"style":"height:264px"})
        propertyData = []
        for price, address, size, bed, bath, image, link in zip(house_prices, addresses, property_size, beds, baths, property_image, property_links):
            if image == property_image[0]:
                image_data = image['src']
            else:
                image_data = image['data-src']
            if len(bath.text) > 1:
                bath_data = bath.text
            else:
                bath_data = f"{bath.text}ba"
            data = {
                "Address": address.text,
                "Property Price": price.text,
                "Square Feet": size.text,
                "Bedrooms": f"{bed.text}bd",
                "Bathrooms": bath_data,
                "Property Photo": image_data, 
                "Property Link": self.base_url+ link["href"]
            }
            propertyData.append(data)
        return propertyData
rocket = RocketHomesBot()

print(rocket.pull_house_data("ma", "walpole", 1))