from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import PostgresSettings

from .base import BaseComponent


class AsyncSessionMaker(async_sessionmaker[AsyncSession]):
    pass


class DatabaseComponent(BaseComponent):
    def __init__(self, settings: PostgresSettings) -> None:
        self._settings = settings
        self._engine: AsyncEngine | None = None
        self._session_maker: AsyncSessionMaker | None = None

    async def start(self) -> None:
        self._engine = create_async_engine(
            self._settings.dsn,
            echo=self._settings.echo,
            pool_size=self._settings.pool_size,
            max_overflow=self._settings.max_overflow,
        )
        self._session_maker = AsyncSessionMaker(self._engine, expire_on_commit=False)

    async def stop(self) -> None:
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None

    @property
    def session_maker(self) -> AsyncSessionMaker:
        if not self._session_maker:
            msg = "Session maker not initialized"
            raise RuntimeError(msg)
        return self._session_maker
