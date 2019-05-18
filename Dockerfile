FROM python:3.7.2

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --quiet --no-ansi
