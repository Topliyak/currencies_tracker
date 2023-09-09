import requests
import json

from typing import List
from dataclasses import dataclass


@dataclass
class Market:
    id: str
    name: str
    ask_unit: str
    bid_unit: str
    min_ask: str
    min_bid: str
    maker_fee: str
    taker_fee: str
    
    
@dataclass
class Price:
    price: str
    volume: str
    amount: str
    factor: str
    type: str
    
    
@dataclass
class Trade:
    """
        id
        price - цена
        volume - сумма в базовой валюте
        funds - сумма в валюте котировки
        market - id рынка
        created_at - время сделки
    """
    
    id: int
    price: str
    volume: str
    funds: str 
    market: str
    created_at: str


def get_markets() -> List[Market]:
    """ https://garantexio.github.io/?shell#47ff48632f """
    
    url = 'https://garantex.org/api/v2/markets'
    
    response = requests.get(url).text
    markets = [Market(**mdick) for mdick in json.loads(response)]
    
    return markets


def get_trades(market_id: str) -> List[Trade]:
    """ https://garantexio.github.io/?shell#f00f8079b3 """
    
    url = 'https://garantex.org/api/v2/trades'
    
    market_param = 'market'
    timestamp_param = 'timestamp'
    limit_param = 'limit'
    
    params = {
        market_param: market_id,
        limit_param: 10,
    }
    
    response = requests.get(url, params)
    
    trades = [Trade(**tdict) for tdict in json.loads(response.text)]
    
    return trades


if __name__ == '__main__':
    markets = get_markets()
    trades = {m.id: get_trades(m.id) for m in markets}
    
    for m_id, t in trades.items():
        print(m_id, t)
        print()
