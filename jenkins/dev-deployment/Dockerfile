FROM python:3.9 AS requirements

RUN apt-get update -y

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /root/.local/share/poetry export -f requirements.txt --with dev --output requirements.txt

# --------

FROM python:3.9

WORKDIR /

RUN apt-get update -y

RUN pip install wheel
RUN pip install bandit black flake8 isort mypy

COPY --from=requirements /requirements/requirements.txt requirements.txt

RUN PIP INSTALL -r reqirements.txt


