from typing import Dict, List
from functools import reduce

from .binance import binance
from .garantex import garantex

from .core.exchange_service import (
    ExchangeService,
    BestPriceSource, BestPrice,
    AveragePriceSource, AveragePrice,
)


SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR = True

names_and_exchange_services: Dict[str, ExchangeService] = {
    'binance': binance,
    'garantex': garantex
}


def _filter_exchange_services(interface: type = None, support_market_id: str = None):
    snames = names_and_exchange_services.keys()
    
    if interface is not None:
        func = lambda name: isinstance(names_and_exchange_services[name], interface)
        snames = list(filter(func, snames))
        
    if support_market_id is not None:
        try:
            func = lambda name: names_and_exchange_services[name].support_market(support_market_id)
            snames = list(filter(func, snames))
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e
        
    return {name: names_and_exchange_services[name] for name in snames}


def get_best_price(market_id) -> Dict[str, BestPrice]:
    names_and_best_price_sources: Dict[str, BestPriceSource]
    
    names_and_best_price_sources = _filter_exchange_services(
        interface=BestPriceSource,
        support_market_id=market_id
    )

    res = {}
    
    for name, bp_source in names_and_best_price_sources.items():
        try:
            res[name] = bp_source.get_best_price(market_id)
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e
        
    return res


def get_average_price(market_id) -> Dict[str, AveragePrice]:
    names_and_avg_price_sources: Dict[str, AveragePriceSource]
    
    names_and_avg_price_sources = _filter_exchange_services(
        interface=AveragePriceSource,
        support_market_id=market_id
    )
            
    res = {}
    
    for name, avgp_source in names_and_avg_price_sources.items():
        try:
            res[name] = avgp_source.get_average_price(market_id)
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e
        
    return res


def get_markets(services_names = None):
    markets: Dict[str, List[str]] = {}

    services_names = services_names or names_and_exchange_services.keys()

    for service_name in services_names:
        if service_name not in names_and_exchange_services:
            raise ValueError(f'Service {service_name} is not supported')
        
        service = names_and_exchange_services[service_name]
        
        new_markets = []
        
        try:
            new_markets = service.get_markets()
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e

        for new_market in new_markets:
            if new_market in markets:
                markets[new_market].append(service_name)
                continue

            markets[new_market] = [service_name]

    return markets


def get_exchange_services():
    return list(names_and_exchange_services.keys())
