# The provided code establishes a connection to a PostgreSQL database using the psycopg2 library, checks if the required environment variables for database configuration are set. Additionally, it verifies the existence of the specified user in the PostgreSQL database.
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
for key in ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']:
    if not os.getenv(key):
        raise Exception(f"Environment variable {key} is not set")
try:
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 5432)),
        user=os.getenv('DB_USER', 'DB_USER'),
        password=os.getenv('DB_PASSWORD', 'DB_PASSWORD'),
        dbname=os.getenv('DB_NAME', 'DB_NAME'),
    )

    cursor = connection.cursor()
    cursor.execute('SELECT 1;')
    data = cursor.fetchone()

    if data is not None:
        print('Database connection established successfully.')

        cursor.execute("SELECT rolname FROM pg_roles WHERE rolname = %s", (os.getenv('DB_USER'),))
        user_data = cursor.fetchone()
        user = os.getenv('DB_USER')
        if user_data is not None:
            print(f'User {user} exists in the database.')
        else:
            print('User DOES NOT exist in the database.')

    else:
        print('Failed to connect to the database.')

    connection.close()
except Exception as e:
    print(f'Error while connecting to the database: {str(e)}')