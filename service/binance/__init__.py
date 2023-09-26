from typing import Set, Optional

from service.core.exchange_service import (
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

    _supported_markets: Optional[Set] = None
    
    def support_market(self, market_id: str, use_cached: bool = True) -> bool:
        if use_cached is False:
            self._update_markets()

        if self._supported_markets is None:
            self._update_markets()
        
        return market_id in self._supported_markets

    def get_markets(self, use_cached: bool = True) -> Set[str]:
        if use_cached is False:
            self._update_markets()

        if self._supported_markets is None:
            self._update_markets()

        return self._supported_markets.copy()

    def _update_markets(self):
        self._supported_markets = set(get_markets_ids())
    
    def get_best_price(self, market_id: str) -> BestPrice:
        best_price = get_best_price(market_id)
        return best_price
    
    def get_average_price(self, market_id: str) -> AveragePrice:
        average_price = get_average_price(market_id)
        return average_price
    

binance = Binance()
