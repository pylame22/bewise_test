from src.schemas.api.request.user import UserCreateRequest, UserParams, UserUpdateRequest
from src.schemas.dto.user import UserCreateDTO, UserParamsDTO, UserUpdateDTO


def user_create_convert(request: UserCreateRequest) -> UserCreateDTO:
    return UserCreateDTO(**request.model_dump())


def user_update_convert(request: UserUpdateRequest) -> UserUpdateDTO:
    return UserUpdateDTO(**request.model_dump(exclude_unset=True))


def user_filter_params_convert(request: UserParams) -> UserParamsDTO:
    return UserParamsDTO(**request.model_dump())
