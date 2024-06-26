FROM ghcr.io/withlogicco/poetry:1.8.2-python-3.12

WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock README.md ./
RUN poetry check && poetry lock --check
RUN poetry install

COPY ./ ./
