from contextvars import ContextVar
from typing import NamedTuple
from uuid import UUID

request_id_ctx = ContextVar[str]("request_id_ctx", default=UUID(int=0).hex)
sequence_ctx = ContextVar[int]("sequence_ctx", default=0)
real_ip_ctx = ContextVar[str]("real_ip_ctx", default="unknown")


class PerformanceTiming(NamedTuple):
    dur: int  # Duration in MS
    desc: str | None = None


timings_ctx = ContextVar[dict[str, PerformanceTiming] | None]("timings_ctx", default=None)
