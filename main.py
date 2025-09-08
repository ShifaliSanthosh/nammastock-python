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
        gainers_raw = data.get("trending_stocks", {}).get(
            "top_gainers", [])[:5]
        gainers = [
            {
                "company_name": g.get("company_name"),
                "price": g.get("price"),
                "percent_change": g.get("percent_change"),
                "net_change": g.get("net_change"),
            }
            for g in gainers_raw
        ]

        return {"top_gainers": gainers}
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
        losers_raw = data.get("trending_stocks", {}).get("top_losers", [][:5])
        losers = [
            {
                "company_name": l.get("company_name"),
                "price": l.get("price"),
                "percent_change": l.get("percent_change"),
                "net_change": l.get("net_change"),
            }
            for l in losers_raw
        ]
        return {"top_losers": losers}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
