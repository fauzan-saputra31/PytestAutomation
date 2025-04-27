import requests
from config import BASE_URI, API_KEY


class OrderBook:
    def __init__(self):
        self.base_url = BASE_URI
        self.headers = {'X-MBX-APIKEY': API_KEY}
        self.params = {'symbol': ''}
        self.endpoint = '/api/v3/depth'

    def get_order_book(self, symbol):
        self.params['symbol'] = symbol
        return requests.get(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    @staticmethod
    def get_order_book_schema():
        return {
            'lastUpdateId': {'type': 'integer', 'required': True},
            'bids': {'type': 'list', 'required': True},
            'asks': {'type': 'list', 'required': True}
        }
