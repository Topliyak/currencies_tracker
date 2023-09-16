from exchange_service import (
    ExchangeService,
    BestPriceSource, BestPrice, 
    AveragePriceSource, AveragePrice
)

from .binance_api_requests import (
    get_best_price,
    get_average_price, 
    get_markets_ids
)


class Binance(ExchangeService,
              BestPriceSource, 
              AveragePriceSource):
    
    def support_market(self, market_id: str) -> bool:
        market_ids = get_markets_ids()
        return market_id in market_ids
    
    def get_best_price(self, market_id: str) -> BestPrice:
        best_price = get_best_price(market_id)
        return best_price
    
    def get_average_price(self, market_id: str) -> AveragePrice:
        average_price = get_average_price(market_id)
        return average_price
    

binance = Binance()
