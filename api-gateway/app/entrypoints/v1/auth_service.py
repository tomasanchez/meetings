"""
Entry points for the Auth service.
"""
from typing import Annotated

from fastapi import APIRouter, Path, Query, Request, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.commands.auth_service import AuthenticateUser, RegisterUser
from app.domain.events.auth_service import TokenGenerated, UserRegistered
from app.domain.schemas import ResponseModel, ResponseModels
from app.service_layer.gateway import api_v1_url, get_service, get_users, verify_status

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

    verify_status(response=response, status_code=code)

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

    response, code = await gateway(service_url=service.base_url, path=f"{api_v1_url}/users/{username}/",
                                   client=client, method="GET")

    verify_status(response=response, status_code=code)

    return ResponseModel[UserRegistered](**response)


@router.post(
    "/users",
    status_code=HTTP_201_CREATED,
    summary="Command to register a new user",
    tags=["Commands"]
)
async def register(command: RegisterUser,
                   services: ServiceProvider,
                   client: AsyncHttpClientDependency,
                   request: Request,
                   response: Response):
    """
    Register a new user.
    """

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="auth", services=services)).base_url,
        path=f"{api_v1_url}/users/",
        client=client,
        method="POST",
        request_body=command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_201_CREATED])

    response_body = ResponseModel[UserRegistered](**service_response)

    response.headers["Location"] = f"{request.base_url}api/v1/users/{response_body.data.id}"
    return response_body


@router.post("/auth/token",
             status_code=HTTP_200_OK,
             summary="Command to authenticate a user",
             tags=["Commands"],
             )
async def authenticate(command: AuthenticateUser,
                       services: ServiceProvider,
                       client: AsyncHttpClientDependency) -> ResponseModel[TokenGenerated]:
    """
    Attempts to log in.
    """

    auth_response, status_code = await gateway(
        service_url=(await get_service(service_name="auth", services=services)).base_url,
        path=f"{api_v1_url}/auth/token",
        client=client,
        method="POST",
        request_body=command.json()
    )

    verify_status(response=auth_response, status_code=status_code)

    return ResponseModel[TokenGenerated](**auth_response)
