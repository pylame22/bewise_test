from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import insert, select, update

from src.core.enums.user import UserRoleEnum, UserStatusEnum
from src.core.models import UserModel
from src.schemas.dto.user import UserCreateDTO, UserParamsDTO, UserUpdateDTO

from .base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    _model_class = UserModel

    async def get_by_username(self, username: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.username == username, UserModel.deleted_at.is_(None))
        return await self._fetch_one_or_none(query)

    async def create(self, user_create_dto: UserCreateDTO, *, hashed_password: str) -> UserModel:
        query = (
            insert(UserModel)
            .values(
                role=UserRoleEnum.CLIENT,
                status=UserStatusEnum.UNVERIFIED,
                username=user_create_dto.username,
                email=user_create_dto.email,
                first_name=user_create_dto.first_name,
                last_name=user_create_dto.last_name,
                city=user_create_dto.city,
                country=user_create_dto.country,
                hashed_password=hashed_password,
            )
            .returning(UserModel)
        )
        return await self._fetch_one(query)

    async def get_all(self, params_dto: UserParamsDTO) -> Sequence[UserModel]:
        query = select(UserModel).where(UserModel.deleted_at.is_(None)).order_by(UserModel.id)
        if params_dto.username:
            query = query.where(UserModel.username == params_dto.username)
        if params_dto.status:
            query = query.where(UserModel.status == params_dto.status)
        return await self._fetch_all(query)

    async def update(self, user_id: int, *, user_update_dto: UserUpdateDTO) -> UserModel | None:
        update_data = user_update_dto.model_dump(exclude_unset=True)
        query = (
            update(UserModel)
            .where(
                UserModel.id == user_id,
                UserModel.deleted_at.is_(None),
            )
            .values(**update_data)
            .returning(UserModel)
        )
        return await self._fetch_one_or_none(query)

    async def update_balance(self, user_id: int, *, balance_delta: Decimal) -> UserModel | None:
        query = (
            update(UserModel)
            .where(
                UserModel.id == user_id,
                UserModel.deleted_at.is_(None),
            )
            .values(balance=UserModel.balance + balance_delta)
            .returning(UserModel)
        )
        return await self._fetch_one_or_none(query)
