from typing import Any

from open_gallery.logging.settings import LoggingSettings
from open_gallery.settings.app import AppSettings


def create_logging_config(settings: LoggingSettings, app_settings: AppSettings) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {"()": "open_gallery.logging.filters.RequestIdFilter"},
            "sequence": {"()": "open_gallery.logging.filters.SequenceFilter"},
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
        "loggers": {
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
        },
        "root": {
            "handlers": ["stdout"],
            "propagate": False,
            "level": settings.root_level,
        },
    }
