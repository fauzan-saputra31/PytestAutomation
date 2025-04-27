import json
import pytest
import requests
import websockets
from assertpy.assertpy import assert_that
from cerberus import Validator
from config import WS_BASE_URI
from tests.api.account import Account
from tests.api.open_order import OpenOrder
from tests.api.order import Order
from tests.api.order_book import OrderBook
from tests.api.trade_history import TradeHistory
from tests.util.file_reader import read_file
from tests.ws.ws import Ws

# get test data from json file in the data folder
@pytest.fixture
def symbol_data():
    data = read_file('symbols.json')
    yield data


@pytest.fixture
def order_data():
    data = read_file('order.json')
    yield data

# ============================= rest api tests =============================
# test user place a buy market order success and order is reflected in account balance and trade history
def test_e2e_market_order(order_data):
    # get initial account balance
    account = Account()
    account_information = account.get_account_information()
    assert_that(account_information.status_code).is_equal_to(requests.codes.ok)
    entry_balance = 0
    for balance in account_information.json()['balances']:
        if balance['asset'] == order_data['asset']:
            entry_balance = balance['free']
    print('entry balance: ' + entry_balance + "\n")

    # make a market order
    order = Order()
    placed_order = order.place_market_order(order_data['symbol'], order_data['side'], order_data['quantity'], 'MARKET')
    print('placed order: ' + str(placed_order.request.url) + "\n")
    assert_that(placed_order.status_code).is_equal_to(requests.codes.ok)
    order_id = placed_order.json()['orderId']
    assert_that(order_id).is_not_none()
    print('order id: ' + str(order_id) + "\n")

    # check last account balance
    acc = Account()
    account_information = acc.get_account_information()
    print('account information: ' + str(account_information.request.url) + "\n")
    assert_that(account_information.status_code).is_equal_to(requests.codes.ok)
    last_balance = 0
    for balance in account_information.json()['balances']:
        if balance['asset'] == order_data['asset']:
            last_balance = balance['free']
    print('last balance: ' + last_balance + "\n")
    assert_that(float(last_balance)).is_greater_than(float(entry_balance))

    # check trade history
    trade_history = TradeHistory()
    trade_hist = trade_history.get_trade_history_by_id(order_data['symbol'], order_id)
    print('trade hist: ' + str(trade_hist.json()) + "\n")
    assert_that(trade_hist.status_code).is_equal_to(requests.codes.ok)
    assert_that(trade_hist.json()[0]['orderId']).is_equal_to(order_id)


# test fetching the account balances account information
def test_fetch_account_balance():
    # send request account information
    account = Account()
    response = account.get_account_information()
    # assert http code success
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    # assert account balance should not be none
    assert_that(response.json()['balances']).is_not_none()
    # assert response json schema
    assert_that(Validator(account.get_account_schema()).validate(response.json())).is_true()


def test_order_book(symbol_data):
    order_book = OrderBook()
    response = order_book.get_order_book(symbol_data['symbol'])
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(Validator(order_book.get_order_book_schema()).validate(response.json())).is_true()


def test_place_a_limit_order(order_data):
    order = Order()
    response = order.place_limit_order(order_data['symbol'], order_data['side'], order_data['type'],
                                  order_data['timeInForce'], order_data['quantity'], order_data['price'])
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response.json()['orderId']).is_not_none()
    assert_that(Validator(order.get_order_schema()).validate(response.json())).is_true()

def test_fetch_open_orders(order_data):
    open_order = OpenOrder()
    response = open_order.get_open_orders()
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    if response.json() is not None:
        for resp in response.json():
            assert_that(Validator(open_order.get_open_order_chema()).validate(resp)).is_true()

def test_fetch_trade_history(symbol_data):
    trade_history = TradeHistory()
    response = trade_history.get_trade_history(symbol_data['symbol'])
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    if response.json() is not None:
        for resp in response.json():
            assert_that(Validator(trade_history.get_trade_history_schema()).validate(resp)).is_true()

# ============================= websocket tests =============================
@pytest.mark.asyncio
async def test_subscribe_order_book():
    ws = Ws()
    data = await ws.subscribe_order_book_stream('btcusdt')
    assert_that(data['s']).is_equal_to('BTCUSDT')
    assert_that(Validator(ws.get_ws_order_book_stream_schema()).validate(data)).is_true()

@pytest.mark.asyncio
async def test_subscribe_trade_stream():
    ws = Ws()
    data = await ws.subscribe_trade_stream('btcusdt')
    assert_that(data['s']).is_equal_to('BTCUSDT')
    assert_that(Validator(ws.get_ws_trade_stream_schema()).validate(data)).is_true()

@pytest.mark.asyncio
async def test_subscribe_user_data_stream():
    account = Account()
    listen_key = account.get_user_data_listen_key().json()['listenKey']
    ws = Ws()
    data = await ws.subscribe_user_data_stream(listen_key)
    assert_that(data['e']).is_equal_to('executionReport')

# @pytest.mark.asyncio
# async def test_subscribe_order_book():
#     async with websockets.connect(WS_BASE_URI + 'bnbusdt' + '@depth') as websocket:
#         message = await websocket.recv()
#         data = json.loads(message)
#         print(data)
#         assert_that(data['s']).is_equal_to('x')