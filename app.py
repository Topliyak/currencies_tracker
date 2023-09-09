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
class MarketRequests:
    timestamp: int
    asks: List[Price]
    bids: List[Price]


def get_markets() -> List[Market]:
    url = 'https://garantex.org/api/v2/markets'
    
    response = requests.get(url).text
    markets = [Market(**mdick) for mdick in json.loads(response)]
    
    return markets


def get_market_requests(market_id: str) -> MarketRequests:
    url = 'https://garantex.org/api/v2/depth'
    market_param = 'market'
    
    params = {market_param: market_id}
    response = requests.get(url, params)
    
    market_requests: MarketRequests = json.loads(response.text)
    
    return market_requests


markets = get_markets()
[get_market_requests(m.id) for m in markets]
