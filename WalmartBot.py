
#This will not run on online IDE 
import requests 
from bs4 import BeautifulSoup 
import json
from fakeUserAgent import generate_agent
class WalmartBot:
    def __init__(self):
        self.base_url =  "https://www.walmart.com/"
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
    def pull_data(self, query, pageNumber):
        page = 3
        scraper = self.make_request(f"search?q={query}&page={pageNumber}")
        product_titles =scraper.findAll('span', attrs = {"class":'normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy'})
        prices_whole_number =scraper.findAll('span', attrs = {"class":'f2'})
        prices_decimal_point =scraper.findAll('span', attrs = {"class":'f6 f5-l'})[1::2]
        product_link =scraper.findAll('a', attrs = {"class":'absolute w-100 h-100 z-1 hide-sibling-opacity'})
        json = {
            "products": []
        }
        for product, price_whole, price_decimal, link in zip(product_titles, prices_whole_number, prices_decimal_point, product_link):
            full_price = f"${price_whole.text}.{price_decimal.text}"
            full_link = f"https://www.walmart.com/{link['href']}"
            monthly_payment = "/month" in full_price
            data = {
                "Product Title": product.text,
                "Product Price": full_price,
                "Product Link": full_link,
                "monthly_payment": monthly_payment
            }
            json["products"].append(data)
        return json
    def scrape_pages(self, query,pageTotal):
        page = 1
        if pageTotal > 10: pageTotal = 10
        json = {
            "All Products": []
        }
        while page <= pageTotal:
            pageData = {
                f"Page {page}": [self.pull_data(query, page)]
            }
            json["All Products"].append(pageData)
            page +=1
        return json
