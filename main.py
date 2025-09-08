from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
from fastapi import HTTPException

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
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        titles = [item.get("title") for item in data]

        return {"titles": titles}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/top-gainers")
def get_top_gainers():
    url = f"{BASE_URL}/trending"
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        gainners = data.get("trending_stocks", {}).get("top_gainers", [][:5])
        return {"top_gainers": gainners}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/top-losers")
def get_top_losers():
    url = f"{BASE_URL}/trending"
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        losers = data.get("trending_stocks", {}).get("top_losers", [][:5])
        return {"top_losers": losers}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
