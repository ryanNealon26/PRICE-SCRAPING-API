from typing import Union

from fastapi import FastAPI
from WalmartBot import WalmartBot
app = FastAPI()

walmart_bot = WalmartBot()
@app.get("/")
def read_root():
    return {"Hello": "User"}

@app.get("/walmart-products/{query}/{pageTotal}")
#for queries with multiple words example Playstation 5, use format playstation+5
def read_item(query: str, pageTotal: int):
    return walmart_bot.scrape_pages(query, pageTotal)
