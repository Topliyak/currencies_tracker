from flask import Flask, request

from service.app import (
	get_best_price,
	get_average_price
)


app = Flask(__name__)


@app.route('/best_price', methods=['GET'])
def best_price():
    market_id = request.args.get('market_id')
    best_price = get_best_price(market_id)
    
    return best_price


@app.route('/average_price')
def average_price():
    market_id = request.args.get('market_id')
    average_price = get_average_price(market_id)
    
    return average_price
