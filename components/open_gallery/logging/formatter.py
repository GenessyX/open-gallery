import logging
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

from pythonjsonlogger import jsonlogger

if TYPE_CHECKING:
    from open_gallery.logging.enums import ContextCallType, ContextEventType


class CustomJsonFormatter(jsonlogger.JsonFormatter):  # type: ignore[name-defined,misc]
    def __init__(  # type: ignore[no-untyped-def]
        self,
        *args,  # noqa: ANN002
        app_name: str,
        stage: str,
        sequence_ctx: ContextVar[int],
        real_ip_ctx: ContextVar[str],
        **kwargs,  # noqa: ANN003
    ) -> None:
        super().__init__(*args, **kwargs)
        self.stage = stage
        self.app_name = app_name
        self.sequence_ctx = sequence_ctx
        self.real_ip_ctx = real_ip_ctx

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["channel"] = f"[open_gallery.{self.app_name}]"

        initiator = f"{log_record.pop('module')}.{log_record.pop('funcName')}"
        log_record["initiator"] = initiator

        sequence = self.sequence_ctx.get()
        log_record["sequence_number"] = sequence
        self.sequence_ctx.set(sequence + 1)

        log_record["real_ip"] = self.real_ip_ctx.get()

        call_type: "ContextCallType | None" = log_record.get("call_type")
        if call_type:
            log_record["call_type"] = call_type.value
        event_type: "ContextEventType | None" = log_record.get("event_type")
        if event_type:
            log_record["event_type"] = event_type.value
