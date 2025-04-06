from dataclasses import dataclass


@dataclass(kw_only=True)
class PaginationParams:
    limit: int = 20
    offset: int = 0
