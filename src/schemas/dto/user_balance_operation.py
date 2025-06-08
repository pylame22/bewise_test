from decimal import Decimal

from pydantic import BaseModel


class UserBalanceOperationCreateDTO(BaseModel):
    balance_before: Decimal
    balance_after: Decimal
    balance_delta: Decimal
