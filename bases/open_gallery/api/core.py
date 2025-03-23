from fastapi import APIRouter, FastAPI

from open_gallery.api.settings import APISettings


def create_app(settings: APISettings | None = None) -> FastAPI:
    if not settings:
        settings = APISettings()

    app = FastAPI(openapi_url=settings.server.openapi_url)

    api_v1 = APIRouter(prefix="/api/v1")

    app.include_router(api_v1)

    return app


app = create_app()
