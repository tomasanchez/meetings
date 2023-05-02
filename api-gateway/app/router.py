"""Application configuration - root APIRouter.
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from app.entrypoints import actuator
from app.entrypoints.v1 import auth_service

root_router = APIRouter()
api_router_v1 = APIRouter(prefix="/api/v1")

# Base Routers
root_router.include_router(actuator.router)

# API Routers
api_router_v1.include_router(auth_service.router)
