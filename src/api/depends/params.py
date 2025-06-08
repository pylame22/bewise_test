from typing import Annotated

from fastapi import Query

from src.schemas.api.request.user import UserParams

UserParamsDep = Annotated[UserParams, Query()]
