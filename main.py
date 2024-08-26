from bs4 import BeautifulSoup
import json
import requests

BASE_URL = "https://www.magticom.ge/"


def fetch_csrf():
    request = requests.get(BASE_URL + "mymagti")
    request_cookies = request.cookies.get_dict()
    soup = BeautifulSoup(request.text, "html.parser")
    return soup.find("input", {"name": "csrf-token-login"}).get("value"), request_cookies


def auth_and_fetch_balance(credentials, csrf_token, cookies):
    data = {
        "subscriber": credentials["username"],
        "password": credentials["password"],
        "csrf-token-login": csrf_token
    }
    requests.post(BASE_URL + "request/log-in.php", data=data, cookies=cookies)
    portal = requests.get(BASE_URL + "request/accounts.php", cookies=cookies)
    raw_data = json.loads(portal.text)
    return raw_data["balances"][0]["balance"]
