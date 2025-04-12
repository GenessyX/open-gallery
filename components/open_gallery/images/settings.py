from dataclasses import dataclass
from pathlib import Path


@dataclass(kw_only=True)
class ImagesSettings:
    base_path: Path = Path("uploads")
    max_size: int = 10 * 1024 * 1024
