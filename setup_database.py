# The provided code connects to a PostgreSQL database server using the psycopg2 library, retrieves database configuration parameters from environment variables, and attempts to create a new database. The script checks whether the specified database already exists. The connection is set to autocommit mode, and any exceptions that occur during the process are caught and printed. The database creation process is encapsulated in a function called create_database, which is invoked when the script is executed.
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

def create_database():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=5432,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres',
        )

        cursor = connection.cursor()

        connection.set_session(autocommit=True)

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        database_exists = cursor.fetchone() is not None

        if not database_exists:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

    except Exception as e:
        print(f"Error creating database: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    create_database()