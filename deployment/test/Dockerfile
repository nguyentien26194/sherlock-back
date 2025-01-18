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

COPY ./deployment/test/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD /entrypoint.sh
