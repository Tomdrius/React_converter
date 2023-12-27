import os
import time
import threading
import traceback
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Float, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import schedule

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = 'exchange_rates'

    id = Column(Integer, primary_key=True)
    currency = Column(String(3), nullable=False)
    rate = Column(Float, nullable=False)

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER', 'DB_USER')}:{os.getenv('DB_PASSWORD', 'DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME', 'DB_NAME')}"
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@app.route('/', methods=['GET'])
def home():
    return "Hello, this is the backend!"

def fetch_and_save_data():
    try:
        response = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = response.json()

        rates = {rate['code']: rate['mid'] for rate in data[0]['rates'] if rate['code'] in ['USD', 'EUR']}

        session = Session()

        for currency, rate in rates.items():
            new_rate = ExchangeRate(currency=currency, rate=rate)
            session.add(new_rate)

        session.commit()
        session.close()

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
        session = Session()
        rates = session.query(ExchangeRate.currency, ExchangeRate.rate).all()
        session.close()

        rates_dict = {currency: rate for currency, rate in rates}
        return rates_dict

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
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', 'localhost')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))

    app.run(debug=True, host=host, port=port)