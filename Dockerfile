FROM python:3.8.3-alpine

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . /app
