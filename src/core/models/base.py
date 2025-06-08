import datetime
from typing import Any, ClassVar

from sqlalchemy import DateTime, Numeric, SmallInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.type_api import TypeEngine

from src.core.enums.user import UserRoleEnum, UserStatusEnum
from src.core.types import Money


class BaseSAModel(DeclarativeBase):
    type_annotation_map: ClassVar[dict[type, TypeEngine[Any]]] = {
        datetime.datetime: DateTime(timezone=True),
        Money: Numeric(12, 2),
        UserRoleEnum: SmallInteger(),
        UserStatusEnum: SmallInteger(),
    }
