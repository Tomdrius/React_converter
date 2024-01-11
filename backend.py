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

DB_USER = os.environ.get('DB_USER')
DB_USER_PG = os.environ.get('DB_USER_PG')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PASSWORD_PG = os.environ.get('DB_PASSWORD_PG')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/', methods=['GET'])
def home():
    return "Hello, this is the backend!"

def connect_to_postgres(db_name=None, user=None, password=None):
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=user or DB_USER_PG,
        password=password or DB_PASSWORD_PG,
        database=db_name,
    )


def create_user_and_database():
    try:
        with connect_to_postgres() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM pg_user WHERE usename = '{DB_USER}';")
                user_exists = cursor.fetchone()

                if not user_exists:
                    cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
                    print(f"User '{DB_USER}' created successfully.")

                cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
                database_exists = cursor.fetchone()

                if not database_exists:
                    cursor.execute(f"CREATE DATABASE {DB_NAME} WITH OWNER = {DB_USER};")
                    print(f"Database '{DB_NAME}' created successfully.")

                connection.commit()

    except Exception as e:
        print(f"Error occured: {str(e)}")



def fetch_and_save_data():
    try:
        response = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = response.json()
        rates = {rate['code']: rate['mid'] for rate in data[0]['rates'] if rate['code'] in ['USD', 'EUR']}
        
        connection = connect_to_postgres(db_name=DB_NAME, user=DB_USER, password=DB_PASSWORD)

        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS exchange_rates (id SERIAL PRIMARY KEY, currency VARCHAR(3) NOT NULL, rate FLOAT NOT NULL);')

        for currency, rate in rates.items():
            cursor.execute("INSERT INTO exchange_rates (currency, rate) VALUES (%s, %s)", (currency, rate))
        
        connection.commit()
        cursor.execute("SELECT currency, rate FROM exchange_rates")

        cursor.close()
        connection.close()


    except Exception as e:
        print(f"An error occurred while fetching and saving data: {str(e)}")

def run_schedule():
    while True:
        try:
            fetch_and_save_data()
            time.sleep(600)
        except Exception as e:
            print(f"An error occurred while running the schedule: {str(e)}")
            time.sleep(5)

create_user_and_database()

schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

@app.route('/exchange-rates', methods=['GET'])
def get_exchange_rates():
    try:
        connection = connect_to_postgres(db_name=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        
        cursor = connection.cursor()   
        cursor.execute('CREATE TABLE IF NOT EXISTS exchange_rates (id SERIAL PRIMARY KEY, currency VARCHAR(3) NOT NULL, rate FLOAT NOT NULL);')

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
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))

    app.run(debug=False, host=host, port=port)