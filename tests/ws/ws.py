import json
import pytest
import websockets

from config import WS_BASE_URI
from tests.api.order import Order


class Ws:
    def __init__(self):
        self.base_url = WS_BASE_URI

    async def subscribe_order_book_stream(self, symbol):
        async with websockets.connect(self.base_url + symbol + '@depth') as websocket:
            message = await websocket.recv()
            data = json.loads(message)
            print(data)
            return data

    @staticmethod
    def get_ws_order_book_stream_schema():
        return {
            'e': {'type': 'string'},
            'E': {'type': 'integer'},
            's': {'type': 'string'},
            'U': {'type': 'integer'},
            'u': {'type': 'integer'},
            'b': {'type': 'list',
                  'schema': {'type': 'list', 'schema': {'type': 'string'}, 'minlength': 2, 'maxlength': 2}},
            'a': {'type': 'list',
                  'schema': {'type': 'list', 'schema': {'type': 'string'}, 'minlength': 2, 'maxlength': 2}},
        }

    async def subscribe_trade_stream(self, symbol):
        async with websockets.connect(self.base_url + symbol + '@trade') as websocket:
            message = await websocket.recv()
            data = json.loads(message)
            print(data)
            return data

    @staticmethod
    def get_ws_trade_stream_schema():
        return {
            'e': {'type': 'string'},
            'E': {'type': 'integer'},
            's': {'type': 'string'},
            't': {'type': 'integer'},
            'p': {'type': 'string'},
            'q': {'type': 'string'},
            'b': {'type': 'integer'},
            'a': {'type': 'integer'},
            'T': {'type': 'integer'},
            'm': {'type': 'boolean'},
            'M': {'type': 'boolean'},
        }

    async def subscribe_user_data_stream(self, listen_key):
        async with websockets.connect(self.base_url + listen_key) as websocket:
            order = Order()
            order.place_market_order('BNBUSDT', 'BUY', 1, 'MARKET')
            message = await websocket.recv()
            data = json.loads(message)
            return data
