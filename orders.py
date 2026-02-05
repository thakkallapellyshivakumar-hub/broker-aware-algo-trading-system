from config import TRADE_MODE
from telegram import send_alert

def get_ltp(obj, exchange, tradingsymbol, symboltoken):
    data = obj.ltpData(
        exchange=exchange,
        tradingsymbol=tradingsymbol,
        symboltoken=symboltoken
    )

    if data and data.get("status"):
        return data["data"]["ltp"]

    return None

def place_order(obj, params):
    if TRADE_MODE == "PAPER":
        send_alert(f"📄 PAPER ORDER\n{params}")
        return "PAPER_ORDER_ID"

    order = obj.placeOrder(params)

    if isinstance(order, str):
        send_alert(f"✅ LIVE ORDER PLACED\nOrder ID: {order}")
        return order

    if order and order.get("status") is False:
        send_alert(f"❌ ORDER FAILED\n{order.get('message')}")
        return None

def modify_order(obj, order_id, price):
    if TRADE_MODE == "LIVE":
        obj.modifyOrder({
            "variety": "NORMAL",
            "orderid": order_id,
            "price": price,
            "ordertype": "LIMIT"
        })

def cancel_order(obj, order_id):
    if TRADE_MODE == "LIVE":
        obj.cancelOrder({"variety": "NORMAL", "orderid": order_id})
