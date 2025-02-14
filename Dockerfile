FROM python:3.13

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN --mount=type=cache,target=/root/.cache pip install poetry==2.0.0

COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0
RUN --mount=type=cache,target=/root/.cache poetry install --without dev --no-root

COPY alembic ./alembic

COPY zapchastimira ./zapchastimira

COPY alembic.ini .
