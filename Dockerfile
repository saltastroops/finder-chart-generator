FROM python:3.11 AS requirements

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

RUN uv export --format requirements.txt --no-hashes > requirements.txt

# ---

FROM python:3.11

WORKDIR /app

COPY --from=requirements /app/requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install gunicorn

COPY fcg ./fcg
COPY static static
COPY templates templates

# Allow Matplotlib and AstroPy to store files
RUN mkdir -p /var/www
RUN chown -R www-data:www-data /var/www

USER www-data

CMD uvicorn fcg.main:app --port 8000 --host 0.0.0.0
