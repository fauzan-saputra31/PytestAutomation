import time
from json import dumps
from urllib.parse import urlencode
from uuid import uuid4
from assertpy.assertpy import assert_that
from config import BASE_URI, API_KEY
from tests.utils.file_reader import read_file
from tests.utils.authentication import create_signature


import requests


def test_fetch_account_balance():
    params = {
        'timestamp': int(time.time() * 1000)
    }
    headers = {
        'X-MBX-APIKEY': API_KEY,
    }
    params['signature'] = create_signature(urlencode(params))
    response = requests.get(BASE_URI+'/api/v3/account', params=params, headers=headers)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    response_text = response.json()
    print(response_text)
