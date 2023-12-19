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

