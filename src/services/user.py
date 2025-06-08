from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from src.core.enums.user import UserStatusEnum
from src.core.models.user import UserModel
from src.core.utils import utc_now
from src.schemas.dto.user import UserCreateDTO, UserParamsDTO, UserUpdateDTO
from src.schemas.dto.user_balance_operation import UserBalanceOperationCreateDTO
from src.services.auth import AuthService
from src.services.exceptions import (
    UserBalanceNotEnoughError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
    UserNotVerifiedError,
    UserPasswordNotValidError,
)
from src.utils.uow import UnitOfWork

from .base import BaseService


class UserService(BaseService):
    def __init__(self, unit_of_work: UnitOfWork, auth_service: AuthService) -> None:
        self._unit_of_work = unit_of_work
        self._auth_service = auth_service

    async def get_current_user(self, username: str, password: str) -> UserModel:
        async with self._unit_of_work as uow:
            user = await uow.context.user_repository.get_by_username(username)
            if not user:
                raise UserNotFoundError
            if not self._auth_service.verify_password(password, hashed_password=user.hashed_password):
                raise UserPasswordNotValidError
            return user

    async def create_user(self, user_create_dto: UserCreateDTO) -> UserModel:
        hashed_password = self._auth_service.hash_password(user_create_dto.password)
        async with self._unit_of_work as uow:
            try:
                user = await uow.context.user_repository.create(user_create_dto, hashed_password=hashed_password)
            except IntegrityError as err:
                raise UsernameAlreadyExistsError from err
            await uow.commit()
            return user

    async def get_users(self, params_dto: UserParamsDTO) -> Sequence[UserModel]:
        async with self._unit_of_work as uow:
            return await uow.context.user_repository.get_all(params_dto)

    async def update_user(self, user_id: int, *, user_update_dto: UserUpdateDTO) -> UserModel:
        async with self._unit_of_work as uow:
            user = await uow.context.user_repository.update(user_id, user_update_dto=user_update_dto)
            if not user:
                raise UserNotFoundError
            await uow.commit()
            return user

    async def delete_user(self, user_id: int) -> UserModel:
        user_update_dto = UserUpdateDTO(deleted_at=utc_now())
        async with self._unit_of_work as uow:
            user = await uow.context.user_repository.update(user_id, user_update_dto=user_update_dto)
            if not user:
                raise UserNotFoundError
            await uow.commit()
            return user

    async def update_user_status(self, user_id: int, *, status: UserStatusEnum) -> UserModel | None:
        user_update_dto = UserUpdateDTO(status=status)
        async with self._unit_of_work as uow:
            user = await uow.context.user_repository.update(user_id, user_update_dto=user_update_dto)
            if not user:
                raise UserNotFoundError
            await uow.commit()
            return user

    async def update_user_balance(self, user_id: int, operator_id: int, *, balance_delta: Decimal) -> Decimal:
        async with self._unit_of_work as uow:
            user = await uow.context.user_repository.update_balance(user_id, balance_delta=balance_delta)
            if not user:
                raise UserNotFoundError
            if user.status != UserStatusEnum.VERIFIED:
                raise UserNotVerifiedError
            if user.balance < 0:
                raise UserBalanceNotEnoughError
            operation_create_dto = UserBalanceOperationCreateDTO(
                balance_before=user.balance - balance_delta,
                balance_after=user.balance,
                balance_delta=balance_delta,
            )
            await uow.context.user_balance_operation_repository.create(
                user_id,
                operator_id,
                operation_create_dto=operation_create_dto,
            )
            await uow.commit()
            return user.balance
