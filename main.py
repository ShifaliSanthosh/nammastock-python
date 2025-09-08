from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
app = FastAPI()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://stock.indianapi.in"



@app.get("/dashboard")
def get_dashboard():
    """Combined endpoint for Angular dashboard"""
    try:
        news = get_news()
        gainers = get_top_gainers()
        losers = get_top_losers()

        return {
            "news": news.get("titles", []),
            "top_gainers": gainers.get("top_gainers", []),
            "top_losers": losers.get("top_losers", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")



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
