FROM python:3.7-slim-buster
LABEL maintainer='hello@odwyer.software'

RUN apt-get update && apt-get install -y --no-install-recommends git gcc \
libc6-dev build-essential libcurl4-openssl-dev libssl-dev && \
rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py

COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt
ADD . /opt/app
WORKDIR /opt/app
ENV PYTHONPATH='${PYTHONPATH}:.'
EXPOSE 8080
CMD find /src/**/* -name .git -type d -exec rm -rf {} +
ENTRYPOINT ['run.sh']
