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
    
    prices = []

    for trade in trades:
        if trade.price is None:
            break

        prices.append(Decimal(trade.price))

    if len(prices) == 0:
        raise ValueError('No data for calculate actual average price')
    
    avg = sum(prices) / len(prices)
    avg_str = str(avg)
    
    return AveragePrice(mins, avg_str)
