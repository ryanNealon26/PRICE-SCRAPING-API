from typing import Union
from fastapi import FastAPI, WebSocket
from WalmartBot import WalmartBot
from RocketHomesBot import RocketHomesBot
from LlamaAssistant import LlamaAssistant
import pandas as pd
from fastapi.responses import FileResponse
app = FastAPI()


walmart_bot = WalmartBot()
rocket_bot = RocketHomesBot()

ai_assistant = LlamaAssistant()

#fast api websockets

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

@app.get("/rocket-homes/excel/{state}/{city}/{pageTotal}")
def read_item(state: str, city: str, pageTotal: int):
    json_data = rocket_bot.scrape_pages(state, city, pageTotal)
    excel_name = f"{city}_{state}_page{pageTotal}.xlsx"
    pd.DataFrame(json_data["Property Data"]).to_excel(excel_name, index=True)
    return FileResponse(excel_name)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        promptData = await websocket.receive_text()
        promptSel = await websocket.receive_text()
        print(promptSel)
        response = ai_assistant.generate_answer(promptData, promptSel)
        await websocket.send_text(response)

@app.websocket("/ai")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        state = await websocket.receive_text()
        city = await websocket.receive_text()
        promptData = await websocket.receive_text()
        response = ai_assistant.analyze_housing_data(state, city, promptData)
        await websocket.send_text(response)
        