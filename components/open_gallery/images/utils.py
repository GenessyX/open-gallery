from typing import IO, Any


def get_size(io: IO[Any]) -> int:
    current_pos = io.tell()
    io.seek(0, 2)
    size = io.tell()
    io.seek(current_pos)
    return size
