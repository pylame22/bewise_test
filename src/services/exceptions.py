class BaseServiceError(Exception):
    code: str


class UserNotFoundError(BaseServiceError):
    code = "user_not_found"


class UserBalanceNotEnoughError(BaseServiceError):
    code = "user_balance_not_enough"


class UserPasswordNotValidError(BaseServiceError):
    code = "user_password_not_valid"


class UserNotVerifiedError(BaseServiceError):
    code = "user_not_verified"


class UsernameAlreadyExistsError(BaseServiceError):
    code = "username_already_exists"
