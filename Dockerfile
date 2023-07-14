FROM python:3.11.4-bullseye
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install git
RUN apt-get -y install python3-dev
# RUN apk -y add python3-pip
RUN git --version
RUN python3 --version
RUN apt-get -y install librdkafka-dev
COPY requirements.txt requirements.txt
RUN pip3 --version
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]