FROM python:3.10-slim-buster as pre-application

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install poetry
RUN python -m pip install --upgrade pip && pip install poetry==1.4.2

# App itself
RUN mkdir /app
WORKDIR /app

ADD pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false --local && poetry install --no-dev

ADD . /app/

COPY ./deployment/local/worker/start /start-worker
RUN sed -i 's/\r$//g' /start-worker
RUN chmod +x /start-worker

WORKDIR /app/sherlock
