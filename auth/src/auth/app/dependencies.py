"""
FastAPI dependencies are reusable components that can be used across multiple routes.
"""
from typing import Annotated

from fastapi import Depends

from auth.adapters.repository import InMemoryUserRepository, UserRepository
from auth.service_layer.password_encoder import BcryptPasswordEncoder, PasswordEncoder
from auth.service_layer.register import RegisterService

in_memory_user_repository = InMemoryUserRepository()


def get_user_repository() -> UserRepository:
    """
    Dependency that returns a UserRepository instance.
    """
    return in_memory_user_repository


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]


def get_password_encoder() -> PasswordEncoder:
    """
    Dependency that returns a PasswordEncoder instance.
    """
    return BcryptPasswordEncoder()


PasswordEncoderDependency = Annotated[PasswordEncoder, Depends(get_password_encoder)]


def get_register_service(user_repository: UserRepositoryDependency,
                         encoder: PasswordEncoderDependency) -> RegisterService:
    """
    Dependency that returns a RegisterService instance.
    """
    return RegisterService(
        user_repository=user_repository,
        password_encoder=encoder,
    )


RegisterDependency = Annotated[RegisterService, Depends(get_register_service)]
