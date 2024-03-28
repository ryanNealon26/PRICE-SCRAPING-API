import requests 
import json
from bs4 import BeautifulSoup 
from fakeUserAgent import generate_agent

class TruliaBot:
    def __init__(self):
        self.base_url = "https://www.trulia.com"
    def make_request(self, searchQuery):
        link =f"{self.base_url}{searchQuery}"
        Headers = ({'User-Agent': generate_agent()})
        response = requests.get(link, headers=Headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')
            return soup
        else:
            json = {
                "Error Message": f"Failed to Pull Data From {link}, return responce code of {response.status_code}"
            }
            return json
    def pull_house_data(self, state, city):
        scraper = self.make_request(f"/{state}/{city}/")
        prices =scraper.findAll('div', attrs = {"data-testid":'property-price'})
        addresses=scraper.findAll('div', attrs = {"data-testid":'property-address'})
        beds = scraper.findAll('div', attrs = {"data-testid":'property-beds'})
        baths = scraper.findAll('div', attrs = {"data-testid":'property-baths'})
        sqrft = scraper.findAll('div', attrs = {"data-testid":'property-floorSpace'})
        links = scraper.findAll('a', attrs = {"class":'Anchor__StyledAnchor-sc-3c3ff02e-1 doURDx'})
        json = {
            "Data": []
        }
        list_link = []
        for link in links:
            if link['href'].find("/home") != -1:
                list_link.append(f"{self.base_url}{link['href']}")
        for address, price, bed, bath, sq, link in zip(addresses, prices, beds, baths, sqrft, list_link):
            data = {
                "Address": address.text,
                "Property Price": price.text,
                "Property Beds": bed.text,
                "Property Baths": bath.text,
                "Property Sqrft": sq.text,
                "Property Link": link
            }
            json["Data"].append(data)
        return json    
