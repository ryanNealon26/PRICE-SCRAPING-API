import requests 
import json
from bs4 import BeautifulSoup 
from fakeUserAgent import generate_agent
from algorithms import mergeSort
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
        scraper = self.make_request(f"{state}/{city}?home-type=house&page={pageNumber}")
        house_prices =scraper.findAll('p', attrs = {"data-testid":'list-price'})
        addresses =scraper.findAll('p', attrs = {"data-testid":'address'})
        property_size =scraper.findAll('p', attrs = {"data-testid":'property-size'})
        beds =scraper.findAll('p', attrs = {"data-testid":'beds'})
        baths =scraper.findAll('p', attrs = {"data-testid":'baths'})
        property_image =scraper.find_all('img', attrs = {"style":'height:264px'})
        property_links = scraper.findAll('a', attrs={"style":"height:264px"})
        propertyData = []
        print(f"{len(addresses)} || {len(property_size)}")
        for price, address, size, bed, bath, image, link in zip(house_prices, addresses, property_size, beds, baths, property_image, property_links):
            if image == property_image[0]:
                image_data = image['src']
            else:
                image_data = image['data-src']
            if len(bath.text) > 1:
                bath_data = bath.text
            else:
                bath_data = f"{bath.text}ba"
            size_data = size.text
            if len(property_size) != len(addresses):
                size_data = "NA"
            data = {
                "Address": address.text,
                "Property Price": price.text,
                "Square Feet": size_data,
                "Bedrooms": f"{bed.text}bd",
                "Bathrooms": bath_data,
                "Property Photo": image_data, 
                "Property Link": self.base_url+ link["href"]
            }
            propertyData.append(data)
        return propertyData
    def scrape_pages(self, state, city, pages):
        pageNumber = 1
        scraper = self.make_request(f"{state}/{city}?page=1")
        json = {
            "Property Data": []
        }
        try:
            total_houses =scraper.findAll('span', attrs = {"id":'location-title-home-count'})
        except:
            total_houses =scraper.findAll('span', attrs = {"id":'location-listings-title-home-count'})
        for total in total_houses:
            total_data = int(total.text.replace(" results", "").replace(",", ""))
        if pages > total_data:
            pages = total_data
        if pages > 10: 
            pages = 10
        while pageNumber <= pages:
            housing_data = self.pull_house_data(state, city, pageNumber)
            for data in housing_data:
                json["Property Data"].append(data)
            pageNumber += 1
        mergeSort(json["Property Data"])
        return json
