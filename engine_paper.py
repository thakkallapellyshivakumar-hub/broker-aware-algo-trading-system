import time
from orders import get_ltp

def run_paper_engine(obj, symbol, token, exchange, qty, side, entry_price,
                     sl_points=10, target_points=20, trail_points=5):

    print("\n🟡 PAPER ENGINE STARTED\n")

    if side == "BUY":
        sl = entry_price - sl_points
        target = entry_price + target_points
    else:
        sl = entry_price + sl_points
        target = entry_price - target_points

    last_trail_price = entry_price

    print(f"ENTRY  : {entry_price}")
    print(f"SL     : {sl}")
    print(f"TARGET : {target}\n")

    try:
        while True:
            time.sleep(2)
            ltp = get_ltp(obj, exchange, symbol, token)

            # trailing SL
            if side == "BUY" and ltp >= last_trail_price + trail_points:
                sl += trail_points
                last_trail_price = ltp
                print(f"\n🔁 PAPER SL TRAILED → {sl}")

            pnl = (ltp - entry_price) * qty if side == "BUY" else (entry_price - ltp) * qty

            print(
                f"\r{symbol} | LTP:{ltp:.2f} | SL:{sl:.2f} | "
                f"TARGET:{target:.2f} | P&L:{pnl:.2f}        ",
                end=""
            )

            if side == "BUY" and (ltp <= sl or ltp >= target):
                print("\n🏁 PAPER EXIT")
                break

    except KeyboardInterrupt:
        print("\n🛑 PAPER ENGINE STOPPED")
