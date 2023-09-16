import requests
import json
from datetime import datetime

from typing import List
from dataclasses import dataclass


@dataclass
class Market:
    id:         str
    name:       str
    ask_unit:   str
    bid_unit:   str
    min_ask:    str
    min_bid:    str
    maker_fee:  str
    taker_fee:  str
    
    
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
    
    id:         int
    price:      str
    volume:     str
    funds:      str 
    market:     str
    created_at: datetime


def get_markets() -> List[Market]:
    """ https://garantexio.github.io/?shell#47ff48632f """
    
    url = 'https://garantex.org/api/v2/markets'
    
    response = requests.get(url).text
    markets = [Market(**mdict) for mdict in json.loads(response)]
    
    return markets


def get_trades(market_id: str, count: int) -> List[Trade]:
    """ https://garantexio.github.io/?shell#f00f8079b3 """
    
    url = 'https://garantex.org/api/v2/trades'
    
    market_param = 'market'
    limit_param = 'limit'
    
    params = {
        market_param: market_id,
        limit_param: count,
    }
    
    response = requests.get(url, params)
    
    trades = []
    
    for tdict in json.loads(response.text):
        trades.append(Trade(
            id=tdict['id'],
            price=tdict['price'],
            volume=tdict['volume'],
            funds=tdict['funds'],
            market=tdict['market'],
            created_at=datetime.fromisoformat(tdict['created_at'])
        ))
    
    return trades


if __name__ == '__main__':
    markets = get_markets()
    trades = {m.id: get_trades(m.id, 10) for m in markets}
    
    for m_id, t in trades.items():
        print(m_id, t)
        print()
