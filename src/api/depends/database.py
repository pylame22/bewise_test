from typing import Annotated

from fastapi import Depends

from src.core.components.database import AsyncSessionMaker

from .base import AppContainerDep


async def _get_database_session_maker(
    container: AppContainerDep,
) -> AsyncSessionMaker:
    return container.database.session_maker


DatabaseSessionMakerDep = Annotated[AsyncSessionMaker, Depends(_get_database_session_maker)]
