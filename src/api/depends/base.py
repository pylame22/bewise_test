from typing import Annotated

from fastapi import Depends, Request

from src.core.app_container import AppContainer
from src.core.settings import AppSettings


def _get_app_container(request: Request) -> AppContainer:
    return request.app.state.container  # type: ignore[no-any-return]


AppContainerDep = Annotated[AppContainer, Depends(_get_app_container)]


def _get_settings(container: AppContainerDep) -> AppSettings:
    return container.settings


SettingsDep = Annotated[AppSettings, Depends(_get_settings)]
