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
JOURNAL_SHEET = "PnL_Journal"
TELEGRAM_BOT_TOKEN = "8332447645:AAFMiAN6nYCzAWf0U6mDhlbC1Tl2_oPLi2A"  # Replace
TELEGRAM_CHAT_ID = "582942300"              # Replace


# ===== DATE HELPERS =====
def get_period_dates():
    today = dt.date.today()
    week_start = today - dt.timedelta(days=today.weekday())  # Monday
    month_start = today.replace(day=1)
    return today, week_start, month_start


# ===== FYERS CONNECTION =====
def get_fyers():
    gc = gspread.service_account(filename=GSHEET_FILE_PATH)
    sh = gc.open(GSHEET_FILE)
    ws = sh.worksheet(CONFIG_SHEET)
    token = ws.acell("F6").value.strip()
    fyers = fyersModel.FyersModel(client_id=CLIENT_ID, token=token)
    return fyers, gc, sh


# ===== FETCH P&L =====
def get_pnl(fyers):
    data = fyers.positions()
    if data.get("s") != "ok":
        print("❌ Error fetching positions:", data)
        return None, None
    realized, unrealized = 0.0, 0.0
    for p in data.get("netPositions", []):
        realized += p.get("realized_profit", 0.0)
        unrealized += p.get("unrealized_profit", 0.0)
    return realized, unrealized


# ===== LOG DAILY ENTRY =====
def log_pnl_to_sheet(sh, realized, unrealized, total):
    today = dt.date.today().strftime("%Y-%m-%d")
    try:
        ws = sh.worksheet(JOURNAL_SHEET)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=JOURNAL_SHEET, rows=1000, cols=6)
        #ws.update(range_name="A1:F1",values=[["Date", "Realized", "Unrealized", "Total", "WeekNum", "Month"]])
        ws.update(values=[["Date", "Realized", "Unrealized", "Total", "WeekNum", "Month"]], range_name="A1:F1")
        #ws.update(body={"values": [["Date", "Realized", "Unrealized", "Total", "WeekNum", "Month"]]},range_name="A1:F1")

        


    records = ws.get_all_records()
    dates = [r["Date"] for r in records] if records else []

    week_num = dt.date.today().isocalendar()[1]
    month_name = dt.date.today().strftime("%B")

    if today not in dates:
        ws.append_row([today, realized, unrealized, total, week_num, month_name])
        
    else:
        idx = dates.index(today) + 2  # +1 for header, +1 for 0-index
        #ws.update(range_name=f"B{idx}:D{idx}", values=[[realized, unrealized, total]])
        ws.update(values=[[realized, unrealized, total]], range_name=f"B{idx}:D{idx}")
        #ws.update(body={"values": [[realized, unrealized, total]]},range_name=f"B{idx}:D{idx}")

    print(f"✅ Logged to Sheet: {today}")


# ===== COMPUTE WEEK / MONTH TOTALS =====
def compute_period_pnl(ws, week_start, month_start):
    data = ws.get_all_records()
    if not data:
        return 0, 0, 0

    today = dt.date.today()
    today_total = week_total = month_total = 0.0

    for row in data:
        try:
            row_date = dt.datetime.strptime(row["Date"], "%Y-%m-%d").date()
            total = float(row.get("Total", 0))
            realized = float(row.get("Realized", 0))

            if row_date == today:
                today_total += total
            if row_date >= week_start:
                week_total += realized
            if row_date >= month_start:
                month_total += realized
        except Exception:
            continue

    return today_total, week_total, month_total


# ===== TELEGRAM SENDER (async, compatible with v21+) =====
async def send_to_telegram(msg):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="HTML")


# ===== MAIN FUNCTION =====
def main():
    fyers, gc, sh = get_fyers()
    realized, unrealized = get_pnl(fyers)

    if realized is None:
        asyncio.run(send_to_telegram("❌ Failed to fetch P&L. Check your FYERS token."))
        return

    total = realized + unrealized
    log_pnl_to_sheet(sh, realized, unrealized, total)

    _, week_start, month_start = get_period_dates()
    ws = sh.worksheet(JOURNAL_SHEET)
    today_total, week_total, month_total = compute_period_pnl(ws, week_start, month_start)

    msg = f"""
📊 <b>FYERS P&L Report</b>

🗓️ <b>Today:</b> ₹{round(today_total, 2)}
  💰 <b>Realized:</b> ₹{round(realized, 2)}
  💤 <b>Unrealized:</b> ₹{round(unrealized, 2)}

📅 <b>Week (Mon→Today):</b> ₹{round(week_total, 2)}
📆 <b>Month (1st→Today):</b> ₹{round(month_total, 2)}

🧾 <i>Logged on: {dt.date.today().strftime('%d %b %Y')}</i>
"""
    asyncio.run(send_to_telegram(msg.strip()))
    print("✅ Sent P&L update to Telegram!")


if __name__ == "__main__":
    main()
