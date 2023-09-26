from typing import List
from .garantex_api_requests import Trade
from service.core.exchange_service import AveragePrice
from decimal import Decimal


def get_average_price_from_trades(trades: List[Trade]) -> AveragePrice:
    times = list(map(lambda t: t.created_at, trades))
    first_moment = min(times)
    last_moment = max(times)
    mins = (last_moment - first_moment).total_seconds() // 60
    mins = round(mins)
    
    str_prices = map(lambda t: t.price, trades)
    prices = map(Decimal, str_prices)
    avg = sum(prices) / len(trades)
    avg_str = str(avg)
    
    return AveragePrice(mins, avg_str)
