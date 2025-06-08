from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends

from src.api.depends.repository import UnitOfWorkDep
from src.services.auth import AuthService
from src.services.user import UserService


def _get_auth_service() -> AuthService:
    password_hasher = PasswordHasher()
    return AuthService(password_hasher)


AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]


def _get_user_service(
    unit_of_work: UnitOfWorkDep,
    auth_service: AuthServiceDep,
) -> UserService:
    return UserService(unit_of_work, auth_service)


UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
