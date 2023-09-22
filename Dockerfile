FROM python:3.10.11-slim
LABEL maintainer="catsperr322@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR app/src/

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt

COPY . .

RUN adduser --disabled-password --no-create-home django-user

USER django-user
