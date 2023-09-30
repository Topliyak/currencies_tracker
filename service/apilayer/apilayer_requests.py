import requests
import json
from typing import Set, Dict, Optional, List
from ..core.exchange_service import ExchangeServiceNotSuccessResponse
from os import environ


APIKEY = environ['APILAYER_APIKEY']


def get_currencies() -> Set[str]:
    url = 'https://api.apilayer.com/currency_data/list'

    heads = {
        'apikey': APIKEY
    }

    response = requests.get(url, headers=heads)

    if response.status_code != 200:
        raise ExchangeServiceNotSuccessResponse()

    response_dict = json.loads(response.text)
    currencies = {c for c in response_dict['currencies'].keys()}

    return currencies


def get_live_currency_rate(source: str, currencies: Optional[List] = None) -> Dict[str, str]:
    url = 'https://api.apilayer.com/currency_data/live'

    heads = {
        'apikey': APIKEY
    }

    source_param = 'source'
    currencies_param = 'currencies'

    params = {
        source_param: source,
    }

    if currencies is not None:
        params |= {currencies_param: ','.join(currencies)}

    response = requests.get(url, params, headers=heads)

    if response.status_code != 200:
        raise ExchangeServiceNotSuccessResponse()

    response_dict = json.loads(response.text)
    markets_and_rates = {market: str(rate) for market, rate in response_dict['quotes'].items()}

    return markets_and_rates
