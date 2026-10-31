# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Shared fixtures for the tests."""

import json
from collections.abc import Callable
from collections.abc import Iterator
from typing import Any
from typing import Final

import pytest
from aiohttp import ClientTimeout
from aioresponses import aioresponses

from keba_keenergy_api.client import KebaKeEnergyAPI
from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.models import DeviceCounts

READ_URL: Final = "http://mocked-host/var/readWriteVars"
WRITE_URL: Final = f"{READ_URL}?action=set"
TIMEOUT: Final = ClientTimeout(total=API_DEFAULT_TIMEOUT)

type SentRequests = Callable[[aioresponses], list[dict[str, Any]]]


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
def counts() -> DeviceCounts:
    """Return installed devices with none, one and two devices of a type.

    Returns
    -------
    DeviceCounts
        No buffer tank and switch valve, two heating circuits, one of every other device type.

    """
    return DeviceCounts(
        buffer_tank=0,
        dhw_tank=1,
        external_heat_source=1,
        heat_pump=1,
        heating_circuit=2,
        solar_circuit=1,
        switch_valve=0,
    )


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
