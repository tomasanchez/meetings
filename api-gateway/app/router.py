"""Application configuration - root APIRouter.
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

root_router = APIRouter()
api_router_v1 = APIRouter(prefix="/api/v1")

# Base Routers

# API Routers
