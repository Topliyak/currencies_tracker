from flask import Flask, request, Response

from service.app import (
	get_best_price,
	get_average_price
)

from .utils.different_formats import convert_to_format


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return """
                <a href="best_price?market_id=LTCBTC">best prices</a>
                <hr>
                <a href="average_price?market_id=USDTRUB">average prices</a>
    """


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
