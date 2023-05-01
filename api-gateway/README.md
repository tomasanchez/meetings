# API Gateway

This is an API Gateway which serves as a central hub for all services.

## Continuous Integration

This project uses `GitHub Actions`.

## Development Environment

This package uses pipenv for dependency management. And Requires Python 3.10

### Building the Development Environment

1. Clone the repository

```bash
git clone "git@github.com:tomasanchez/grupo-3-tacs.git"
```

2. Create the virtual environment.

```bash
cd grupo-3-tacs/api-gateway && python -m venv venv
```

3. Install the dependencies.

```bash
cd grupo-3-tacs/api-gateway && pip install -r requirements-dev.txt
```

3. Activate the virtual environment.

Use the activation script for your shell.

```bash
venv/bin/activate
```

Note: this may vary depending on your OS and shell.

## Running Local

1. Run:

```bash
uvicorn app.main:app --reload
```

2. Go to http://127.0.0.0:8000/docs to see the API documentation.

## Running Tests

Run:

```bash
pytest
```

## Production Environment

This project uses the `Docker` image `uvicorn-gunicorn-fastapi:python3.10-slim` for superior performance.

## Recommended Readings

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Cosmic Python](https://cosmicpython.com/)
- [Gunicorn + Uvicorn](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)