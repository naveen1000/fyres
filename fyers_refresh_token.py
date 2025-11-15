# fyers_refresh_token.py
import requests
import gspread
import hashlib

# ==== CONFIG ====
CLIENT_ID = "DUDIBC46PY-100"         # e.g. DUDIBC46PY-100
SECRET_KEY = "AKFYIB3Q54"
GSHEET_JSON = "gsheet_service_key.json"
GSHEET_NAME = "Apps Associates"
WORKSHEET_NAME = "config"
# =================

def notify(msg):
    url='https://api.telegram.org/bot1193312817:AAGTRlOs3YZHFeDSO_33YTwwewrEaMbLizE/sendMessage?chat_id=582942300&parse_mode=Markdown&text='+msg
    requests.get(url)
    print("notified")

def sha256_hash(data: str) -> str:
    """Return SHA256 hash string."""
    return hashlib.sha256(data.encode()).hexdigest()

def refresh_token():
    print("🔄 Refreshing Fyers access token...")

    gc = gspread.service_account(filename=GSHEET_JSON)
    ws = gc.open(GSHEET_NAME).worksheet(WORKSHEET_NAME)
    refresh_token_value = ws.acell("F5").value

    if not refresh_token_value:
        print("❌ No refresh token found in F5.")
        return

    # Create SHA256 hash of appId + appSecret
    appIdHash = sha256_hash(f"{CLIENT_ID}:{SECRET_KEY}")

    url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
    payload = {
        "grant_type": "refresh_token",
        "appIdHash": appIdHash,
        "refresh_token": refresh_token_value,
        "pin": "9963"
    }

    try:
        res = requests.post(url, json=payload)
        data = res.json()
        print("Response:", data)

        if data.get("s") == "ok" and "access_token" in data:
            ws.update("F6", [[data["access_token"]]])
            print("✅ Access token refreshed and updated in Google Sheet!")
            notify("✅ Fyers access token refreshed successfully.")
        else:
            print(f"❌ Token refresh failed: {data}")
    except Exception as e:
        print(f"❌ Exception during refresh: {e}")

if __name__ == "__main__":
    refresh_token()
