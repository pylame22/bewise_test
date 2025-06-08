from argon2 import PasswordHasher, exceptions

from src.services.base import BaseService


class AuthService(BaseService):
    def __init__(self, password_hasher: PasswordHasher) -> None:
        self._password_hasher = password_hasher

    def hash_password(self, password: str) -> str:
        return self._password_hasher.hash(password)

    def verify_password(self, password: str, *, hashed_password: str) -> bool:
        try:
            self._password_hasher.verify(hashed_password, password)
        except exceptions.VerifyMismatchError:
            return False
        return True
