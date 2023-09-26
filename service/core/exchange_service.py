from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set
    
    
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
   
   
class ExchangeService(ABC):
    @abstractmethod
    def support_market(self, market_id: str, use_cached: bool = True) -> bool:
        pass

    @abstractmethod
    def get_markets(self, use_cached: bool = True) -> Set[str]:
        pass
    