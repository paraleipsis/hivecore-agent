FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /hivecore-agent

RUN apk update
RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r /hivecore-agent/requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/hivecore-agent/src"

LABEL maintainer="paralepsis <der.krabbentaucher@gmail.com>"