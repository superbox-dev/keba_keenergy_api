# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the exceptions."""

from http import HTTPStatus

import pytest

from keba_keenergy_api.exceptions import APIError


@pytest.mark.parametrize(
    ("message", "status", "expected"),
    [
        ("mocked-error", None, "mocked-error"),
        ("", HTTPStatus.NOT_FOUND, "404 Not Found: Nothing matches the given URI"),
        ("mocked-error", HTTPStatus.NOT_FOUND, "404 Not Found: Nothing matches the given URI - mocked-error"),
    ],
    ids=["message", "status", "status_and_message"],
)
def test_api_error(message: str, status: HTTPStatus | None, expected: str) -> None:
    """Test the message of an `APIError` with and without HTTP status."""
    error: APIError = APIError(message, status=status)

    assert str(error) == expected
    assert error.message == expected
    assert error.status is status
