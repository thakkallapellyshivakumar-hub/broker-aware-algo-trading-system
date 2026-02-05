import time
import random
from datetime import datetime
import pandas as pd

from broker import angel_login
from orders import place_order, get_ltp
from token_master import get_symbol_token
from config import TRADE_MODE
from telegram_alerts import send_alert

# ================= USER SETTINGS =================
SL_POINTS = 10
TARGET_POINTS = 20
TRAIL_POINTS = 5
SL_BUFFER = 0.5
EXCEL_FILE = "trade_log.xlsx"

BLOCKED_SUFFIXES = ("-BE", "-BZ", "-BL", "-AF", "-RL", "-IQ", "-LS")

# ================= HELPERS =================
def is_live_trade_allowed(symbol):
    return not symbol.endswith(BLOCKED_SUFFIXES)

def safe_call(func, sleep_sec=2, default=None):
    try:
        return func()
    except Exception as e:
        if "access rate" in str(e).lower():
            time.sleep(sleep_sec)
            return default
        raise

def init_excel():
    try:
        pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "Time","Mode","Symbol","Side","Qty",
            "Entry Price","Exit Price","Exit Reason","PnL"
        ])
        df.to_excel(EXCEL_FILE, index=False)

def log_trade(row):
    df = pd.read_excel(EXCEL_FILE)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

# ================= START =================
print("🚀 MAIN STARTED")
init_excel()

print("🔐 Logging in...")
obj = angel_login()
print("✅ Logged in")

# ================= SYMBOL =================
stock = input("\nEnter Stock Name (e.g. SBIN / INFY): ").strip().upper()
symbol, token = get_symbol_token(obj, stock)

if not symbol:
    print("❌ Symbol not found")
    exit()

exchange = "NSE"
ltp = get_ltp(obj, exchange, symbol, token)
print(f"\n📊 {symbol} | LTP: {ltp}")

# ================= INPUT =================
qty = int(input("Enter Quantity: "))
side = input("BUY or SELL: ").strip().upper()

print(f"\n📝 CONFIRM → {symbol} {side} Qty:{qty} Mode:{TRADE_MODE}")
if input("Confirm order? (YES / NO): ").strip().upper() != "YES":
    exit()

# ================= LIVE SAFETY =================
if TRADE_MODE == "LIVE":
    if not is_live_trade_allowed(symbol):
        msg = f"⚠️ LIVE ORDER BLOCKED\nSymbol: {symbol}\nReason: Caution / Surveillance"
        print(msg)
        send_alert(msg)
        exit()

    rms = safe_call(lambda: obj.rmsLimit(), default=None)
    if rms and rms.get("data"):
        available = float(rms["data"]["availablecash"])
        required = ltp * qty * 0.2

        print(f"💰 Available Margin: {available:.2f}")
        print(f"📉 Required Margin (approx): {required:.2f}")

        if available < required:
            msg = (
                "❌ LIVE ORDER BLOCKED – INSUFFICIENT FUNDS\n"
                f"Symbol: {symbol}\n"
                f"Available: {available:.2f}\n"
                f"Required: {required:.2f}"
            )
            print(msg)
            send_alert(msg)
            exit()

# ================= PLACE ENTRY =================
print("\n📥 Placing ENTRY order...")
order_id = place_order(obj, {
    "variety": "NORMAL",
    "tradingsymbol": symbol,
    "symboltoken": token,
    "transactiontype": side,
    "exchange": exchange,
    "ordertype": "MARKET",
    "producttype": "INTRADAY",
    "duration": "DAY",
    "price": "0",
    "quantity": str(qty)
})

if not order_id:
    print("❌ Entry order failed")
    exit()

if TRADE_MODE == "LIVE":
    send_alert(
        "✅ LIVE ORDER PLACED\n"
        f"Symbol: {symbol}\nSide: {side}\nQty: {qty}\nOrder ID: {order_id}"
    )

print(f"✅ ENTRY ORDER ID: {order_id}")

# ================= PAPER MODE =================
if TRADE_MODE == "PAPER":
    send_alert(f"📄 PAPER ORDER\n{symbol} {side} Qty:{qty}")

    fill_ratio = random.choice([0.5, 0.7, 1.0])
    filled_qty = max(1, int(qty * fill_ratio))
    entry_price = round(ltp + random.uniform(-0.2, 0.2), 2)

    if side == "BUY":
        sl = entry_price - SL_POINTS
        target = entry_price + TARGET_POINTS
    else:
        sl = entry_price + SL_POINTS
        target = entry_price - TARGET_POINTS

    last_trail = entry_price
    print("\n📈 PAPER TRAILING STARTED\n")

    try:
        while True:
            time.sleep(2)
            ltp = get_ltp(obj, exchange, symbol, token)

            if side == "BUY" and ltp >= last_trail + TRAIL_POINTS:
                sl += TRAIL_POINTS
                last_trail = ltp

            pnl = (ltp - entry_price) * filled_qty

            # ===== EXACT FIX: ONE-LINE UPDATE ONLY =====
            print(
                f"\r{symbol} | LTP:{ltp:.2f} | SL:{sl:.2f} | "
                f"TARGET:{target:.2f} | P&L:{pnl:.2f}        ",
                end="",
                flush=True
            )
            # ==========================================

            if ltp <= sl:
                exit_price = ltp
                exit_reason = "SL HIT"
                break

            if ltp >= target:
                exit_price = ltp
                exit_reason = "TARGET HIT"
                break

    except KeyboardInterrupt:
        exit_price = ltp
        exit_reason = "MANUAL EXIT"

    pnl = (exit_price - entry_price) * filled_qty

    log_trade({
        "Time": datetime.now(),
        "Mode": "PAPER",
        "Symbol": symbol,
        "Side": side,
        "Qty": filled_qty,
        "Entry Price": entry_price,
        "Exit Price": exit_price,
        "Exit Reason": exit_reason,
        "PnL": round(pnl, 2)
    })

    send_alert(f"🏁 PAPER EXIT\n{symbol}\nReason: {exit_reason}\nPnL: {round(pnl,2)}")
    print()
    exit()

# ================= LIVE MODE CONTINUES UNCHANGED =================
