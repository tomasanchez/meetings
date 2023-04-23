"""Application configuration - root APIRouter.
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from auth.entrypoints import actuator
from auth.entrypoints.v1 import auth, users

root_router = APIRouter()
api_router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])

# Base Routers
root_router.include_router(actuator.router)

# API Routers
api_router_v1.include_router(users.router)
api_router_v1.include_router(auth.router)
