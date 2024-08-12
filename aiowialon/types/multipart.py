"""Data types for multipart Wialon Remote API calls"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict


@dataclass(frozen=True)
class MultipartField:
    """Dataclas that keeps multipart field data for remote API call"""

    name: str
    value: Any = field(repr=False)
    content_type: Optional[str] = None
    filename: Optional[str] = None
    content_transfer_encoding: Optional[str] = None

    def dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the multipart field
        prepared to be added to the request data, used internally
        in 'Wialon.multipart' method
        """

        return {key: value for key, value in asdict(self).items() if value is not None}


__all__ = ['MultipartField']
