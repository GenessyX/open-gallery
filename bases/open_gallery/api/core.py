import logging
import logging.config

from fastapi import APIRouter, FastAPI

from open_gallery.api.settings import APISettings
from open_gallery.context.core import real_ip_ctx, request_id_ctx, sequence_ctx
from open_gallery.logging.config import create_logging_config
from open_gallery.shared_api.types import enable_types_support

enable_types_support()

logger = logging.getLogger(__name__)


def create_app(settings: APISettings | None = None) -> FastAPI:
    if not settings:
        settings = APISettings()

    logging.config.dictConfig(
        create_logging_config(
            settings.logging,
            settings.app,
            sequence_ctx,
            real_ip_ctx,
            request_id_ctx,
        ),
    )

    app = FastAPI(openapi_url=settings.server.openapi_url)

    api_v1 = APIRouter(prefix="/api/v1")

    from open_gallery.api.identity.router import identity_router

    api_v1.include_router(identity_router)

    app.include_router(api_v1)

    logger.info("Application initialized")

    return app


app = create_app()
