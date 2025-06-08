from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.core.enums.user import UserStatusEnum


class UserCreateDTO(BaseModel):
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    country: str | None = None


class UserUpdateDTO(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    country: str | None = None
    status: UserStatusEnum | None = None
    balance_delta: Decimal | None = None
    deleted_at: datetime | None = None


class UserParamsDTO(BaseModel):
    username: str | None = None
    status: UserStatusEnum | None = None
