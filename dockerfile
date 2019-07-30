FROM ubuntu:18.04

RUN apt-get update && apt-get install

RUN apt-get install -y\
    git make build-essential python-dev\
    python-pip libssl-dev zlib1g-dev libbz2-dev\
    libreadline-dev libsqlite3-dev curl

RUN pip install virtualenv

WORKDIR /app

COPY  . /app

RUN pip install -r requirements.txt

EXPOSE 5672:5672

#RUN python task.py



