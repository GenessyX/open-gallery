from fastapi import APIRouter

from open_gallery.routing.logging_route import LoggingRoute

identity_router = APIRouter(prefix="/identity", route_class=LoggingRoute)


@identity_router.get("")
async def test() -> str:
    return "hello world"
