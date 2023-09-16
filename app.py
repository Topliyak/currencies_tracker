from typing import Dict

from binance import binance
from garantex import garantex

from exchange_service import (
    ExchangeService,
    BestPriceSource,
    AveragePriceSource
)


names_and_exchange_services: Dict[str, ExchangeService] = {
    'binance': binance,
    'garantex': garantex
}


def _filter_exchange_services(interface: type = None, support_market_id: str = None):
    snames = names_and_exchange_services.keys()
    
    if interface is not None:
        func = lambda name: isinstance(names_and_exchange_services[name], interface)
        snames = filter(func, snames)
        
    if support_market_id is not None:
        func = lambda name: names_and_exchange_services[name].support_market(support_market_id)
        snames = filter(func, snames)
        
    return {name: names_and_exchange_services[name] for name in snames}


def get_best_price(market_id):
    names_and_best_price_sources: Dict[str, BestPriceSource]
    
    names_and_best_price_sources = _filter_exchange_services(
        interface=BestPriceSource,
        support_market_id=market_id
    )
            
    res = {}
    
    for name, bp_source in names_and_best_price_sources.items():
        res[name] = bp_source.get_best_price(market_id)
        
    return res


def get_average_price(market_id):
    names_and_avg_price_sources: Dict[str, AveragePriceSource]
    
    names_and_avg_price_sources = _filter_exchange_services(
        interface=AveragePriceSource,
        support_market_id=market_id
    )
            
    res = {}
    
    for name, avgp_source in names_and_avg_price_sources.items():
        res[name] = avgp_source.get_average_price(market_id)
        
    return res
