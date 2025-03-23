import logging
import logging.config

from fastapi import APIRouter, FastAPI

from open_gallery.api.identity.router import identity_router
from open_gallery.api.settings import APISettings
from open_gallery.logging.config import create_logging_config

logger = logging.getLogger(__name__)


def create_app(settings: APISettings | None = None) -> FastAPI:
    if not settings:
        settings = APISettings()

    logging.config.dictConfig(create_logging_config(settings.logging, settings.app))

    app = FastAPI(openapi_url=settings.server.openapi_url)

    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(identity_router)

    app.include_router(api_v1)

    logger.info("Application initialized")

    return app


app = create_app()
