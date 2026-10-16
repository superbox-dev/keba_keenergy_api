# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""KEBA KeEnergy API error classes."""

from http import HTTPStatus


class APIError(Exception):
    """Base error of the KEBA KeEnergy API, e.g. for HTTP and connection errors."""

    def __init__(
        self,
        message: str = "",
        /,
        *,
        status: HTTPStatus | None = None,
    ) -> None:
        """Initialize an API error.

        Parameters
        ----------
        message
            Additional error message.
        status
            HTTP status associated with the error.

        """
        _message: str = message

        if status:
            _message = f"{status} {status.phrase}: {status.description}"

            if message:
                _message = f"{_message} - {message}"

        self.message: str = _message
        self.status: HTTPStatus | None = status

    def __str__(self) -> str:
        """Return the error message."""
        return self.message


class InvalidJsonError(APIError):
    """The response of the Web HMI is not valid JSON."""


class AuthenticationError(APIError):
    """The credentials were rejected by the Web HMI (HTTP 401)."""


class APITimeoutError(APIError, TimeoutError):
    """The request to the Web HMI timed out.

    Inherits from ``TimeoutError`` as well, so existing ``except TimeoutError`` handlers keep working.
    """
