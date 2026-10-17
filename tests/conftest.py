# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Shared fixtures for the tests."""

import json
from collections.abc import Callable
from typing import Any
from typing import TypeAlias

import pytest
from aioresponses import aioresponses

SentRequests: TypeAlias = Callable[[aioresponses], list[dict[str, Any]]]


@pytest.fixture
def sent_requests() -> SentRequests:
    """Return a function that lists the requests sent to the mocked API.

    The JSON body is decoded, so a snapshot shows one line per variable instead of one long string.

    Returns
    -------
    SentRequests
        Function that returns the method, URL and decoded body of every request, grouped by URL.

    """

    def _sent_requests(mock: aioresponses) -> list[dict[str, Any]]:
        return [
            {"method": method, "url": str(url), "data": json.loads(call.kwargs["data"])}
            for (method, url), calls in (mock.requests or {}).items()
            for call in calls
        ]

    return _sent_requests
