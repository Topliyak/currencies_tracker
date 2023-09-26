from typing import Set, Optional

from service.core.exchange_service import (
    ExchangeService,
    AveragePriceSource, AveragePrice
)

from .garantex_api_requests import (
    get_trades, 
    get_markets
)

from .utils import get_average_price_from_trades


class Garantex(ExchangeService, 
               AveragePriceSource):
    
    _supported_markets: Optional[Set[str]] = None
    
    def support_market(self, market_id: str, use_cached: bool = True) -> bool:
        if use_cached is False:
            self._update_markets()

        if self._supported_markets is None:
            self._update_markets()
        
        return market_id.upper() in self._supported_markets

    def get_markets(self, use_cached: bool = True) -> Set[str]:
        if use_cached is False:
            self._update_markets()

        if self._supported_markets is None:
            self._update_markets()

        return self._supported_markets.copy()

    def _update_markets(self):
        self._supported_markets = {m.id.upper() for m in get_markets()}
    
    def get_average_price(self, market_id: str) -> AveragePrice:
        market_id_in_garantex_format = market_id.lower()
        trades = get_trades(market_id_in_garantex_format, count=50)
        avg = get_average_price_from_trades(trades)
        
        return avg
        
        
garantex = Garantex()
