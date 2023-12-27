import psycopg2

database_name = 'exchange_rates'

def create_tables():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='P:><kol86',
            host='localhost',
            port=5432
        )

        print('Zalogowano się do PostgreSQL')
    except psycopg2.Error as e:
        print('Nie udało się zalogować do PostgreSQL')

    
    # Create a cursor object
    cursor = connection.cursor()
    try:
        connection.commit()
    except psycopg2.DatabaseError as e:
        connection.rollback()
        raise e
    # cursor.execute(f'CREATE DATABASE {database_name};')
    # cursor.execute('CREATE USER baza WITH PASSWORD \'password\';')
    # cursor.execute('ALTER ROLE baza CREATEROLE;')
    cursor.execute('GRANT CREATE ON SCHEMA public TO baza;')
    cursor.execute('GRANT ALL ON SEQUENCE exchange_rates_id_seq to baza;')
    cursor.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON exchange_rates TO baza;')
    # cursor.execute('DROP TABLE IF EXISTS exchange_rates;')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()







