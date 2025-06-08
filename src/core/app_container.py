from dataclasses import dataclass

from src.core.settings import AppSettings

from .components.database import DatabaseComponent


@dataclass
class AppContainer:
    settings: AppSettings
    database: DatabaseComponent
