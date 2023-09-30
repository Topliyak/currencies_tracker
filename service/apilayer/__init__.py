from ..core.exchange_service import (
    ExchangeService,
    LiveRateSource, PairRate,
)

from .apilayer_requests import (
    get_live_currency_rate,
    get_currencies,
)

from typing import List, Set, Optional


class APILayer(LiveRateSource,
               ExchangeService):

    _cached_markets: Optional[Set[str]] = None

    def get_markets(self, use_cached: bool = True) -> Set[str]:
        if use_cached is False:
            self._update_markets()

        if self._cached_markets is None:
            self._update_markets()

        return self._cached_markets.copy()

    def _update_markets(self) -> None:
        currencies = get_currencies()
        pairs = {src + curr for src in currencies for curr in currencies if src != curr}
        self._cached_markets = pairs

    def get_live(self, market_id: str) -> PairRate:
        src = market_id[:3]
        currency = market_id[3:]

        live = get_live_currency_rate(src, [currency])

        pair_rate = PairRate(
            market=market_id,
            rate=live[market_id]
        )

        return pair_rate

    def get_lives(self, source_id: str) -> List[PairRate]:
        lives = get_live_currency_rate(source=source_id)
        pairs: List[PairRate] = []

        for market, rate in lives.items():
            pairs.append(
                PairRate(
                    market=market,
                    rate=rate
                )
            )

        return pairs


apilayer = APILayer()
