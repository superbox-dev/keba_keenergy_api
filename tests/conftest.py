# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Shared fixtures for the tests."""

import json
from collections.abc import Callable
from collections.abc import Iterator
from typing import Any
from typing import Final
from typing import TypeAlias

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI

READ_URL: Final[str] = "http://mocked-host/var/readWriteVars"
WRITE_URL: Final[str] = f"{READ_URL}?action=set"

SentRequests: TypeAlias = Callable[[aioresponses], list[dict[str, Any]]]


def case_id(method: str, kwargs: dict[str, Any], /, *values: object) -> str:
    """Return the test id of an endpoint test case.

    Parameters
    ----------
    method
        Name of the endpoint method.
    kwargs
        Keyword arguments of the method call.
    *values
        Further values that tell the cases apart, e.g. the raw and the expected value.

    Returns
    -------
    str
        The method, the keyword arguments and the values, joined by ``-``.

    """
    return "-".join([method, *(f"{key}_{value}" for key, value in kwargs.items()), *(str(value) for value in values)])


@pytest.fixture
def client() -> KebaKeEnergyAPI:
    """Return a client for the mocked host.

    Returns
    -------
    KebaKeEnergyAPI
        Client without authentication and SSL.

    """
    return KebaKeEnergyAPI(host="mocked-host")


@pytest.fixture
def mock_api() -> Iterator[aioresponses]:
    """Mock all requests sent with `aiohttp`.

    Yields
    ------
    aioresponses
        Mock to register the responses and check the sent requests.

    """
    with aioresponses() as mock:
        yield mock


@pytest.fixture
def sent_requests() -> SentRequests:
    """Return a function that lists the requests sent to the mocked API.

    The JSON body is decoded, so a snapshot shows one line per variable instead of one long string.

    Returns
    -------
    SentRequests
        Function that returns the method, URL and decoded body (``None`` without body) of every request,
        grouped by URL.

    """

    def _sent_requests(mock: aioresponses) -> list[dict[str, Any]]:
        return [
            {
                "method": method,
                "url": str(url),
                "data": None if call.kwargs.get("data") is None else json.loads(call.kwargs["data"]),
            }
            for (method, url), calls in (mock.requests or {}).items()
            for call in calls
        ]

    return _sent_requests
