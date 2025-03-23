import logging

from open_gallery.context import request_id_ctx, sequence_ctx


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


class SequenceFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        sequence = sequence_ctx.get()
        record.sequence = sequence
        sequence_ctx.set(sequence + 1)
        return True
