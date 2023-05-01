"""Application configuration - root APIRouter.
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from app.entrypoints import actuator

root_router = APIRouter()
api_router_v1 = APIRouter(prefix="/api/v1")

# Base Routers
root_router.include_router(actuator.router)

# API Routers
