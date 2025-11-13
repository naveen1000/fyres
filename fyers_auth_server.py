# fyers_auth_server.py
import os
import json
import webbrowser
from flask import Flask, request
from fyers_apiv3 import fyersModel
import gspread

# CONFIG
GSHEET_SERVICE_KEY = "gsheet_service_key.json"
GSHEET_NAME = "Apps Associates"
CONFIG_SHEET = "config"

app = Flask(__name__)

def get_config():
    gc = gspread.service_account(filename=GSHEET_SERVICE_KEY)
    sh = gc.open(GSHEET_NAME)
    ws = sh.worksheet(CONFIG_SHEET)
    client_id = ws.acell("F2").value.strip()
    secret_key = ws.acell("F3").value.strip()
    redirect_uri = ws.acell("F4").value.strip()
    return client_id, secret_key, redirect_uri, ws

@app.route("/")
def index():
    client_id, secret_key, redirect_uri, ws = get_config()
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )
    login_url = session.generate_authcode()
    return f"""
    <h3>FYERS Authorization</h3>
    <p><a href="{login_url}" target="_blank">Click here to Login to FYERS</a></p>
    """

@app.route("/callback")
def callback():
    auth_code = request.args.get("auth_code")
    if not auth_code:
        return "<p>Auth code missing in callback URL.</p>"
    
    client_id, secret_key, redirect_uri, ws = get_config()
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )
    session.set_token(auth_code)
    response = session.generate_token()
    print("Response:", response)
    
    if response.get("s") == "ok":
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        ws.update("F5", [[refresh_token]])
        ws.update("F6", [[access_token]])
        return "<p>✅ Tokens saved to Google Sheet! You can close this window.</p>"
    else:
        return f"<p>❌ Error: {response}</p>"

if __name__ == "__main__":
    client_id, secret_key, redirect_uri, ws = get_config()
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )
    login_url = session.generate_authcode()
    print("Open this URL to login and authorize:")
    print(login_url)
    webbrowser.open(login_url)
    app.run(port=5000)
