FROM python:3.10.8-slim as development_build

ARG APP_DIR=/app

ARG ENV

ENV ENV=${ENV} \
    PYTHOPNUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1 \
    UVICORN_PORT=8000 \
    UVICORN_HOST="0.0.0.0"\
    FASTAPI_DEBUG=0

# Deploy application
WORKDIR $APP_DIR
COPY pyproject.toml poetry.lock README.md ${APP_DIR}/
ADD src ${APP_DIR}/src

# System dependencies
RUN pip install --disable-pip-version-check "poetry==$POETRY_VERSION"

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --only main

EXPOSE $UVICORN_PORT

CMD ["poetry", "run", "python","-m", "auth.main"]