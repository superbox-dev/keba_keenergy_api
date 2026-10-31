# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""KEBA KeEnergy API exceptions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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

        super().__init__(_message)
        self.message: str = _message
        self.status: HTTPStatus | None = status

    def __str__(self) -> str:
        """Return the error message."""
        return self.message


class AuthenticationError(APIError):
    """The credentials were rejected by the Web HMI (HTTP 401)."""


class APITimeoutError(APIError, TimeoutError):
    """The request to the Web HMI timed out."""


class InvalidResponseError(APIError):
    """The response of the Web HMI is not valid JSON or a value can't be converted to the endpoint type."""


class UnsupportedVariableError(APIError):
    """The Web HMI doesn't know a requested variable, e.g. because its software version is too old."""

    def __init__(self, message: str = "", /, *, variable: str, status: HTTPStatus | None = None) -> None:
        """Initialize the error.

        Parameters
        ----------
        message
            Additional error message.
        variable
            Name of the unknown variable, e.g. ``APPL.CtrlAppl.sParam.heatpump[0].values.COP``.
        status
            HTTP status associated with the error.

        """
        super().__init__(message, status=status)
        self.variable: str = variable
