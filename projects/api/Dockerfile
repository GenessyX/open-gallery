FROM python:3.12.6-slim AS python-base

ARG wheel=api-0.1.0-py3-none-any.whl
ARG deps=pyproject.toml

WORKDIR /app

COPY ./dist/$wheel /app/$wheel
COPY ./$deps /app/$deps
COPY ./uv.lock /app/uv.lock
COPY --link --from=ghcr.io/astral-sh/uv:0.4 /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/usr/local

RUN uv sync --locked
RUN uv pip install --system --no-cache-dir /app/$wheel

COPY ./run.py /app/run.py
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

CMD ["python", "run.py"]
