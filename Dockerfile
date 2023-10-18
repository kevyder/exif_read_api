FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache --virtual .tmp-build-deps

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Install Poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN apk del .tmp-build-deps

WORKDIR /app
COPY . /app/

RUN adduser -D user

RUN poetry install --no-root
USER user
