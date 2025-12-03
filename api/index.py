from flask import Flask, abort

from flask import request
from bs4 import BeautifulSoup
import json
import requests

app = Flask(__name__)


@app.route("/", methods=["POST"])
def fetch_balance():
    try:
        data = request.get_json()
        payload = {
            "username": data["username"],
            "password": data["password"],
        }
    except KeyError:
        abort(400)

    csrf_token, cookies = fetch_csrf()
    try:
        balance = auth_and_fetch_balance(payload, csrf_token, cookies)
        return {
            "balance": balance,
        }
    except:
        abort(401)


BASE_URL = "https://www.magticom.ge/"


def fetch_csrf():
    csrf_request = requests.get(BASE_URL + "mymagti")
    request_cookies = csrf_request.cookies.get_dict()
    soup = BeautifulSoup(csrf_request.text, "html.parser")
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

app.run(debug=False, host='0.0.0.0', port=8080)
