This project is a currency converter. It consists of two parts:

App.js - a React component that displays the user interface.
Backend.py - a Flask application that provides currency exchange rates.

Running

Create and activate a virtual environment:
python3 -m venv nbp
source nbp/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the Flask application:
python backend.py

Run the React application:
npm install
npm start

The application will be available at http://localhost:3000 (frontend) and http://localhost:5000 (backend).

Running in a Docker container

The application can also be run in a Docker container. To do this, create a Docker image by running the following command:

docker build -t ccbackend:first . -f Dockerfile.python
docker build -t ccfrontend:second . -f Dockerfile.node
Then, run the Docker container by running the following command:

docker compose up
The application will be available at http://localhost:3000 and http://localhost:5000.

==========================================================

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

Aplikację można również uruchomić w kontenerze Dockera. Aby to zrobić, utwórz obraz Dockera, wykonując następujące polecenie:

docker build -t ccbackend:first . -f Dockerfile.python
docker build -t ccfrontend:second . -f Dockerfile.node

Następnie uruchom kontener Dockera, wykonując następujące polecenie:

docker compose up

Aplikacja będzie dostępna pod adresem http://localhost:3000 i http://localhost:5000.