import time
import requests
from urllib.parse import urlencode
from config import BASE_URI, API_KEY
from tests.util import authentication


class Order:
    def __init__(self):
        self.base_url = BASE_URI
        self.headers = {'X-MBX-APIKEY': API_KEY}
        self.params = {'timestamp': int(time.time() * 1000)}
        self.endpoint = '/api/v3/order'

    def place_limit_order(self, symbol, side, order_type, time_in_force, quantity, price):
        self.params['symbol'] = symbol
        self.params['side'] = side
        self.params['type'] = order_type
        self.params['timeInForce'] = time_in_force
        self.params['quantity'] = quantity
        self.params['price'] = price
        self.params['signature'] = authentication.create_signature(urlencode(self.params))
        return requests.post(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    def place_market_order(self, symbol, side, quantity, order_type):
        self.params['symbol'] = symbol
        self.params['side'] = side
        self.params['type'] = order_type
        self.params['quantity'] = quantity
        self.params['signature'] = authentication.create_signature(urlencode(self.params))
        return requests.post(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    @staticmethod
    def get_order_schema():
        return {
            'symbol': {'type': 'string'},
            'orderId': {'type': 'integer'},
            'orderListId': {'type': 'integer'},
            'clientOrderId': {'type': 'string'},
            'transactTime': {'type': 'integer'},
            'price': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'origQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'executedQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'origQuoteOrderQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'cummulativeQuoteQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'status': {'type': 'string', 'allowed': ['NEW', 'PARTIALLY_FILLED', 'FILLED', 'CANCELED', 'REJECTED']},
            'timeInForce': {'type': 'string', 'allowed': ['GTC', 'IOC', 'FOK']},
            'type': {'type': 'string', 'allowed': ['LIMIT', 'MARKET', 'STOP_LOSS', 'TAKE_PROFIT']},
            'side': {'type': 'string', 'allowed': ['BUY', 'SELL']},
            'workingTime': {'type': 'integer'},
            'fills': {'type': 'list'},
            'selfTradePreventionMode': {'type': 'string', 'allowed': ['EXPIRE_MAKER', 'EXPIRE_TAKER', 'EXPIRE_BOTH']}
        }
