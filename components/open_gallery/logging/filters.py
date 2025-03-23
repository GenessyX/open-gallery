import logging
from contextvars import ContextVar


class RequestIdFilter(logging.Filter):
    def __init__(self, name: str = "", *, request_id_ctx: ContextVar[str]) -> None:
        super().__init__(name)
        self.request_id_ctx = request_id_ctx

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id_ctx.get()
        return True


class SequenceFilter(logging.Filter):
    def __init__(self, name: str = "", *, sequence_ctx: ContextVar[int]) -> None:
        super().__init__(name)
        self.sequence_ctx = sequence_ctx

    def filter(self, record: logging.LogRecord) -> bool:
        sequence = self.sequence_ctx.get()
        record.sequence = sequence
        self.sequence_ctx.set(sequence + 1)
        return True
