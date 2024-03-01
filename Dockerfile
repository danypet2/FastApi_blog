FROM python:3.11

RUN mkdir /blog

WORKDIR /blog

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .