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
        historical_data = get_historical_nifty()

        return {
            "news": news.get("titles", []),
            "top_gainers": gainers.get("top_gainers", []),
            "top_losers": losers.get("top_losers", []),
            "historical_data": historical_data.get("nifty", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Dashboard error: {str(e)}")


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
    

def get_historical_nifty():
    url = f"{BASE_URL}/historical_data"
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "stock_name": "nifty",
        "period": "max",
        "filter": "default",
        "key": "all"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        return {"nifty": data}
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=500, detail=f"Historical API error: {e.response.text}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/commodities")
def get_commodities():
    url = f"{BASE_URL}/commodities"
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # since data is a list, just slice it
        commodities_raw = data[:10]

        commodities = [
            {
                "product": c.get("product"),
                "expiry": c.get("expiry"),
                "change": c.get("change"),
                "per_change": c.get("per_change"),
            }
            for c in commodities_raw
        ]


        return {"commodities": commodities}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))