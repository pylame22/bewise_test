import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

_CONFIG_FILE = "config.yml"
_BASE_DIR = Path(__file__).parent.parent.parent


class PostgresSettings(BaseModel):
    user: str
    password: str
    db: str
    host: str
    port: int
    echo: bool
    pool_size: int
    max_overflow: int

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class AppSettings(BaseModel):
    base_dir: Path
    postgres: PostgresSettings


def get_settings() -> AppSettings:
    load_dotenv()
    with Path(f"{_BASE_DIR}/{_CONFIG_FILE}").open() as file:
        data = file.read()
    for match in re.finditer(r"\${(?P<env_value>.*)}", data):
        env_name = match.group("env_value")
        env_value = os.environ[env_name]
        data = data.replace(match.group(), env_value)
    settings_data = yaml.safe_load(data)
    return AppSettings(base_dir=_BASE_DIR, **settings_data)
