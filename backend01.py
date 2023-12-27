import os
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS

from typing import Dict, Any, Optional

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/', methods=['GET'])
def home() -> str:
    return "Hello, this is the backend!"

@app.route('/exchange-rates', methods=['GET'])
def get_exchange_rates() -> Dict[str, float]:
    try:
        response = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = response.json()

        rates = {rate['code']: rate['mid'] for rate in data[0]['rates'] if rate['code'] in ['USD', 'EUR']}
        return jsonify(rates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/convert', methods=['POST'])
def convert_currency() -> Dict[str, Any]:
    try:
        data = request.get_json()
        target_currency: Optional[str] = data.get('targetCurrency')
        amount: float = data.get('amount')

        if not target_currency or not amount:
            raise ValueError("Missing required parameters")

        response = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = response.json()
        rates = {rate['code']: rate['mid'] for rate in data[0]['rates']}

        if target_currency not in rates:
            raise ValueError("Invalid currency code")

        rate_target = rates[target_currency]

        result = amount * rate_target
        

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.after_request
def after_request(response) -> requests.Response:
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', 'localhost')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))

    app.run(debug=True, host=host, port=port)