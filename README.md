# MoveMind AI

MoveMind AI ar en enkel webbaserad halsocoach som anvander generativ AI for att ge allmanna tips om rorelse, motivation, somn, stress och vardagshalsa.

Appen ar byggd med Python och Flask. AI-delen anvander Groq API.

## Funktioner

- Anvandaren fyller i alder, mal, aktivitetsniva och eventuella begransningar.
- Appen skickar informationen till en AI-modell.
- AI skapar en enkel och personlig halsoplan.
- Appen visar en sakerhetsnotis om att den inte ersatter lakare.

## Starta lokalt

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="din-api-nyckel"
python app.py
```

Oppna sedan:

```text
http://127.0.0.1:5000
```

## Hosta pa AWS EC2

1. Skapa en EC2-instans med Ubuntu eller Amazon Linux.
2. Installera Python, pip och Git.
3. Ladda upp projektet eller klona det fran GitHub.
4. Installera kraven med `pip install -r requirements.txt`.
5. Satt miljovariabeln `GROQ_API_KEY`.
6. Starta appen med `python app.py`.
7. Oppna port 5000 eller koppla appen till port 80 med Nginx/Apache.

## Viktigt

MoveMind AI ger endast allmanna halsotips. Den ersatter inte lakare, fysioterapeut eller sjukvard.
