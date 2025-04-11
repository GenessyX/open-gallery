from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from open_gallery.logging.settings import LoggingSettings
from open_gallery.persistence.settings import DatabaseSettings
from open_gallery.settings.app import AppSettings


@dataclass(kw_only=True)
class LoggingContextVars:
    sequence: ContextVar[int]
    real_ip: ContextVar[str]
    request_id: ContextVar[str]


def create_logging_config(
    settings: LoggingSettings,
    app_settings: AppSettings,
    database_settings: DatabaseSettings,
    context_vars: LoggingContextVars,
) -> dict[str, Any]:
    loggers = {
        "__main__": {
            "handlers": ["stdout"],
            "level": settings.handlers_level,
            "propagate": False,
        },
        "open_gallery": {
            "handlers": ["stdout"],
            "level": settings.handlers_level,
            "propagate": False,
        },
    }

    if database_settings.echo:
        loggers["sqlalchemy.engine"] = {
            "handlers": ["stdout"],
            "level": settings.handlers_level,
            "propagate": False,
        }
    if database_settings.echo_pool:
        loggers["sqlalchemy.pool"] = {
            "handlers": ["stdout"],
            "level": settings.handlers_level,
            "propagate": False,
        }
    if database_settings.echo_orm:
        loggers["sqlalchemy.orm"] = {
            "handlers": ["stdout"],
            "level": settings.handlers_level,
            "propagate": False,
        }
    if database_settings.echo_dialects:
        loggers["sqlalchemy.dialects"] = {
            "handlers": ["stdout"],
            "level": settings.handlers_level,
            "propagate": False,
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {
                "()": "open_gallery.logging.filters.RequestIdFilter",
                "request_id_ctx": context_vars.request_id,
            },
            "sequence": {
                "()": "open_gallery.logging.filters.SequenceFilter",
                "sequence_ctx": context_vars.sequence,
            },
        },
        "formatters": {
            "plain": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": (
                    "[%(asctime)s.%(msecs)03d] %(levelname)s [%(request_id)s %(sequence)s] %(name)s | %(message)s"
                ),
            },
            "json": {
                "()": "open_gallery.logging.formatter.CustomJsonFormatter",
                "format": "%(message)s %(process)s %(module)s %(funcName)s %(levelname)s %(name)s %(request_id)s",
                "timestamp": True,
                "stage": app_settings.stage.value,
                "app_name": app_settings.name,
                "json_ensure_ascii": False,
                "real_ip_ctx": context_vars.real_ip,
            },
        },
        "handlers": {
            "stdout": {
                "level": settings.handlers_level,
                "class": "logging.StreamHandler",
                "formatter": settings.formatter.value,
                "filters": ["request_id", "sequence"],
            },
        },
        "loggers": loggers,
        "root": {
            "handlers": ["stdout"],
            "propagate": False,
            "level": settings.root_level,
        },
    }
