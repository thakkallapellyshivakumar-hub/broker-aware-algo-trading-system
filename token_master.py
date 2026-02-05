def get_symbol_token(obj, stock_name, exchange="NSE"):
    """
    Uses Angel One searchScrip API (official & stable)
    stock_name: SBIN / HAL / DIXON / RELIANCE
    returns: (tradingsymbol, symboltoken)
    """
    try:
        # IMPORTANT: positional arguments only
        res = obj.searchScrip(exchange, stock_name)
    except Exception as e:
        print("❌ searchScrip API error:", e)
        return None, None

    if not res or not res.get("data"):
        return None, None

    # Prefer EQ symbols
    for item in res["data"]:
        symbol = item.get("tradingsymbol", "")
        token = item.get("symboltoken")

        if symbol.endswith("-EQ"):
            return symbol, token

    # Fallback: first result
    item = res["data"][0]
    return item.get("tradingsymbol"), item.get("symboltoken")
