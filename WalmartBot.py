 
import requests 
from bs4 import BeautifulSoup 
from fakeUserAgent import generate_agent
from algorithms import quickSort
import re
class WalmartBot:
    def __init__(self):
        self.base_url =  "https://www.walmart.com/"
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
    def pull_data(self, query, pageNumber):
        scraper = self.make_request(f"search?q={query}&page={pageNumber}")
        product_titles =scraper.findAll('span', attrs = {"class":'normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy'})
        prices_whole_number =scraper.findAll('span', attrs = {"class":'f2'})
        prices_decimal_point =scraper.findAll('span', attrs = {"class":'f6 f5-l'})[1::2]
        product_link =scraper.find_all('a', class_= 'absolute w-100 h-100 z-1 hide-sibling-opacity')
        specials =scraper.find('div', attrs = {"data-testid":'sba-container'})      
        
        if specials == []:
            fixedLinks = product_link
        else:
            counter = re.findall("add to cart",str(specials))
            fixedLinks = product_link[len(counter):]
        product_images = scraper.find_all('img',  attrs = {"data-testid":'productTileImage'})
        product_list = []
        for product, price_whole, price_decimal, link, image in zip(product_titles, prices_whole_number, prices_decimal_point, fixedLinks, product_images):
            full_price = f"${price_whole.text}.{price_decimal.text}"            
            full_price = full_price.replace(",", "")
            if len(link['href']) < 200:
                full_link = f"https://www.walmart.com/{link['href']}"
            else: 
                full_link = link['href']
            monthly_payment = "/month" in full_price
            data = {
                "Product Title": product.text,
                "Product Price": full_price,
                "Product Link": full_link,
                "Image Link": image["src"],
                "monthly_payment": monthly_payment
            }
            product_list.append(data)
        return product_list
    def scrape_pages(self, query,pageTotal):
        page = 1
        if pageTotal > 10: pageTotal = 10
        json = {
            "Inventory": []
        }
        product_titles = []
        while page <= pageTotal:
            final_response = []
            response = self.pull_data(query, page)
            while response == []:
                response = self.pull_data(query, page)
            for responses in response:
                if responses["Product Title"] not in product_titles:
                    final_response.append(responses)
                    product_titles.append(responses["Product Title"])
            json["Inventory"].append(final_response)
            page +=1
        return json
    def merge_prep(self, productData, pageNumber):
        i = 0
        merge_prep = []
        products = productData["Inventory"]
        while i < pageNumber:
            j = 0
            page_list = products[i]
            while j < len(page_list):
                product = page_list[j]
                if not product["monthly_payment"]:
                        product["Product Price"] = product["Product Price"].replace("/undefined", "")
                        product["Product Price"] = float(product["Product Price"].replace(",", "")[1:])
                        merge_prep.append(product)
                j +=1
            i +=1
        return merge_prep
    def sorted_products(self, productData, pageNumber):
        productArray = self.merge_prep(productData, pageNumber) 
        length = len(productArray) - 1
        quickSort(productArray, 0, length)       
        for product in productArray:
            product["Product Price"] = f"${product['Product Price']}"
        json = {
            "Sorted Products": productArray
        }
        return json
    def product_reviews(self):
        url = "reviews/product/365828795"
        scraper = self.make_request(url)
        reviews  =scraper.findAll('h3', attrs = {"class":'w_kV33 w_Sl3f w_mvVb f5 b'})
        stars  =scraper.findAll('span', attrs = {"class":'w_iUH7'})
        for review, star in zip(reviews[1:], stars[8:]):
            print(f"{review.text} || {star.text}")

