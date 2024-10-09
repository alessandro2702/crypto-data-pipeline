FROM python:3.11

RUN pip install poetry

COPY . /crypto_ingestion

WORKDIR /crypto_ingestion/crypto_pipeline/src

RUN poetry install

CMD poetry run python landing_crypto_trending.py && poetry run python raw_crypto_trending.py