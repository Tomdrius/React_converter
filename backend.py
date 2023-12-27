import os
import time
import threading
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import requests
import schedule

load_dotenv()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/', methods=['GET'])
def home():
    return "Hello, this is the backend!"


def fetch_and_save_data():
    try:
        response = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = response.json()

        rates = {rate['code']: rate['mid'] for rate in data[0]['rates'] if rate['code'] in ['USD', 'EUR']}
        
        connection = psycopg2.connect(
            host=os.getenv('FLASK_RUN_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            user=os.getenv('DB_USER', 'DB_USER'),
            password=os.getenv('DB_PASSWORD', 'DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'DB_NAME'),
        )

        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS exchange_rates (id SERIAL PRIMARY KEY, currency VARCHAR(3) NOT NULL, rate FLOAT NOT NULL);')

        for currency, rate in rates.items():
            cursor.execute("INSERT INTO exchange_rates (currency, rate) VALUES (%s, %s)", (currency, rate))
        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Błąd podczas pobierania i zapisywania danych: {str(e)}")

schedule.every(10).minutes.do(fetch_and_save_data)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(10)

schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

@app.route('/exchange-rates', methods=['GET'])
def get_exchange_rates():
    try:
        response = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = response.json()
        rates = {rate['code']: rate['mid'] for rate in data[0]['rates'] if rate['code'] in ['USD', 'EUR']}


        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            user=os.getenv('DB_USER', 'DB_USER'),
            password=os.getenv('DB_PASSWORD', 'DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'DB_NAME'),
        )
        cursor = connection.cursor()   
        cursor.execute('CREATE TABLE IF NOT EXISTS exchange_rates (id SERIAL PRIMARY KEY, currency VARCHAR(3) NOT NULL, rate FLOAT NOT NULL);')

        for currency, rate in rates.items():
            cursor.execute("INSERT INTO exchange_rates (currency, rate) VALUES (%s, %s)", (currency, rate))

        connection.commit()
        cursor.execute("SELECT currency, rate FROM exchange_rates")
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        rates = {currency: rate for currency, rate in data}
        return rates
    except Exception as e:
        print(f"Error in get_exchange_rates: {str(e)}")
        return {}

def convert_currency(target_currency: str, amount: float) -> float:
    try:
        rates = get_exchange_rates()

        if target_currency in rates:
            rate_target = rates[target_currency]
        else:
            raise KeyError(f"Currency code '{target_currency}' not found.")

        result = amount * rate_target
        return result
    
    except Exception as e:
        print(f"Error in convert_currency: {str(e)}")
        return 0.0

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        target_currency = data.get('targetCurrency')
        amount = data.get('amount')

        if not target_currency or not amount:
            raise ValueError("Missing required parameters")

        result = convert_currency(target_currency=target_currency, amount=float(amount))
        

        return jsonify({"result": result})
    except KeyError as ke:
        return jsonify({"error": f"KeyError: {str(ke)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', 'localhost')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))

    app.run(debug=False, host=host, port=port)