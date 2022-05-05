FROM python:3.9-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY ./src /src
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /src

ENV FLASK_APP=Sudoku.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
