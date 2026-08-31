import requests

BASE_URL = "http://localhost:8000/api/v1"

def get_headers(token: str | None = None) -> dict:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def api_get(endpoint: str, token: str | None = None, params: dict | None = None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=get_headers(token), params=params)
    return response

def api_post(endpoint: str, json: dict | None = None, data: dict | None = None, token: str | None = None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, headers=get_headers(token), json=json, data=data)
    return response

def api_put(endpoint: str, json: dict | None = None, token: str | None = None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.put(url, headers=get_headers(token), json=json)
    return response

def api_delete(endpoint: str, token: str | None = None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.delete(url, headers=get_headers(token))
    return response

def api_post_file(endpoint: str, files: dict, data: dict, token: str | None = None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, headers=get_headers(token), files=files, data=data)
    return response
