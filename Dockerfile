FROM python:3.12-alpine AS base

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk update && \
    apk add libpq

FROM base AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Install the app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM base AS runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app
EXPOSE 8000
ENTRYPOINT ["python", "-m", "app.main"]