FROM python:3.7.2

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
