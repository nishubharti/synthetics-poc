# syntax=docker/dockerfile:1
FROM ubuntu:latest
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install git
# RUN apt-get -y install python3-dev
RUN apt-get -y install python3-pip
RUN git --version
# RUN apt-get -y install librdkafka-dev
RUN pip3 install -r requirements.txt
CMD ["python", "app.py"]
