import json
from typing import Any, Optional
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from datetime import datetime
from collections import deque

# import logging
# logger = logging.getLogger()
# config_logging(logging, logging.DEBUG)

API_KEY = ""
API_SECRET = ""
LOCAL_CURRENCY = "AUD"

with open('API Key.txt') as file:
    API_KEY, API_SECRET = [x.rstrip() for x in file]  # Read txt file to get API keys

client = Client(key = API_KEY, secret = API_SECRET)

def get_human_readable_date(date: int) -> datetime:
    return datetime.fromtimestamp(date/1000)

def convert_to_posix(human_date: str) -> int:
    '''
    Full code will parse input as DD-MM-YYYY and convert to POSIX time in milliseconds
    '''
    datetime_obj = datetime.strptime(human_date, '%d-%m-%Y')
    posixTime = datetime.timestamp(datetime_obj)

    return int(posixTime*1000)  # In ms

def get_bank_history(type: int, startTime: int, endTime:int):    # UID cost 90k   / 180k per min (so can easily go above limits)
    transfers = client.fiat_order_history(type, startTime=startTime, endTime=endTime)   # Gets DEPOSITS AND WITHDRAWS FROM BANK ACC
    return transfers

def get_fiat_payment_history(type: int, startTime: int, endTime: int):
    fiat_payments = client.fiat_payment_history(type, startTime=startTime, endTime=endTime)
    return fiat_payments

def exchange_info() -> json:
    response = client.exchange_info()
    return response

def get_acc_info():
    '''
    Gets the API key permissions and status
    '''
    response = client.account()
    api_perms = client.api_key_permissions()
    api_status = client.api_trading_status()
    return response

def acc_snapshot():
    '''
    Gets account snapshot for all SPOT assets

    '''
    response = client.account_snapshot("SPOT", limit=1)

    return response


def get_convert_history(startTime: int, endTime: int):
    response = client.convert_trade_history(startTime, endTime)
    return response

def dividend_over_timeframe(startTime: int, endTime: int, asset: Optional[str] = None) -> float:
    totalFiat = 0
    if asset:
        dividend_request = client.asset_dividend_record(startTime=startTime, endTime=endTime, asset=asset, limit=500)
        print("Asset specified")
    else:
        dividend_request = client.asset_dividend_record(startTime=startTime, endTime=endTime, limit=500)

    # with open('divident_request.json', 'w') as json_file:
    #     json.dump(dividend_request, json_file)
    for dividend_payout in dividend_request['rows']:
        current_asset = dividend_payout['asset']
        amount = float(dividend_payout['amount'])
        divTime = dividend_payout['divTime']
        start = divTime
        end = divTime + 60000
        print(current_asset + LOCAL_CURRENCY, start, end)
        # oneTrade, = client.agg_trades(asset+LOCAL_CURRENCY, startTime=startTime, endTime=endTime, limit=1)
        marketValue = get_fiat_market_value(current_asset, start, end)
        
        totalFiat += amount*marketValue

    return totalFiat

def get_fiat_market_value(asset: str, startTime: int, endTime: int) -> float:
    path = find_path(asset, LOCAL_CURRENCY)
    if path == "Symbol Not Found":
        return 0
    val = 1
    while len(path) > 2:
        # print(path[0]+path[1])
        val *= float(client.klines(path[0]+path[1], '1m', startTime=startTime, endTime=endTime)[0][1])
        # print(f"1 {path[0]} is worth {val} {path[1]}")
        path.pop(0)

    
    # Gets open value from the klines for the time staking reward was paid out.
    marketValue = val*float(client.klines(path[0]+path[1], '1m', startTime=startTime, endTime=endTime)[0][1])



    return marketValue

def find_path(base, quote):

    with open('symbol_graph.json') as file:

        symbols = json.load(file)
        stacc = deque()
        stacc.append([base])
        while(stacc):
            path = stacc.popleft()
            cur = path[-1]
            if cur not in symbols:
                return "Symbol Not Found"
            if quote in symbols[cur]:
                return path + [quote]
            for s in symbols[cur]:
                if s == cur:
                    continue
                else:
                    stacc.append(path+[s])





    return "No Valid Path"

def get_trades(symbol: str) -> any:
    response = client.my_trades(symbol)
    return response


# txnTypes = ["SUBSCRIPTION", "REDEMPTION", "INTEREST"]
# get_fiat_deposits()
# print(client.system_status())
# print(client.bnb_convertible_assets())
# print(client.account_snapshot("SPOT"))
# print((client.fiat_payment_history(0)))  # Gets stuff bought with fiat if left to ZERO
# Important for calculating capital gains at the end.


# print(client.staking_history('STAKING','INTEREST', asset='ALGO', startTime='1643634000000'))
# print(client.staking_product_list('STAKING',asset='ALGO'))


# print(totalFiat)
# client.convert_trade_history(1638316800000,1612137600000)
# print(client.asset_detail())  # GETS ALL AVAILABLE ASSETS ON BINANACE (USELESS FOR ME)
# client.rebate_spot_history(startTime=1642377600000, endTime=1645056000000)
# client.my_trades()

'''
1654508928000
1643634000000
'''