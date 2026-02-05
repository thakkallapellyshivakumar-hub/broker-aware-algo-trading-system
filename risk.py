from config import SL_POINTS, TARGET_POINTS, TRAIL_POINTS
from telegram import send_alert

def calc_sl_target(entry):
    return entry - SL_POINTS, entry + TARGET_POINTS

def trail_sl(current_price, sl):
    if current_price - sl > TRAIL_POINTS:
        return current_price - TRAIL_POINTS
    return sl
