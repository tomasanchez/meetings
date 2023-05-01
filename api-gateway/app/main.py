"""
Main module of the FastAPI application.
"""

from app.asgi import get_application

app = get_application()
