import requests

# 🔴 PUT YOUR DETAILS HERE
BOT_TOKEN = "8421759646:AAEeymOebI_BvTCPh9UIbZp0N0KBPDh81KY"
CHAT_ID = "5397388376"

def send_alert(message: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Telegram error: {e}")
