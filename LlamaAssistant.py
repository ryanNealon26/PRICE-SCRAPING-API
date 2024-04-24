from api_key import api_key
import json
from llamaapi import LlamaAPI
from RocketHomesBot import RocketHomesBot

# Initialize the SDK
class LlamaAssistant:
    def __init__(self):
        self.llama = LlamaAPI(api_key)
    def generate_answer(self, preferences, selection):
        if(selection=="Find Ideal Locations"):
            prompt = f"Give me a list of cities and towns that a user would enjoy with the following detailed preferences. Please use the state abbreviation instead of the full state name. Use * at the beginning of each list element. Preferences Begin Here: {preferences} "
        if(selection=="Learn about Locations"):
            prompt = f"Tell me about locations the user asks for. Include information such as population, common weather, price ranges, and a general variety of data that a home buyer would want to know about a location. Location Begin Here: {preferences}"
        # Build the API request
        api_request_json = {
            "model": "llama3-70b",
            "messages": [
                {"role": "user", "content": prompt},
                
            ]
        }
        response = self.llama.run(api_request_json)
        response = self.filter_response(response)
        return response
    def filter_response(self, response):
        ai_response = response.json()['choices'][0]["message"]["content"]
        ai_response = ai_response.replace("<", "").replace(">","")
        ai_response = ai_response.replace("\n", "<br></br>")
        return ai_response
    def analyze_housing_data(self, state, city, preferences):
        rocket_bot = RocketHomesBot()
        housing_data = rocket_bot.scrape_pages(state, city, 1)
        #housing_data is json
        housing_data_json = json.dumps(housing_data)
        prompt = f"Analyze the following json data {housing_data_json} and choose some (at most 3) of the properties that fit the specified preferences. Return the list and include all of the data in the json including links. Preferences: {preferences}"
        api_request_json = {
            "model": "llama3-70b",
            "messages": [
                {"role": "user", "content": prompt},
                
            ],
        }
        response = self.llama.run(api_request_json)
        response = self.filter_response(response)
        return response



