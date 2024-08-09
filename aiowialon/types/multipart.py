from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict


@dataclass(frozen=True)
class MultipartField:
    name: str
    value: Any = field(repr=False)
    content_type: Optional[str] = None
    filename: Optional[str] = None
    content_transfer_encoding: Optional[str] = None

    def dict(self) -> Dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


__all__ = ['MultipartField']
