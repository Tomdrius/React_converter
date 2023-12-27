import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
for key in ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']:
    if not os.getenv(key):
        raise Exception(f"Zmienna środowiskowa {key} nie jest ustawiona")
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
        print('Połączenie z bazą danych zostało nawiązane pomyślnie.')

        # Sprawdź, czy użytkownik może się zalogować
        cursor.execute("SELECT rolname FROM pg_roles WHERE rolname = %s", (os.getenv('DB_USER'),))
        user_data = cursor.fetchone()
        user = os.getenv('DB_USER')
        if user_data is not None:
            print(f'Użytkownik {user} istnieje w bazie danych.')
        else:
            print('Użytkownik NIE istnieje w bazie danych.')

    else:
        print('Nie udało się połączyć z bazą danych.')

    connection.close()
except Exception as e:
    print(f'Błąd podczas łączenia z bazą danych: {str(e)}')

