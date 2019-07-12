FROM python:3.7.2

WORKDIR /app

COPY . /app

RUN pip install poetry --no-cache-dir --quiet --disable-pip-version-check

RUN poetry config settings.virtualenvs.create false

RUN poetry install --quiet --no-ansi
