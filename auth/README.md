# Auth Service

Auth Service is a REST API that provides authentication and authorization for the _Schedutn_ project.

## Continuous Integration

This project uses `make` as an adaptation layer.

Run `make help` to see all available commands.

## Development Environment

### Installing Poetry

This package uses poetry for dependency management.

Install poetry in the system `site_packages`. DO NOT INSTALL IT in a virtual environment itself.

To install poetry, run:

```bash
pip install poetry
```

### Building the Development Environment

1. Clone the repository

```bash
git clone "git@github.com:tomasanchez/pymeet.git"
```

2. Install the dependencies.

If you don't start in a virtual environment poetry will create one for you.

```bash
cd pymeet/pymeet-rest && poetry install
```

Note that poetry doesn't activate the virtual environment for you. You have to do it manually.
Or prefix subsequent the commands with `poetry run`.

You can view the environment that poetry uses with `poetry env info`.

To activate run:

```bash
poetry shell
```

## Running Local

1. Run:

```bash
poetry run python -m pymeet.main
```

2. Go to http://localhost:8000/docs to see the API documentation.

## Running Tests

Run:

```bash
poetry run pytest
```

To generate a coverage report add `--cov src`.

```bash
poetry run pytest --cov src
```

## Updating Dependencies

To update the dependencies run:

```bash
poetry update
```

## Recommended Readings

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Cosmic Python](https://cosmicpython.com/)