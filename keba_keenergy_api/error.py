"""KEBA KeEnergy API error classes."""


class APIError(Exception):
    """API error."""

    def __init__(
        self,
        message: str = "",
        /,
        *,
        status: int | None = None,
    ) -> None:
        self.message: str = message
        self.status: int | None = status

    def __str__(self) -> str:
        return f"{self.status} {self.message}" if self.status else self.message


class InvalidJsonError(APIError):
    """Invalid JSON data error."""


class AuthenticationError(APIError):
    """Invalid credentials error."""
