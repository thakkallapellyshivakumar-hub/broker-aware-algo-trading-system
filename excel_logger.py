import pandas as pd
from datetime import datetime

FILE_NAME = "angel_orders.xlsx"


def save_orders_to_excel(orderbook, ltp_map):
    rows = []

    for o in orderbook:
        symbol = o.get("tradingsymbol")
        rows.append({
            "Stock": symbol,
            "Exchange": o.get("exchange"),
            "Side": o.get("transactiontype"),
            "Product": o.get("producttype"),
            "Qty": o.get("quantity"),
            "Placed Price": o.get("price"),
            "Executed Price": o.get("averageprice") or "-",
            "LTP": ltp_map.get(symbol, "-"),
            "Status": o.get("orderstatus"),
            "Time": o.get("updatetime") or o.get("exchtime")
        })

    df = pd.DataFrame(rows)
    df.to_excel(FILE_NAME, index=False)
