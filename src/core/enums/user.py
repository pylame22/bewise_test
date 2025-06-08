from enum import IntEnum


class UserRoleEnum(IntEnum):
    STAFF = 1
    CLIENT = 2


class UserStatusEnum(IntEnum):
    UNVERIFIED = 1
    VERIFIED = 2
    # banned, deleted, etc...
