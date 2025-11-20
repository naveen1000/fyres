import datetime as dt
import asyncio
import gspread
from fyers_apiv3 import fyersModel
from telegram import Bot

# ===== CONFIG =====
CLIENT_ID = "DUDIBC46PY-100"
GSHEET_FILE_PATH = "/home/ubuntu/Desktop/zerodha/gsheet_service_key.json"
GSHEET_FILE = "Apps Associates"
CONFIG_SHEET = "config"
TELEGRAM_BOT_TOKEN = "8332447645:AAFMiAN6nYCzAWf0U6mDhlbC1Tl2_oPLi2A"  # Replace if needed
TELEGRAM_CHAT_ID = "582942300"              # Replace


def get_fyers():
    """Read FYERS token from Google Sheet and return a fyers client and sheet objects."""
    gc = gspread.service_account(filename=GSHEET_FILE_PATH)
    sh = gc.open(GSHEET_FILE)
    ws = sh.worksheet(CONFIG_SHEET)
    token = ws.acell("F6").value.strip()
    fyers = fyersModel.FyersModel(client_id=CLIENT_ID, token=token)
    return fyers, gc, sh


def get_funds(fyers):
    """Fetch funds from FYERS API. Returns raw response dict or None on error."""
    try:
        data = fyers.funds()
    except Exception as e:
        print("❌ Exception while calling fyers.funds():", e)
        return None

    # If API returns a status field similar to other endpoints
    status = data.get("s") if isinstance(data, dict) else None
    if status and status != "ok":
        print("❌ Error fetching funds:", data)
        return None

    return data


def format_funds(data):
    """Create a readable summary string from the funds response."""
    if not data:
        return "No funds data available."
    # FYERS returns a 'fund_limit' list with items containing titles and amounts
    def fmt_amt(x):
        try:
            return f"₹{float(x):,.2f}"
        except Exception:
            return str(x)

    if isinstance(data, dict):
        parts = []
        # prefer 'fund_limit' if present
        if "fund_limit" in data and isinstance(data["fund_limit"], list):
            for item in data["fund_limit"]:
                title = item.get("title") or item.get("name") or "Item"
                # FYERS example uses 'equityAmount' and 'commodityAmount'
                equity = item.get("equityAmount")
                commodity = item.get("commodityAmount")
                
                if equity is not None and commodity is not None:
                    try:
                        eq_val = float(equity)
                        com_val = float(commodity)
                    except (ValueError, TypeError):
                        eq_val = 0.0
                        com_val = 0.0

                    # If both are zero, skip entirely
                    if eq_val == 0 and com_val == 0:
                        continue
                    
                    # If commodity is zero, show only equity (no label needed if it's the only one, 
                    # but adhering to previous style: "Title: Amount")
                    if com_val == 0:
                        parts.append(f"{title}: {fmt_amt(eq_val)}")
                    # If equity is zero, show only commodity
                    elif eq_val == 0:
                        parts.append(f"{title}: {fmt_amt(com_val)} (Commodity)")
                    # Both non-zero
                    else:
                        parts.append(f"{title}: {fmt_amt(eq_val)} (Equity), {fmt_amt(com_val)} (Commodity)")

                else:
                    # fallback to any numeric fields
                    shown = False
                    for k, v in item.items():
                        if isinstance(v, (int, float)):
                            if v != 0:
                                parts.append(f"{title} - {k}: {fmt_amt(v)}")
                                shown = True
                    if not shown:
                        # Only show if it's not just empty/zero numeric fields we skipped
                        # But here we might want to skip if we didn't find anything interesting.
                        # The original code showed the raw item if nothing was shown.
                        # Let's only show if it really seems relevant, or maybe just skip it to be concise.
                        # User asked: "Sections that contain only zero values will be omitted entirely"
                        pass

            if parts:
                return "\n".join(parts)

        # fallback: show top-level simple fields
        for k, v in data.items():
            if isinstance(v, (int, float)):
                if v != 0:
                    parts.append(f"{k}: {v}")
            elif isinstance(v, str):
                parts.append(f"{k}: {v}")
        if parts:
            return "\n".join(parts)

    # final fallback
    return str(data)


async def send_to_telegram(msg):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="HTML")


def main():
    fyers, gc, sh = get_fyers()
    data = get_funds(fyers)

    if data is None:
        asyncio.run(send_to_telegram("❌ Failed to fetch funds. Check your FYERS token."))
        return

    summary = format_funds(data)
    msg = f"📥 <b>FYERS Funds Summary</b>\n\n{summary}"

    asyncio.run(send_to_telegram(msg))
    print("✅ Sent funds summary to Telegram!")


if __name__ == "__main__":
    main()
