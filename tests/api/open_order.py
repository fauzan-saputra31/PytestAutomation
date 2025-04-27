import time
import requests
from urllib.parse import urlencode
from config import BASE_URI, API_KEY
from tests.util import authentication


class OpenOrder:
    def __init__(self):
        self.base_url = BASE_URI
        self.headers = {'X-MBX-APIKEY': API_KEY}
        self.params = {'timestamp': int(time.time() * 1000)}
        self.endpoint = '/api/v3/openOrders'

    def get_open_orders(self):
        self.params['signature'] = authentication.create_signature(urlencode(self.params))
        return requests.get(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    @staticmethod
    def get_open_order_chema():
        return {
            'symbol': {'type': 'string'},
            'orderId': {'type': 'integer', 'min': 1},
            'orderListId': {'type': 'integer', 'default': -1},
            'clientOrderId': {'type': 'string', 'regex': '^[a-zA-Z0-9]{20,22}$'},
            'price': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'origQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'executedQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'cummulativeQuoteQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'status': {'type': 'string', 'allowed': ['NEW', 'PARTIALLY_FILLED', 'FILLED', 'CANCELED', 'REJECTED']},
            'timeInForce': {'type': 'string', 'allowed': ['GTC', 'IOC', 'FOK']},
            'type': {'type': 'string', 'allowed': ['LIMIT', 'MARKET', 'STOP_LOSS', 'TAKE_PROFIT']},
            'side': {'type': 'string', 'allowed': ['BUY', 'SELL']},
            'stopPrice': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'icebergQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'time': {'type': 'integer', 'min': 1_000_000_000},
            'updateTime': {'type': 'integer', 'min': 1_000_000_000},
            'isWorking': {'type': 'boolean'},
            'workingTime': {'type': 'integer', 'min': 1_000_000_000},
            'origQuoteOrderQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'selfTradePreventionMode': {'type': 'string', 'allowed': ['EXPIRE_MAKER', 'EXPIRE_TAKER', 'EXPIRE_BOTH']}
        }
