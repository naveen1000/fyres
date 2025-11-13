# fyers_token_refresh.py
from fyers_apiv3 import fyersModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# === FYERS Credentials ===
FYERS_CLIENT_ID = "YOUR_CLIENT_ID"        # e.g. YH1234-100
FYERS_SECRET_KEY = "YOUR_SECRET_KEY"
REDIRECT_URI = "https://your_redirect_url"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"

# === Google Sheet Setup ===
SHEET_NAME = "FyersJournal"
SHEET_TAB = "config"   # will hold access_token

# Google Service Account JSON key file
GOOGLE_CREDENTIALS_FILE = "service_account.json"

def refresh_access_token():
    session = fyersModel.SessionModel(
        client_id=FYERS_CLIENT_ID,
        secret_key=FYERS_SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="refresh_token",
        refresh_token=REFRESH_TOKEN
    )
    response = session.generate_access_token()

    if response.get("s") == "ok":
        access_token = response["access_token"]
        print("✅ Token refreshed.")

        # Save to Google Sheet
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_CREDENTIALS_FILE, 
            ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).worksheet(SHEET_TAB)

        sheet.update("A1", "access_token")
        sheet.update("B1", access_token)
        sheet.update("A2", "last_refreshed")
        sheet.update("B2", str(datetime.datetime.now()))

        print("✅ Access token saved to sheet.")
    else:
        print("❌ Failed to refresh token:", response)

if __name__ == "__main__":
    refresh_access_token()
