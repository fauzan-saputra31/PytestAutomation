import pytest
import requests
from assertpy.assertpy import assert_that
from cerberus import Validator
from tests.api.account import Account
from tests.api.open_order import OpenOrder
from tests.api.order import Order
from tests.api.order_book import OrderBook
from tests.util.file_reader import read_file

account = Account()
open_order = OpenOrder()
order = Order()
order_book = OrderBook()


# get test data from json file in the data folder
@pytest.fixture
def symbols():
    data = read_file('symbols.json')
    yield data


@pytest.fixture
def order_data():
    data = read_file('order.json')
    yield data


# test fetching the account balances account information
def test_fetch_account_balance():
    # send request account information
    response = account.get_account_information()
    # assert http code success
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    # assert account balance should not be none
    assert_that(response.json()['balances']).is_not_none()
    # assert response json schema
    assert_that(Validator(account.get_account_schema()).validate(response.json())).is_true()


def test_order_book(symbols):
    response = order_book.get_order_book(symbols['symbol'])
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(Validator(order_book.get_order_book_schema()).validate(response.json())).is_true()


def test_place_a_limit_order(order_data):
    response = order.place_limit_order(order_data['symbol'], order_data['side'], order_data['type'],
                                  order_data['timeInForce'], order_data['quantity'], order_data['price'])
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response.json()['orderId']).is_not_none()
    assert_that(Validator(order.get_order_schema()).validate(response.json())).is_true()

def test_get_open_orders(order_data):
    response = open_order.get_open_orders()
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    for resp in response.json():
        assert_that(Validator(open_order.get_open_order_chema()).validate(resp)).is_true()

