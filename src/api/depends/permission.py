from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.api.depends.service import UserServiceDep
from src.core.enums.user import UserRoleEnum
from src.core.models.user import UserModel
from src.services.exceptions import UserNotFoundError, UserPasswordNotValidError

security = HTTPBasic()


async def _get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    user_service: UserServiceDep,
) -> UserModel:
    try:
        user = await user_service.get_current_user(credentials.username, credentials.password)
    except (UserNotFoundError, UserPasswordNotValidError) as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err.code) from err
    return user


CurrentUserDep = Annotated[UserModel, Depends(_get_current_user)]


def _check_staff(current_user: CurrentUserDep) -> None:
    if current_user.role != UserRoleEnum.STAFF:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


CheckStaffDep = Annotated[None, Depends(_check_staff)]


def _check_staff_or_owner(user_id: int, current_user: CurrentUserDep) -> None:
    if current_user.role != UserRoleEnum.STAFF and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


CheckStaffOrOwnerDep = Annotated[None, Depends(_check_staff_or_owner)]
