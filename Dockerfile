FROM python:3.8-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN apk update && apk upgrade
RUN apk add  git
RUN git --version
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
