import time
import gspread
from fyers_apiv3 import fyersModel


# ====== CONFIG ======
CLIENT_ID = "DUDIBC46PY-100"   # Replace with your Client ID
SECRET_KEY = "AKFYIB3Q54"  # Replace with your Secret Key
REDIRECT_URI = "http://127.0.0.1:5000/callback"  # Same as in Fyers App
AUTH_CODE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJEVURJQkM0NlBZIiwidXVpZCI6IjVjZjI1NzY1MDEyYjRmODY4ZTE2ZGI5OWQ3OGJmNDA3IiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IllTNTQ3MDQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIwYTc4YTAyNzUxNzY0MzhmZTBhYjM1NjgzMTI2NmMyNjZlYzZiZmVlYWYwYTczOWNiNmQ3ZmI2OCIsImlzRGRwaUVuYWJsZWQiOiJZIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzYyOTgxODM4LCJpYXQiOjE3NjI5NTE4MzgsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc2Mjk1MTgzOCwic3ViIjoiYXV0aF9jb2RlIn0.1qsybUFsDJeSfIXi_LC_aICbH8c2tvTuhzjnxEhyuWU"  # Get fresh auth_code manually from Fyers URL once
GSHEET_FILE = "Apps Associates"
GSHEET_SHEET = "config"
GSHEET_FILE_PATH = "gsheet_service_key.json"

# ====== GOOGLE SHEET CONNECT ======
gc = gspread.service_account(filename=GSHEET_FILE_PATH)
sh = gc.open(GSHEET_FILE)
worksheet = sh.worksheet(GSHEET_SHEET)


# ====== STEP 1: Create Session ======
def refresh_token_to_sheet():
    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

    session.set_token(AUTH_CODE)
    response = session.generate_token()
    print(response)

    access_token = response.get("access_token")

    if not access_token:
        print("❌ Token generation failed.")
        return

    # ====== STEP 2: Write Token to Google Sheet ======
    worksheet.update(range_name='B1', values=[[access_token]])
    print("✅ Access Token Updated in Google Sheet!")


if __name__ == "__main__":
    refresh_token_to_sheet()
