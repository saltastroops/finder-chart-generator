FROM python:3.9 AS requirements

RUN apt-get update -y

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/bin python3 -

RUN pip install wheel
RUN pip install bandit black flake8 isort mypy
