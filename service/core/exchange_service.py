from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set, List
    
    
@dataclass
class BestPrice:
    ask_price:  str
    ask_qty:    str
    bid_price:  str
    bid_qty:    str


class BestPriceSource(ABC):
    @abstractmethod
    def get_best_price(self, market_id: str) -> BestPrice:
        pass
    
    
@dataclass
class AveragePrice:
    mins:   int
    price:  str
    
    
class AveragePriceSource(ABC):
    @abstractmethod
    def get_average_price(self, market_id: str) -> AveragePrice:
       pass


@dataclass
class PairRate:
    market: str
    rate: str


class LiveRateSource(ABC):
    @abstractmethod
    def get_live(self, market_id: str) -> PairRate:
        pass

    @abstractmethod
    def get_lives(self, source_id: str) -> List[PairRate]:
        pass


class ExchangeServiceNotSuccessResponse(Exception):
    pass
   
   
class ExchangeService(ABC):
    def support_market(self, market_id: str, use_cached: bool = True) -> bool:
        return market_id in self.get_markets(use_cached=use_cached)

    @abstractmethod
    def get_markets(self, use_cached: bool = True) -> Set[str]:
        pass
    