import time

def safe_call(func, sleep_sec=2, default=None):
    try:
        return func()
    except Exception as e:
        if "access rate" in str(e).lower():
            time.sleep(sleep_sec)
            return default
        raise


def run_live_engine(obj, symbol, token, exchange, qty, side, entry_price,
                    sl_order_id, target_order_id,
                    sl_trigger, sl_buffer, trail_points):

    print("\n🟢 LIVE ENGINE STARTED (Trailing SL active)\n")

    last_trail_price = entry_price
    last_ob_check = 0

    try:
        while True:
            time.sleep(3)

            ltp = safe_call(
                lambda: obj.ltpData(
                    exchange=exchange,
                    tradingsymbol=symbol,
                    symboltoken=token
                )["data"]["ltp"],
                default=None
            )
            if ltp is None:
                continue

            # ---- TRAIL SL ----
            if side == "BUY" and ltp >= last_trail_price + trail_points:
                sl_trigger += trail_points
                sl_limit = sl_trigger - sl_buffer
                last_trail_price = ltp

                safe_call(lambda: obj.modifyOrder({
                    "orderid": sl_order_id,
                    "price": str(round(sl_limit, 2)),
                    "triggerprice": str(round(sl_trigger, 2)),
                    "quantity": str(qty)
                }))

                print(f"\n🔁 SL MODIFIED → {sl_trigger}")

            # ---- CHECK EXIT (slow) ----
            if time.time() - last_ob_check > 10:
                last_ob_check = time.time()
                ob = safe_call(lambda: obj.orderBook(), default=None)

                if ob and ob.get("data"):
                    for o in ob["data"]:
                        if o["orderid"] == sl_order_id and o["orderstatus"].lower() == "complete":
                            print("\n🛑 SL HIT – EXITED")
                            safe_call(lambda: obj.cancelOrder(target_order_id))
                            raise KeyboardInterrupt

                        if o["orderid"] == target_order_id and o["orderstatus"].lower() == "complete":
                            print("\n🎯 TARGET HIT – EXITED")
                            safe_call(lambda: obj.cancelOrder(sl_order_id))
                            raise KeyboardInterrupt

            pnl = (ltp - entry_price) * qty if side == "BUY" else (entry_price - ltp) * qty

            print(
                f"\r{symbol} | LTP:{ltp:.2f} | SL:{sl_trigger:.2f} | "
                f"P&L:{pnl:.2f}        ",
                end=""
            )

    except KeyboardInterrupt:
        print("\n🏁 LIVE ENGINE STOPPED")
