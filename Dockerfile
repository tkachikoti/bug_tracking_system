FROM python:3.7.2-slim

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -- upgrade flask
RUN pip install --upgrade Flask-WTF
RUN pip install --upgrade pytest
RUN pip install --upgrade numpy


ENTRYPOINT ["python", "app.py"]