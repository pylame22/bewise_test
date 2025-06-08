from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.types import Money

from .base import BaseSAModel


class UserBalanceOperationModel(BaseSAModel):
    __tablename__ = "user_balance_operations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    operator_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    balance_delta: Mapped[Money]
    balance_before: Mapped[Money]
    balance_after: Mapped[Money]

    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
