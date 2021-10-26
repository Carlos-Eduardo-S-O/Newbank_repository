# syntax=docker/dockerfile:1
FROM python:3.10.0b2-buster
RUN mkdir /service
RUN mkdir /ssl_files
RUN mkdir /dictionaries
WORKDIR /service
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

