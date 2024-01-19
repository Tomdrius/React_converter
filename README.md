# This project is a currency converter. It consists of two parts:

App.js - a React component that displays the user interface.

Backend.py - a Flask application that provides currency rates.

## Running

1. Create and activate a virtual environment:
`python3 -m venv nbp`
`source nbp/bin/activate`

2. Install the dependencies: `pip install -r requirements.txt`

3. Run the Flask application: `python backend.py`
4. Run the React application:
`npm install`
`npm start`

5. The application will be available at http://localhost:3000 (frontend), and also at http://localhost:5000 (backend).

6. Creating containers using Docker

7. Build the container for the backend (Flask): `docker build -t backend -f Dockerfile.python .`

8. Build the container for the frontend (React): `docker build -t frontend -f Dockerfile.node .`

9. Build the container for the frontend (React): `docker build -t frontend -f Dockerfile.node .`

10. Run both containers: `docker compose up`

The application will be available at the previously mentioned addresses.

## Database:
The project uses a PostgreSQL database to store exchange rates. The database is automatically created when the application is run locally. To manually create the database, run the loggingDB.py file `python loggingDB.py`

## Rates saving:
Exchange rates are automatically fetched from the NBP API and saved to the database every 10 minutes.

## Information reading:
To read the saved rates from the database, use the appropriate API endpoints.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)

=======================================================

Ten projekt to konwerter walut. Składa się z dwóch części:

App.js - komponent React, który wyświetla interfejs użytkownika.
Backend.py - aplikacja Flask, która dostarcza kursów walut.

Uruchomienie

Utwórz i aktywuj środowisko wirtualne:
python3 -m venv nbp
source nbp/bin/activate

Zainstaluj zależności:
pip install -r requirements.txt

Uruchom aplikację Flask:
python backend.py

Uruchom aplikację React:
npm install
npm start

Aplikacja będzie dostępna pod adresem http://localhost:3000 (frontend),
a także pod adresem http://localhost:5000 (backend).

Tworzenie kontenerów za pomocą Dockera

Zbuduj kontener dla backendu (Flask):
docker build -t backend -f Dockerfile.python .

Zbuduj kontener dla frontendu (React):
docker build -t frontend -f Dockerfile.node .

Uruchom oba kontenery:
docker compose up

Aplikacja będzie dostępna pod wcześniej wspomnianymi adresami.

Baza danych:
Projekt korzysta z bazy danych PostgreSQL do przechowywania kursów walut. Baza danych jest automatycznie tworzona, gdy aplikacja jest uruchamiana lokalnie. Można ją ręcznie utworzyć uruchamiająć plik loggingDB.py.

Zapisywanie kursów:
Kursy walut są automatycznie pobierane z API NBP i zapisywane do bazy danych co 10 minut.

Odczytywanie informacji:
Aby odczytać zapisane kursy z bazy danych, użyj odpowiednich endpointów API.