import hmac
import hashlib

from config import SECRET_KEY


def create_signature(message):
    return hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
