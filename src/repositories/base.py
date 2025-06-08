from collections.abc import Sequence

from sqlalchemy import Executable
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.base import BaseSAModel


class BaseRepository[T: BaseSAModel]:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _execute(self, query: Executable) -> None:
        await self._session.execute(query)

    async def _fetch_all(self, query: Executable) -> Sequence[T]:
        result = await self._session.execute(query)
        return result.scalars().all()

    async def _fetch_one(self, query: Executable) -> T:
        result = await self._session.execute(query)
        return result.scalars().first()  # type: ignore [return-value]

    async def _fetch_one_or_none(self, query: Executable) -> T | None:
        result = await self._session.execute(query)
        return result.scalars().first()
