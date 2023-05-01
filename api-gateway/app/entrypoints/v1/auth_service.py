"""
Entry points for the Auth service.
"""
from typing import Annotated

from fastapi import APIRouter, Path, Query
from starlette.status import HTTP_200_OK

from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.events.auth_service import UserRegistered
from app.domain.schemas import ResponseModel, ResponseModels
from app.service_layer.gateway import api_v1_url, get_service, get_users, verify_ok

router = APIRouter(prefix="/auth-service", tags=["Auth"])

UsersQuery = Annotated[
    str | None, Query(description="A list of comma-separated usernames.", example="johndoe, other", alias="users")]


@router.get("/users",
            status_code=HTTP_200_OK,
            summary="Find all users",
            tags=["Queries"]
            )
async def query_users(
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
        user_names: UsersQuery = None, ) -> ResponseModels[UserRegistered]:
    """
    Retrieves users from the Database.
    """

    service = await get_service(service_name="auth", services=services)

    response, code = await get_users(users=user_names, service=service, client=client)

    verify_ok(response=response, status_code=code)

    return ResponseModels[UserRegistered](**response)


@router.get("/users/{username}",
            status_code=HTTP_200_OK,
            summary="Find user by username",
            tags=["Queries"]
            )
async def query_user_by_username(
        username: Annotated[str, Path(description="The user's username.", example="johndoe")],
        services: ServiceProvider,
        client: AsyncHttpClientDependency, ) -> ResponseModel[UserRegistered]:
    """
    Retrieves a specific user from the Database.
    """

    service = await get_service(service_name="auth", services=services)

    response, code = await gateway(service_url=service.base_url, path=f"{api_v1_url}/users/{username}",
                                   client=client, method="GET")

    verify_ok(response=response, status_code=code)

    return ResponseModel[UserRegistered](**response)
