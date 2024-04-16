from typing import Union
from fastapi import FastAPI
from WalmartBot import WalmartBot
from RocketHomesBot import RocketHomesBot
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO


import os
app = FastAPI()

walmart_bot = WalmartBot()
rocket_bot = RocketHomesBot()
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
@app.get("/rocket-homes/{state}/{city}/{pageTotal}")
def read_item(state: str, city: str, pageTotal: int):
    housing_data = rocket_bot.scrape_pages(state, city, pageTotal)
    return housing_data