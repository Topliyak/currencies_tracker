from flask import Flask, request, Response
from .utils.different_formats import convert_to_format
from typing import Dict

from service.app import (
	get_best_price,
	get_average_price,
    get_markets,
    get_exchange_services,
    get_live_rates,
    get_live_rate,
)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return """
                <a href="best_price?market_id=LTCBTC">best prices for LTCBTC</a>
                <hr>
                <a href="average_price?market_id=USDTRUB">average prices for USDTRUB</a>
                <hr>
                <a href="markets">markets</a>
                <hr>
                <a href="exchange_services">exchange_services</a>
                <hr>
                <a href="lives?source=USD">live_rates for USD</a>
                <hr>
                <a href="live?market=USDRUB">live_rate for USDRUB</a>
    """


@app.route('/exchange_services', methods=['GET'])
def exchange_services():
    services = get_exchange_services()

    format = request.args.get('format') or 'json'
    response = convert_to_format(services, format)

    return response


@app.route('/markets', methods=['GET'])
def markets():
    services_arg = request.args.get('services')
    markets: Dict

    if services_arg is not None:
        services = services_arg.split(',')
        markets = get_markets(services)
    else:
        markets = get_markets()

    format = request.args.get('format') or 'json'
    response = convert_to_format(markets, format)

    return response


@app.route('/best_price', methods=['GET'])
def best_price():
    market_id = request.args.get('market_id')
    best_price = {serv: bp.__dict__ for serv, bp in get_best_price(market_id).items()}
    
    if len(best_price) == 0:
        return Response('There are not exchange services that responded', status=204)

    format = request.args.get('format') or 'json'
    response = convert_to_format(best_price, format)
    
    return response


@app.route('/average_price', methods=['GET'])
def average_price():
    market_id = request.args.get('market_id')
    average_price = {serv: ap.__dict__ for serv, ap in get_average_price(market_id).items()}
    
    if len(average_price) == 0:
        return Response('There are not exchange services that responded', status=204)

    format = request.args.get('format') or 'json'
    response = convert_to_format(average_price, format)
    
    return response


@app.route('/lives', methods=['GET'])
def live_rates():
    source = request.args['source']
    rates = get_live_rates(source)
    rates = {serv: [r.__dict__ for r in rates] for serv, rates in rates.items()}

    format = request.args.get('format') or 'json'
    response = convert_to_format(rates, format)

    return response


@app.route('/live', methods=['GET'])
def live_rate():
    market = request.args['market']
    rates = get_live_rate(market)
    rates = {serv: rate.__dict__ for serv, rate in rates.items()}

    format = request.args.get('format') or 'json'
    response = convert_to_format(rates, format)

    return response
