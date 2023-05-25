"""
FastAPI dependencies are reusable components that can be used across multiple routes.
"""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.database import Database

from auth.adapters.db import ClientFactory
from auth.adapters.repositories.pymongo_repository import PymongoUserRepository
from auth.adapters.repository import UserRepository
from auth.app.settings.mongo_db_settings import MongoDbSettings
from auth.service_layer.auth import AuthService
from auth.service_layer.jwt import JwtService
from auth.service_layer.password_encoder import BcryptPasswordEncoder, PasswordEncoder
from auth.service_layer.register import RegisterService

mongo_settings = MongoDbSettings()
user_repository: UserRepository | None = None
password_encoder: PasswordEncoder | None = None
bearer_auth = HTTPBearer(scheme_name='JSON Web Token', description='Bearer JWT')

BearerTokenAuth = Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth)]


def get_client_factory() -> ClientFactory:
    """
    Dependency that returns a ClientFactory instance.
    """
    return ClientFactory(mongo_settings.CLIENT)


ClientFactoryDependency = Annotated[ClientFactory, Depends(get_client_factory)]


def get_database(client: ClientFactoryDependency) -> Database:
    """
    Dependency that returns a database.
    """
    return client().get_database(mongo_settings.DATABASE)


DatabaseDependency = Annotated[Database, Depends(get_database)]


def get_user_repository(db: DatabaseDependency) -> UserRepository:
    """
    Dependency that returns a UserRepository instance.
    """
    global user_repository

    if user_repository is None:
        user_repository = PymongoUserRepository(database=db)

    return user_repository


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]


def get_password_encoder() -> PasswordEncoder:
    """
    Dependency that returns a PasswordEncoder instance.
    """
    global password_encoder

    if password_encoder is None:
        password_encoder = BcryptPasswordEncoder()

    return password_encoder


PasswordEncoderDependency = Annotated[PasswordEncoder, Depends(get_password_encoder)]


def get_register_service(user_repo: UserRepositoryDependency,
                         encoder: PasswordEncoderDependency) -> RegisterService:
    """
    Dependency that returns a RegisterService instance.
    """
    return RegisterService(
        user_repository=user_repo,
        password_encoder=encoder,
    )


RegisterDependency = Annotated[RegisterService, Depends(get_register_service)]


def get_jwt_service() -> JwtService:
    """
    Dependency that returns a JwtService instance.
    """
    return JwtService()


JwtServiceDependency = Annotated[JwtService, Depends(get_jwt_service)]


def get_auth_service(user_repo: UserRepositoryDependency,
                     jwt_service: JwtServiceDependency,
                     encoder: PasswordEncoderDependency) -> AuthService:
    """
    Dependency that returns a RegisterService instance.
    """
    return AuthService(
        user_repository=user_repo,
        encoder=encoder,
        jwt_service=jwt_service,
    )


AuthDependency = Annotated[AuthService, Depends(get_auth_service)]
