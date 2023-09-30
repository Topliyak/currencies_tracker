from typing import Dict, List, Optional, Iterable

from .binance import binance
from .garantex import garantex
from .apilayer import apilayer

from .core.exchange_service import (
    ExchangeService,
    BestPriceSource, BestPrice,
    AveragePriceSource, AveragePrice,
    LiveRateSource, PairRate,
)


SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR = True

names_and_exchange_services: Dict[str, ExchangeService] = {
    'binance': binance,
    'garantex': garantex,
    'apilayer': apilayer,
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
    markets: Dict[str, Iterable[str]] = {}

    services_names = services_names or names_and_exchange_services.keys()

    for service_name in services_names:
        service = names_and_exchange_services[service_name]
        
        try:
            markets[service_name] = service.get_markets()
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e

    return markets


def get_exchange_services():
    return list(names_and_exchange_services.keys())


def get_live_rates(source: str):
    names_and_live_rate_sources: Dict[str, LiveRateSource]
    
    names_and_live_rate_sources = _filter_exchange_services(
        interface=LiveRateSource,
    )

    res: Dict[str, List[PairRate]] = {}

    for serv_name, service in names_and_live_rate_sources.items():
        try:
            res[serv_name] = service.get_lives(source_id=source)                
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e

    return res


def get_live_rate(market: str):
    names_and_live_rate_sources: Dict[str, LiveRateSource]
    
    names_and_live_rate_sources = _filter_exchange_services(
        interface=LiveRateSource,
    )

    res: Dict[str, PairRate] = {}

    for serv_name, service in names_and_live_rate_sources.items():
        try:
            res[serv_name] = service.get_live(market_id=market)                
        except Exception as e:
            if SKIP_EXCHANGE_SERVICE_IF_RAISE_ERROR is False:
                raise e

    return res
