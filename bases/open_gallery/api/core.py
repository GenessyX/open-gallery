import logging
import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import APIRouter, FastAPI

from open_gallery.api.identity.exceptions import user_error_handler
from open_gallery.api.ioc.settings import SettingsProvider
from open_gallery.api.settings import APISettings
from open_gallery.context.core import real_ip_ctx, request_id_ctx, sequence_ctx
from open_gallery.hashing.ioc import HasherProvider
from open_gallery.identity.exceptions import UserError
from open_gallery.identity.ioc import IdentityUsecasesProvider
from open_gallery.logging.config import create_logging_config
from open_gallery.passwords.ioc import PasswordsProvider
from open_gallery.persistence.ioc import DatabaseProvider, RepositoriesProvider, UnitsOfWorkProvider
from open_gallery.persistence.tables.base import mapper_registry
from open_gallery.persistence.tables.mappers import bind_mappers
from open_gallery.shared.exceptions import DomainError
from open_gallery.shared_api.exceptions import domain_error_handler
from open_gallery.shared_api.types import enable_types_support

enable_types_support()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await app.state.dishka_container.close()


def create_app(settings: APISettings | None = None) -> FastAPI:
    if not settings:
        settings = APISettings()

    container = make_async_container(
        SettingsProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
        UnitsOfWorkProvider(),
        HasherProvider(),
        PasswordsProvider(),
        IdentityUsecasesProvider(),
        FastapiProvider(),
    )

    bind_mappers(mapper_registry)

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

    setup_dishka(container=container, app=app)

    api_v1 = APIRouter(prefix="/api/v1")

    from open_gallery.api.identity.router import identity_router

    api_v1.include_router(identity_router)

    app.include_router(api_v1)

    app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(UserError, user_error_handler)  # type: ignore[arg-type]

    logger.info("Application initialized")

    return app


app = create_app()
