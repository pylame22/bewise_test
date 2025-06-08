from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums.user import UserRoleEnum, UserStatusEnum
from src.core.types import Money

from .base import BaseSAModel


class UserModel(BaseSAModel):
    __tablename__ = "users"

    __table_args__ = (
        sa.Index("idx_users_username", "username", unique=True),
        sa.Index("idx_users_status", "status", postgresql_using="hash"),  # if we have highly selective values
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    city: Mapped[str | None]
    country: Mapped[str | None]
    balance: Mapped[Money] = mapped_column(server_default="0")

    role: Mapped[UserRoleEnum]
    status: Mapped[UserStatusEnum]
    hashed_password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    updated_at: Mapped[datetime | None]
    deleted_at: Mapped[datetime | None]
