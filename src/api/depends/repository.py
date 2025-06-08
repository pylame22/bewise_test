from typing import Annotated

from fastapi import Depends

from src.utils.uow import UnitOfWork

from .database import DatabaseSessionMakerDep


def _get_unit_of_work(session_maker: DatabaseSessionMakerDep) -> UnitOfWork:
    return UnitOfWork(session_maker)


UnitOfWorkDep = Annotated[UnitOfWork, Depends(_get_unit_of_work)]
