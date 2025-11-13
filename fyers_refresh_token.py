# fyers_refresh_token.py
import requests
import gspread
import datetime as dt

GSHEET_SERVICE_KEY = "gsheet_service_key.json"
GSHEET_NAME = "Apps Associates"
CONFIG_SHEET = "config"

def get_sheet():
    gc = gspread.service_account(filename=GSHEET_SERVICE_KEY)
    sh = gc.open(GSHEET_NAME)
    return sh.worksheet(CONFIG_SHEET)

def refresh_token():
    ws = get_sheet()
    client_id = ws.acell("F2").value.strip()
    secret_key = ws.acell("F3").value.strip()
    refresh_token = ws.acell("F5").value.strip()

    url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
    payload = {
        "grant_type": "refresh_token",
        "appId": client_id,
        "secret_key": secret_key,
        "refresh_token": refresh_token
    }

    res = requests.post(url, json=payload).json()
    print("Response:", res)

    if res.get("s") == "ok":
        new_access = res["access_token"]
        new_refresh = res["refresh_token"]
        ws.update("F5", [[new_refresh]])
        ws.update("F6", [[new_access]])
        ws.update("F7", [[str(dt.datetime.now())]])
        print("✅ Token refreshed successfully.")
    else:
        print("❌ Token refresh failed:", res)

if __name__ == "__main__":
    refresh_token()
