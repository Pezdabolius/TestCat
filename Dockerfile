FROM python:3.12.0-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . .