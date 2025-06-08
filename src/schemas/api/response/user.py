from decimal import Decimal

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    city: str | None
    country: str | None


class UserUpdateBalanceResponse(BaseModel):
    balance_after: Decimal = Field(max_digits=12, decimal_places=2)
