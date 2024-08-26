from flask import Flask, abort

from main import fetch_csrf, auth_and_fetch_balance
from flask import request

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


app.run(debug=True, host='0.0.0.0', port=80)
