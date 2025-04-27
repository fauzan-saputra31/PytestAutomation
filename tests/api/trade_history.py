import time
import requests
from urllib.parse import urlencode
from config import BASE_URI, API_KEY
from tests.util import authentication


class TradeHistory:
    def __init__(self):
        self.base_url = BASE_URI
        self.headers = {'X-MBX-APIKEY': API_KEY}
        self.params = {'timestamp': int(time.time() * 1000)}
        self.endpoint = '/api/v3/myTrades'

    def get_trade_history(self, symbol):
        self.params['symbol'] = symbol
        self.params['signature'] = authentication.create_signature(urlencode(self.params))
        return requests.get(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    def get_trade_history_by_id(self, symbol, order_id):
        self.params['symbol'] = symbol
        self.params['orderId'] = order_id
        self.params['signature'] = authentication.create_signature(urlencode(self.params))
        return requests.get(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    @staticmethod
    def get_trade_history_schema():
        return {
            'symbol': {'type': 'string'},
            'id': {'type': 'integer', 'min': 1},
            'orderId': {'type': 'integer', 'min': 1},
            'orderListId': {'type': 'integer', 'default': -1},
            'price': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'qty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'quoteQty': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'commission': {'type': 'string', 'regex': '^[0-9]+\\.[0-9]{8}$'},
            'commissionAsset': {'type': 'string'},
            'time': {'type': 'integer', 'min': 1_000_000_000},
            'isBuyer': {'type': 'boolean'},
            'isMaker': {'type': 'boolean'},
            'isBestMatch': {'type': 'boolean'}
        }
