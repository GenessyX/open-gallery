from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from open_gallery.logging.settings import LoggingSettings
from open_gallery.persistence.settings import DatabaseSettings
from open_gallery.settings.app import AppSettings
from open_gallery.settings.server import ServerSettings

APP_ROOT = Path(__file__).parent.parent

ENV_FILES = (APP_ROOT / ".env", APP_ROOT / "local.env")

WebServer = Literal["uvicorn", "granian"]


class APISettings(BaseSettings):
    web_server: WebServer = "uvicorn"
    app: AppSettings = AppSettings()
    server: ServerSettings = ServerSettings()
    database: DatabaseSettings = DatabaseSettings()
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_nested_delimiter="__",
        extra="ignore",
    )
