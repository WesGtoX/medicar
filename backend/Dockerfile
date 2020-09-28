FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt

COPY . /app/
