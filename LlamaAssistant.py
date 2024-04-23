from api_key import api_key
import json
from llamaapi import LlamaAPI

# Initialize the SDK
class LlamaAssistant:
    def __init__(self):
        self.llama = LlamaAPI(api_key)
    def generate_answer(self, preferences):
        prompt = f"Please do not use emojis in your reply. Give me a list of cities and towns that a user would enjoy with the following detailed preferences. Please use the state abbreviation instead of the full state name. Do not include new line characters in the response and use * at the beginning of each list element. Preferences Begin Here: {preferences} "
        # Build the API request
        api_request_json = {
            "messages": [
                {"role": "user", "content": prompt},
                
            ]
        }
        response = self.llama.run(api_request_json)
        response = self.filter_response(response)
        return response
    def filter_response(self, response):
        ai_response = response.json()['choices'][0]["message"]["content"]
        ai_response = ai_response.replace(")", "<br></br>").replace("(", " ")
        return ai_response

# Execute the Request

llama = LlamaAssistant()

llama.generate_answer("I enjoy warm climates and wish to have an urban feel")

