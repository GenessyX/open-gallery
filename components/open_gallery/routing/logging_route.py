import logging
import time
import uuid
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response
from fastapi.routing import APIRoute

from open_gallery.context.core import PerformanceTiming, real_ip_ctx, request_id_ctx, sequence_ctx, timings_ctx
from open_gallery.http_utils import constants
from open_gallery.logging.enums import ContextCallType, ContextEventType
from open_gallery.routing.utils import convert_body, convert_fastapi_multi_mapping, convert_mapping, get_content_type

logger = logging.getLogger(__name__)


def timings_to_header(timings: dict[str, PerformanceTiming]) -> str:
    return ", ".join(
        [
            f"{name};{'desc=' + f'{timing.desc};' if timing.desc else ''}dur={timing.dur}"
            for name, timing in timings.items()
        ],
    )


class LoggingRoute(APIRoute):
    def _get_request_id_ctx(self, request: Request) -> str:
        request_id = request.headers.get(constants.REQUEST_ID_HEADER)

        if not request_id:
            request_id = uuid.uuid4().hex

        return request_id

    def init_context(self, request: Request) -> None:
        sequence_ctx.set(0)
        real_ip_ctx.set(request.headers.get(constants.REAL_IP_HEADER, "unknown"))
        request_id_ctx.set(self._get_request_id_ctx(request))

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            self.init_context(request)

            request_content_type = get_content_type(request.headers)
            logger.info(
                "HTTP request received at '%s' with method '%s'",
                str(request.url),
                request.method,
                extra={
                    "call_type": ContextCallType.INCOMING,
                    "event_type": ContextEventType.REQUEST,
                    "request_method": request.method,
                    "request_body": convert_body(
                        content_type=request_content_type,
                        body=await request.body(),
                    ),
                    "request_params": convert_fastapi_multi_mapping(request.query_params),
                    "request_headers": convert_mapping(dict(request.headers)),
                },
            )

            start_time = time.monotonic()
            response: Response = await original_route_handler(request)
            end_time = time.monotonic()

            request_duration = round(end_time - start_time, 5)
            request_duration_int = int(request_duration * 1000)

            timings = timings_ctx.get()
            if timings is None:
                timings = {}
            timings["app"] = PerformanceTiming(dur=request_duration_int)
            timings_ctx.set(timings)

            response.headers["x-response-time"] = f"{request_duration_int}"
            response.headers["server-timing"] = timings_to_header(timings)
            response.headers[constants.REQUEST_ID_HEADER] = request_id_ctx.get()

            response_content_type = get_content_type(response.headers)
            logger.info(
                "HTTP response sent with status code '%s' in '%.4f' seconds.",
                response.status_code,
                request_duration,
                extra={
                    "status_code": response.status_code,
                    "transfer_time": request_duration,
                    "call_type": ContextCallType.INCOMING,
                    "event_type": ContextEventType.RESPONSE,
                    "response_body": convert_body(
                        content_type=response_content_type,
                        body=bytes(response.body),
                    ),
                    "response_headers": convert_mapping(dict(response.headers)),
                },
            )
            return response

        return custom_route_handler
