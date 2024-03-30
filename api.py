from typing import Union
from fastapi import FastAPI
from WalmartBot import WalmartBot
from TruliaBot import TruliaBot
app = FastAPI()

walmart_bot = WalmartBot()
trulia_bot = TruliaBot()
@app.get("/")
def read_root():
    return {"Hello": "User"}

@app.get("/walmart-products/{query}/{pageTotal}")
#for queries with multiple words example Playstation 5, use format playstation+5
def read_item(query: str, pageTotal: int):
    return walmart_bot.scrape_pages(query, pageTotal)

@app.get("/walmart-products/sorted/{query}/{pageTotal}")
def read_item(query: str, pageTotal: int):
    productData = walmart_bot.scrape_pages(query, pageTotal)
    sortedData = walmart_bot.sorted_products(productData, pageTotal)
    return sortedData

@app.get("/trulia-homes/{state}/{city}")
def read_item(state: str, city: str):
    data =  trulia_bot.pull_house_data(state, city, 1, False)
    while data["Page 1"] == []:
        data = trulia_bot.pull_house_data(state, city, 1, False)
    return data

@app.get("/trulia-homes/{state}/{city}/{page}")
def read_item(state: str, city: str, page: int):
    try:
        data = trulia_bot.scrape_pages(state, city, page, False)
        return data
    except:
        return {"Error Message": "The api failed to pull the data, please make sure that the spelling for the state abbreviation and city name are correct."}
@app.get("/trulia-rental/{state}/{city}/{page}")
def read_item(state: str, city: str, page: int):
    try:
        data = trulia_bot.scrape_pages(state, city, page, True)
        return data
    except:
        return {"Error Message": "The api failed to pull the data, please make sure that the spelling for the state abbreviation and city name are correct."}

@app.get("/trulia-images/{state}/{city}")
def read_item(state: str, city: str):
    images = trulia_bot.scrape_images(state, city)
    print(images["Images"])
    while images["Images"] == []:
        images = trulia_bot.scrape_images(state, city)
    return images