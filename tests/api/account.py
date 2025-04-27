import time
import requests
from urllib.parse import urlencode
from config import BASE_URI, API_KEY
from tests.util import authentication

# Account API class
class Account:
    def __init__(self):
        self.base_url = BASE_URI
        self.headers = {'X-MBX-APIKEY': API_KEY}
        self.params = {'timestamp': int(time.time() * 1000)}
        self.endpoint = '/api/v3/account'

    # get account information with params timestamp and signature
    def get_account_information(self):
        self.params['signature'] = authentication.create_signature(urlencode(self.params))
        return requests.get(self.base_url + self.endpoint, params=self.params, headers=self.headers)

    # get account information response json schema
    @staticmethod
    def get_account_schema():
        return {
            'makerCommission': {'type': 'integer', 'required': True},
            'takerCommission': {'type': 'integer', 'required': True},
            'buyerCommission': {'type': 'integer', 'required': True},
            'sellerCommission': {'type': 'integer', 'required': True},
            'commissionRates': {
                'type': 'dict',
                'schema': {
                    'maker': {'type': 'string', 'required': True},
                    'taker': {'type': 'string', 'required': True},
                    'buyer': {'type': 'string', 'required': True},
                    'seller': {'type': 'string', 'required': True},
                },
                'required': True
            },
            'canTrade': {'type': 'boolean', 'required': True},
            'canWithdraw': {'type': 'boolean', 'required': True},
            'canDeposit': {'type': 'boolean', 'required': True},
            'brokered': {'type': 'boolean', 'required': True},
            'requireSelfTradePrevention': {'type': 'boolean', 'required': True},
            'preventSor': {'type': 'boolean', 'required': True},
            'updateTime': {'type': 'integer', 'required': True},
            'accountType': {'type': 'string', 'required': True},
            'balances': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'asset': {'type': 'string', 'required': True},
                        'free': {'type': 'string', 'required': True},
                        'locked': {'type': 'string', 'required': True},
                    }
                },
                'required': True
            },
            'permissions': {
                'type': 'list',
                'schema': {'type': 'string'},
                'required': True
            },
            'uid': {'type': 'integer', 'required': True}
        }
