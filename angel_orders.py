"""
Angel One SmartAPI – Place Order Script
--------------------------------------
• Uses MPIN (no password)
• Safe error handling
• No NoneType crashes
• Beginner + production friendly
"""

from SmartApi import SmartConnect
import pyotp
import time
from config import API_KEY, CLIENT_ID, MPIN, TOTP_SECRET


# ------------------------------------------------
# STEP 1: LOGIN
# ------------------------------------------------
print("🔐 Logging in to Angel One...")

obj = SmartConnect(api_key=API_KEY)

try:
    totp = pyotp.TOTP(TOTP_SECRET).now()
    session = obj.generateSession(CLIENT_ID, MPIN, totp)
except Exception as e:
    print("❌ Login exception:", e)
    exit()

if session is None or session.get("status") is False:
    print("❌ Login Failed")
    print("Message:", session.get("message") if session else "No response")
    exit()

print("✅ Login Successful")


# ------------------------------------------------
# STEP 2: ORDER DETAILS (USE SAFE SYMBOLS FIRST)
# ------------------------------------------------
order_params = {
    "variety": "NORMAL",
    "tradingsymbol": "SBIN-EQ",      # ✅ SAFE TEST SYMBOL
    "symboltoken": "3045",           # SBIN token
    "transactiontype": "BUY",
    "exchange": "NSE",
    "ordertype": "LIMIT",
    "producttype": "INTRADAY",
    "duration": "DAY",
    "price": "650",                  # example price
    "quantity": "1"
}


# ------------------------------------------------
# STEP 3: PLACE ORDER (SAFE HANDLING)
# ------------------------------------------------
print("📥 Placing Order...")

try:
    order = obj.placeOrder(order_params)
except Exception as e:
    print("❌ Exception while placing order:", e)
    exit()

# CASE 1: API returned nothing
if order is None:
    print("❌ Order failed: No response from Angel One")
    exit()

# CASE 2: SUCCESS (Angel returns order id as string)
if isinstance(order, str):
    order_id = order
    print(f"✅ Order Placed Successfully | Order ID: {order_id}")
    exit()

# CASE 3: API returned dict
if isinstance(order, dict):

    if order.get("status") is False:
        print("❌ Order Rejected")
        print("Message:", order.get("message"))
        print("Error Code:", order.get("errorcode"))
        exit()

    # success dict
    order_id = order.get("data", {}).get("orderid")
    print(f"✅ Order Placed Successfully | Order ID: {order_id}")
    exit()

# Fallback (should never happen)
print("⚠️ Unknown order response type:", order)



# ------------------------------------------------
# STEP 4: (OPTIONAL) MODIFY ORDER
# ------------------------------------------------
"""
time.sleep(2)

modify_params = {
    "variety": "NORMAL",
    "orderid": order_id,
    "ordertype": "LIMIT",
    "price": "645",
    "quantity": "1"
}

modify = obj.modifyOrder(modify_params)

if modify and modify.get("status"):
    print("✏️ Order Modified")
else:
    print("⚠️ Modify Failed:", modify)
"""


# ------------------------------------------------
# STEP 5: (OPTIONAL) CANCEL ORDER
# ------------------------------------------------
"""
time.sleep(2)

cancel_params = {
    "variety": "NORMAL",
    "orderid": order_id
}

cancel = obj.cancelOrder(cancel_params)

if cancel and cancel.get("status"):
    print("❌ Order Cancelled")
else:
    print("⚠️ Cancel Failed:", cancel)
"""
