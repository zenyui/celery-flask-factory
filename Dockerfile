FROM python:3.6-alpine3.7

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY server ./server/
COPY celery_worker.py ./
COPY cli.py ./