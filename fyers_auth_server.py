# fyers_auth_server.py
from fyers_apiv3 import fyersModel
import webbrowser
import time
import gspread
from flask import Flask, request

# ========== CONFIG ==========
CLIENT_ID = "DUDIBC46PY-100"        # Example: ABCD12345-100
SECRET_KEY = "AKFYIB3Q54"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
GSHEET_JSON = "gsheet_service_key.json"
GSHEET_NAME = "Apps Associates"
WORKSHEET_NAME = "config"
# =============================

app = Flask(__name__)

gc = gspread.service_account(filename=GSHEET_JSON)
ws = gc.open(GSHEET_NAME).worksheet(WORKSHEET_NAME)

@app.route("/")
def login():
    fyers = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        state="sample"
    )
    auth_link = fyers.generate_authcode()
    webbrowser.open(auth_link)
    return "Opened browser for Fyers login..."

@app.route("/callback")
def callback():
    auth_code = request.args.get("auth_code")
    print(f"Received auth_code: {auth_code}")

    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )
    session.set_token(auth_code)
    token_response = session.generate_token()

    print("Response:", token_response)

    if "refresh_token" in token_response:
        ws.update("F5", [[token_response["refresh_token"]]])
        ws.update("F6", [[token_response["access_token"]]])
        print("✅ Tokens saved successfully to Google Sheet!")
        return "✅ Login successful! You can close this tab now."
    else:
        print("❌ Token generation failed:", token_response)
        return "❌ Token generation failed. Check terminal."

if __name__ == "__main__":
    app.run(port=5000)
