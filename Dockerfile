FROM python:3.10 AS requirements

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ~/.local/bin/poetry export -f requirements.txt --output requirements.txt

# ---

FROM python:3.10

WORKDIR /app

COPY --from=requirements /app/requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install gunicorn

COPY fcg ./fcg
COPY static static
COPY templates templates

USER www-data

CMD uvicorn fcg.main:app --port 6789 --host 0.0.0.0
