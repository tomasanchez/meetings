"""
Main module of the FastAPI application.
"""

from app.asgi import get_application

app = get_application()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
