import requests
import json
from typing import List, Iterable
from service.core.exchange_service import BestPrice, AveragePrice


def get_markets_ids() -> List[str]:
    """ https://binance-docs.github.io/apidocs/spot/en/#exchange-information """
    
    url = "https://api.binance.com/api/v3/exchangeInfo"
    
    response = requests.get(url)
    response_dict = json.loads(response.text)
    
    if 'code' in response_dict:
        raise ValueError(response_dict)
    
    markets_ids = [s['symbol'] for s in response_dict['symbols']]
    
    return markets_ids


def get_best_price(market_id: str) -> BestPrice:
    """ https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker """
    
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    
    market_param = 'symbol'
    
    params = {market_param: market_id}
    
    response = requests.get(url, params=params)
    response_dict = json.loads(response.text)
    
    if 'code' in response_dict:
        raise ValueError(response_dict)
    
    best_price = BestPrice(
        ask_price=response_dict['askPrice'],
        ask_qty=response_dict['askQty'],
        bid_price=response_dict['bidPrice'],
        bid_qty=response_dict['bidQty']
    )
    
    return best_price


def get_best_prices(*markets_ids: Iterable[str]) -> List[BestPrice]:
    """ https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker """
 
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    
    markets_param = 'symbols'
    
    markets_value = ','.join([f'"{market}"' for market in markets_ids])
    markets_value = f'[{markets_value}]'
    
    params = {markets_param: markets_value}
    
    response = requests.get(url, params=params)
    response_dict = json.loads(response.text)
    
    if 'code' in response_dict:
        raise ValueError(response_dict)
    
    best_prices = [BestPrice(**bp_dict) for bp_dict in response_dict]
    
    return best_prices


def get_average_price(market_id: str) -> AveragePrice:
    """ https://binance-docs.github.io/apidocs/spot/en/#current-average-price """
    
    url = 'https://api.binance.com/api/v3/avgPrice'
    
    market_param = 'symbol'
    
    params = {market_param: market_id}
    
    response = requests.get(url, params=params)
    response_dict = json.loads(response.text)
    
    if 'code' in response_dict:
        raise ValueError(response_dict)
    
    avg_price = AveragePrice(**response_dict)
    
    return avg_price
