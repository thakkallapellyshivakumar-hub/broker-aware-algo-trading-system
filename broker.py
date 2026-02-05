from SmartApi import SmartConnect
import pyotp
from config import API_KEY, CLIENT_ID, MPIN, TOTP_SECRET

def angel_login():
    obj = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    session = obj.generateSession(CLIENT_ID, MPIN, totp)

    if not session or session.get("status") is False:
        raise Exception("Angel Login Failed")

    return obj
