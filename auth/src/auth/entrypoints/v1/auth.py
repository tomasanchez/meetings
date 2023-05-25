"""Authentication & Authorization Entry Points

"""

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from auth.app.dependencies import AuthDependency, BearerTokenAuth
from auth.domain.commands import AuthenticateUser
from auth.domain.events import TokenGenerated, UserAuthenticated
from auth.domain.schemas import ResponseModel
from auth.service_layer.errors import InvalidCredentialsError

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/token', status_code=HTTP_200_OK, tags=["Commands"])
async def log_in(command: AuthenticateUser, auth_service: AuthDependency) -> ResponseModel[TokenGenerated]:
    """
    Authenticates a user, providing an Access Token.
    """
    try:
        token = auth_service.authenticate(username=command.username, password=command.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))

    return ResponseModel(data=TokenGenerated(token=token))


@router.get('/me', status_code=HTTP_200_OK, tags=["Commands"])
async def me(
        token: BearerTokenAuth,
        auth_service: AuthDependency,
) -> ResponseModel[UserAuthenticated]:
    """
    Authorizes a token, providing the user's information.
    """
    try:
        user = auth_service.authorize(token.credentials)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))

    return ResponseModel(data=user)
