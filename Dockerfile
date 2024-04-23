ARG HOME=/home/app
ARG POETRY_VERSION=1.8.2
ARG PYTHON_VERSION=3.12

FROM busybox


FROM acidrain/python-poetry:$PYTHON_VERSION-slim-$POETRY_VERSION as poetry

ARG HOME
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONUNBUFFERED=true \
    PYTHONDONTWRITEBYTECODE=true
WORKDIR $HOME

COPY pyproject.toml poetry.lock $HOME/
RUN poetry install --no-cache --no-interaction --no-ansi -vvv


FROM python:$PYTHON_VERSION-slim

ARG HOME
ENV PYTHONUNBUFFERED=true \
    PYTHONDONTWRITEBYTECODE=true \
    APP_HOME=$HOME/diploma \
    PATH="$HOME/.venv/bin:$PATH"
WORKDIR $APP_HOME

RUN apt-get update && \
    apt-get install -y --no-install-recommends tini && \
    apt-get clean && rm -rf /var/cache/apt


COPY --from=poetry $HOME/.venv $HOME/.venv

ENTRYPOINT ["tini", "--"]
