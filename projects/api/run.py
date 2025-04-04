from open_gallery.shared_api.types import enable_types_support

enable_types_support()

from open_gallery.api.settings import APISettings  # noqa: E402

settings = APISettings()

if __name__ == "__main__":
    if settings.web_server == "granian":
        from granian.constants import Interfaces, Loops
        from granian.server import Server

        runtime = Server(
            "open_gallery.api.core:app",
            reload=settings.app.reload,
            port=settings.server.port,
            address=settings.server.host,
            loop=Loops.uvloop,
            interface=Interfaces.ASGI,
            workers=settings.server.workers,
        )
        runtime.serve()

    if settings.web_server == "uvicorn":
        import uvicorn

        uvicorn.run(
            "open_gallery.api.core:app",
            reload=settings.app.reload,
            port=settings.server.port,
            host=settings.server.host,
        )
