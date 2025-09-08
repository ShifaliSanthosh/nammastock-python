from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
load_dotenv()
app = FastAPI()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://stock.indianapi.in"


@app.get("/news")
def get_news():
    url = f"{BASE_URL}/news"
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()
