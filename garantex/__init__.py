from exchange_service import AveragePrice
from exchange_service import (
    ExchangeService,
    AveragePriceSource, AveragePrice
)

from .garantex_api_requests import (
    get_trades, 
    get_markets
)

from .utils import get_average_price_from_trades

from decimal import Decimal


class Garantex(ExchangeService, 
               AveragePriceSource):
    
    def support_market(self, market_id: str) -> bool:
        market_ids = [m.id for m in get_markets()]
        market_id_in_garantex_format = market_id.lower()
        
        return market_id_in_garantex_format in market_ids
    
    def get_average_price(self, market_id: str) -> AveragePrice:
        market_id_in_garantex_format = market_id.lower()
        trades = get_trades(market_id_in_garantex_format, count=50)
        avg = get_average_price_from_trades(trades)
        
        return avg
        
        
garantex = Garantex()
