"""Data types for multipart Wialon Remote API calls"""

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class MultipartField:
    """Dataclas that keeps multipart field data for remote API call"""

    name: str
    value: Any = field(repr=False)
    content_type: str | None = None
    filename: str | None = None
    content_transfer_encoding: str | None = None

    def dict(self) -> dict[str, Any]:
        """Returns a dictionary representation of the multipart field
        prepared to be added to the request data, used internally
        in 'Wialon.multipart' method
        """

        return {key: value for key, value in asdict(self).items() if value is not None}


__all__ = ("MultipartField",)
