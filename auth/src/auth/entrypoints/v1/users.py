"""
Users entrypoint
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from auth.app.dependencies import RegisterDependency, UserRepositoryDependency
from auth.domain.commands import RegisterUser
from auth.domain.events import UserRegistered
from auth.domain.mappers import user_model_to_user_registered
from auth.domain.schemas import ResponseModel, ResponseModels
from auth.service_layer.errors import IllegalUserError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=HTTP_200_OK, tags=["Queries"])
async def query_all(user_repository: UserRepositoryDependency) -> ResponseModels[UserRegistered]:
    """
    Retrieves a collection of users from the database.
    """
    users = [user_model_to_user_registered(user) for user in user_repository.find_all()] or list()

    return ResponseModels(data=users)


@router.get("/{username}", status_code=HTTP_200_OK, tags=["Queries"])
async def query_by_username(username: Annotated[str, Path(description="The user's username.", example="johndoe")],
                            user_repository: UserRepositoryDependency, ) -> ResponseModel[UserRegistered]:
    """
    Retrieves a user from the database by its id.
    """
    user = user_repository.find_by_username(username)

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found.")

    return ResponseModel(data=user_model_to_user_registered(user))


@router.post("/", status_code=HTTP_201_CREATED, tags=["Commands"])
async def register_user(command: RegisterUser,
                        register: RegisterDependency,
                        request: Request,
                        response: Response) -> ResponseModel[UserRegistered]:
    """
    Allows to register a new user in the system.
    """
    try:
        user = register.register(username=command.username, email=command.email, password=command.password)
    except IllegalUserError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))

    response.headers["Location"] = f"{request.base_url}users/{user.username}"
    return ResponseModel(data=user_model_to_user_registered(user))
