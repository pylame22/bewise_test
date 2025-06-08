from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from src.core.enums.user import UserStatusEnum


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    country: str | None = None


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    country: str | None = None


class UserUpdateStatusRequest(BaseModel):
    status: UserStatusEnum


class UserUpdateBalanceRequest(BaseModel):
    balance_delta: Decimal = Field(max_digits=12, decimal_places=2)


class UserParams(BaseModel):
    username: str | None = None
    status: UserStatusEnum | None = None
