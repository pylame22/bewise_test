from fastapi import APIRouter, status

from src.api.converters.user import user_create_convert, user_filter_params_convert, user_update_convert
from src.api.depends.params import UserParamsDep
from src.api.depends.permission import CheckStaffDep, CheckStaffOrOwnerDep
from src.api.depends.service import UserServiceDep
from src.api.exceptions import BadRequestError, NotFoundError
from src.schemas.api.request.user import (
    UserCreateRequest,
    UserUpdateBalanceRequest,
    UserUpdateRequest,
    UserUpdateStatusRequest,
)
from src.schemas.api.response.user import UserResponse, UserUpdateBalanceResponse
from src.services.exceptions import (
    UserBalanceNotEnoughError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
    UserNotVerifiedError,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreateRequest, service: UserServiceDep) -> UserResponse:
    user_create_dto = user_create_convert(user_create)
    try:
        user = await service.create_user(user_create_dto)
    except UsernameAlreadyExistsError as err:
        raise BadRequestError(err.code) from err
    return UserResponse.model_validate(user, from_attributes=True)


@router.get("")
async def get_users(filter_params: UserParamsDep, service: UserServiceDep, _: CheckStaffDep) -> list[UserResponse]:
    params_dto = user_filter_params_convert(filter_params)
    users = await service.get_users(params_dto)
    return [UserResponse.model_validate(user, from_attributes=True) for user in users]  # TODO: use pagination response


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdateRequest,
    service: UserServiceDep,
    _: CheckStaffOrOwnerDep,
) -> UserResponse:
    user_update_dto = user_update_convert(user_update)
    try:
        user = await service.update_user(user_id, user_update_dto=user_update_dto)
    except UserNotFoundError as err:
        raise NotFoundError(err.code) from err
    return UserResponse.model_validate(user, from_attributes=True)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDep, _: CheckStaffDep) -> None:
    try:
        await service.delete_user(user_id)
    except UserNotFoundError as err:
        raise NotFoundError(err.code) from err


@router.post("/{user_id}/update_status", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_status(
    user_id: int,
    user_status: UserUpdateStatusRequest,
    service: UserServiceDep,
    _: CheckStaffDep,
) -> None:
    try:
        await service.update_user_status(user_id, status=user_status.status)
    except UserNotFoundError as err:
        raise NotFoundError(err.code) from err


@router.post("/{user_id}/change_balance")
async def update_user_balance(
    user_id: int,
    user_balance: UserUpdateBalanceRequest,
    service: UserServiceDep,
    _: CheckStaffDep,
) -> UserUpdateBalanceResponse:
    try:
        balance_after = await service.update_user_balance(user_id, user_id, balance_delta=user_balance.balance_delta)
    except UserNotFoundError as err:
        raise NotFoundError(err.code) from err
    except (UserNotVerifiedError, UserBalanceNotEnoughError) as err:
        raise BadRequestError(err.code) from err
    return UserUpdateBalanceResponse(balance_after=balance_after)
