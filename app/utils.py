import logging
import requests
from flask import current_app

logging.basicConfig(level=logging.DEBUG)

def fetch_ozon_data(category):
    url = "https://api-seller.ozon.ru/v2/product/list"
    headers = {
        "Client-Id": current_app.config['OZON_CLIENT_ID'],
        "Api-Key": current_app.config['OZON_API_KEY'],
        "Content-Type": "application/json",
    }
    payload = {
        "filter": {
            "category_id": category
        },
        "limit": 50
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("result", {}).get("items", [])
    else:
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        raise Exception(f"Ошибка при запросе к API Ozon: {response.status_code}, {error_message}")

def fetch_ozon_data_by_query(query):
    url = "https://api-seller.ozon.ru/v2/product/list"
    headers = {
        "Client-Id": current_app.config['OZON_CLIENT_ID'],
        "Api-Key": current_app.config['OZON_API_KEY'],
        "Content-Type": "application/json",
    }
    payload = {
        "filter": {
            "search": query
        },
        "limit": 50
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("result", {}).get("items", [])
    else:
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        raise Exception(f"Ошибка при запросе к API Ozon: {response.status_code}, {error_message}")