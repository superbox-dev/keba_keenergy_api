"""KEBA KeEnergy API error classes."""


class APIError(Exception):
    """API error."""


class InvalidJsonError(APIError):
    """Invalid JSON data error."""


class AuthenticationError(APIError):
    """Invalid credentials error."""
