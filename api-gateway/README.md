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

## Environment Variables

### Application

Variables prefixed with `FASTAPI_` are used to configure the application.

| Name                        | Description                                     | Default Value |
|-----------------------------|-------------------------------------------------|---------------|
| FASTAPI_DEBUG               | Debug Mode                                      | False         |
| FASTAPI_PROJECT_NAME        | Swagger Title                                   | API GATEWAY   |
| FASTAPI_PROJECT_DESCRIPTION | Swagger Description                             | ...           |
| FASTAPI_USE_LIMITER         | Toggles Rate Limiting                           | False         |
| FASTAPI_LIMITER_THRESHOLD   | Maximum requests number                         | 10            |
| FASTAPI_LIMITER_INTERVAL    | Time in which the threshold is reset in minutes | 1             |
| FASTAPI_USE_LIMITER         | Toggles Rate Limiting                           | False         |
| FASTAPI_VERSION             | Application Version                             | app.version   |
| FASTAPI_DOCS_URL            | Swagger Endpoint                                | /docs         |

### Gateway

Variables prefixed with `GATEWAY_` are used to configure the gateway.

| Name             | Description                   | Default Value |
|------------------|-------------------------------|---------------|
| GATEWAY_SERVICES | Available services to connect | _see below_*  |
| GATEWAY_TIMEOUT  | Requests time out in seconds  | 59            |

Service interface

```py
class Service:
    name: str
    base_url: str
    readiness_url: str = "/readiness"
    health_url: str = "/health"
```

Eg:

```json
 [
  {
    "name": "users",
    "base_url": "http://users:8001",
    "readiness_url": "actuator/readiness"
  },
  {
    "name": "auth",
    "base_url": "http://auth:8000"
  }
]
```

### Redis

Variables prefixed with `REDIS_` are used to configure the redis connection.

| Name           | Description                      | Default Value |
|----------------|----------------------------------|---------------|
| REDIS_HOST     | Redis Host                       | localhost     |
| REDIS_PORT     | Redis Port                       | 6379          |
| REDIS_CLUSTER  | If connection is using a cluster | False         |
| REDIS_ACTIVE   | Whether to use redis or not      | True          |
| REDIS_USERNAME | DB Username                      |               |
| REDIS_PASSWORD | DB Password                      |               |

## Production Environment

This project uses the `Docker` image `uvicorn-gunicorn-fastapi:python3.10-slim` for superior performance.

## Recommended Readings

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Cosmic Python](https://cosmicpython.com/)
- [Gunicorn + Uvicorn](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

## Design

### Rate Limiting

This API Gateway uses a `Redis` instance to store the rate limit counters.
The rate limit is set to `X` requests per `T` seconds.

#### Class Diagram

Our `FastAPI` application calls a middleware function which checks the rate limit before request is served.

It uses the `RateLimiter` to increment the counter for the request host and checks if it has exceeded the limit, if so,
it returns it interrupts the execution sending a response with a `429` status code: too many requests.

![Rate Limiting Class Diagram](../docs/assets/rate-limiter-class_diagram.svg)

The `RateLimiter` implementation uses the `Redis` instance to store the counters with the `INCR` command, which
guarantees that is run atomically. `RedisConnector` is a wrapper around the `Redis` client which provides common methods
an errors for using both a single redis connection or a cluster. `RedisClient` uses `aioredis` for as ync operations.