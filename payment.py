import hmac
import hashlib
import base64
from urllib.parse import urlencode

FONDY_MERCHANT_ID = "YOUR_MERCHANT_ID"
FONDY_SECRET = "YOUR_SECRET_KEY"

# створення платіжного посилання
def create_payment_link(user_id: int, amount=49, currency="UAH", desc="Підписка на ЮрБот"):
    order_id = f"sub-{user_id}"

    data = {
        "merchant_id": FONDY_MERCHANT_ID,
        "order_id": order_id,
        "amount": str(amount * 100),  # у копійках
        "currency": currency,
        "order_desc": desc,
        "response_url": "https://yourbot.com/payment_callback",
        "lang": "uk",
    }

    # Генеруємо підпис
    signature = sign_fondy(data, FONDY_SECRET)
    data["signature"] = signature

    base_url = "https://pay.fondy.eu/api/checkout/redirect/"
    query_string = urlencode(data)
    return f"{base_url}?{query_string}"

def sign_fondy(data: dict, secret: str):
    # Підпис за схемою Fondy
    keys = sorted(k for k in data if k != "signature")
    to_sign = "|".join(str(data[k]) for k in keys)
    return base64.b64encode(
        hashlib.sha1((secret + to_sign).encode()).digest()
    ).decode()
