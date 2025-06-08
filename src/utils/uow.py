from dataclasses import dataclass
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.components.database import AsyncSessionMaker
from src.repositories.user import UserRepository
from src.repositories.user_balance_operation import UserBalanceOperationRepository


@dataclass
class _UnitOfWorkContext:
    session: AsyncSession
    user_repository: UserRepository
    user_balance_operation_repository: UserBalanceOperationRepository


class UnitOfWork:
    def __init__(self, session_maker: AsyncSessionMaker) -> None:
        self._session_maker = session_maker
        self._context: _UnitOfWorkContext | None = None

    @property
    def context(self) -> _UnitOfWorkContext:
        if not self._context:
            msg = "Context not initialized"
            raise RuntimeError(msg)
        return self._context

    async def __aenter__(self) -> Self:
        session = self._session_maker()
        self._context = _UnitOfWorkContext(
            session=session,
            user_repository=UserRepository(session),
            user_balance_operation_repository=UserBalanceOperationRepository(session),
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.context.session.close()

    async def commit(self) -> None:
        await self.context.session.commit()

    async def rollback(self) -> None:
        await self.context.session.rollback()
