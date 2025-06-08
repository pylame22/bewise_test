from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.routers.user import router as user_router
from src.core.app_container import AppContainer
from src.core.components.database import DatabaseComponent
from src.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    database = DatabaseComponent(settings.postgres)
    await database.start()

    app.state.container = AppContainer(
        settings=settings,
        database=database,
    )

    yield None

    await database.stop()


def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    app.include_router(user_router)
    return app
