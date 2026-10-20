# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the system endpoints."""

import json
import re
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import WRITE_URL
from tests.conftest import case_id
from tests.test_endpoints.test_system_section_data import GETTERS
from tests.test_endpoints.test_system_section_data import INVALID_SETTERS
from tests.test_endpoints.test_system_section_data import POSITION_NAMES
from tests.test_endpoints.test_system_section_data import SETTERS


@pytest.mark.parametrize(
    ("method", "kwargs", "response", "expected"),
    GETTERS,
    ids=[case_id(method, kwargs, *response.values(), expected) for method, kwargs, response, expected in GETTERS],
)
async def test_getter(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    kwargs: dict[str, Any],
    response: dict[str, Any],
    expected: float | str,
) -> None:
    """Test that a getter reads its variables and returns the converted value."""
    mock_api.post(READ_URL, payload=[{"name": name, "value": value} for name, value in response.items()])

    data: float | str = await getattr(client.system, method)(**kwargs)

    assert data == expected
    assert type(data) is type(expected)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in response]),
        method="POST",
        headers={},
        ssl=False,
    )


@pytest.mark.parametrize(
    ("method", "value", "kwargs", "expected"),
    SETTERS,
    ids=[case_id(method, kwargs, value) for method, value, kwargs, _ in SETTERS],
)
async def test_setter(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    value: float | str,
    kwargs: dict[str, Any],
    expected: dict[str, str],
) -> None:
    """Test that a setter writes the expected variables."""
    mock_api.post(WRITE_URL, payload={})

    await getattr(client.system, method)(value, **kwargs)

    mock_api.assert_called_once_with(
        url=WRITE_URL,
        data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
        method="POST",
        headers={},
        ssl=False,
    )


@pytest.mark.parametrize(
    ("method", "value", "kwargs", "message"),
    INVALID_SETTERS,
    ids=[case_id(method, kwargs, value) for method, value, kwargs, _ in INVALID_SETTERS],
)
async def test_setter_invalid_value(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    value: str,
    kwargs: dict[str, Any],
    message: str,
) -> None:
    """Test that a setter raises `APIError` for an invalid value and sends no request."""
    with pytest.raises(APIError, match=re.escape(message)):
        await getattr(client.system, method)(value, **kwargs)

    mock_api.assert_not_called()


async def test_get_positions(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that `get_positions()` returns the value from the response."""
    mock_api.post(
        READ_URL,
        payload=[{"name": name, "value": value} for name, value in zip(POSITION_NAMES, "2111111", strict=True)],
    )

    response: Position = await client.system.get_positions()

    assert response == Position(
        heat_pump=2,
        heat_circuit=1,
        solar_circuit=1,
        buffer_tank=1,
        hot_water_tank=1,
        external_heat_source=1,
        switch_valve=1,
    )

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in POSITION_NAMES]),
        method="POST",
        headers={},
        ssl=False,
    )


@pytest.mark.parametrize(
    ("method", "endpoint", "payload", "expected"),
    [
        (
            "get_info",
            "swupdate?action=getSystemInstalled",
            [{"ret": "OK", "name": "KeEnergy.MTec", "version": "2.2.2"}],
            {"name": "KeEnergy.MTec", "version": "2.2.2"},
        ),
        (
            "get_info",
            "swupdate?action=getSystemInstalled",
            [{"name": "KeEnergy.MTec"}],
            {"name": "KeEnergy.MTec"},
        ),
        (
            "get_hmi_info",
            "swupdate?action=getHmiInstalled",
            [{"ret": "OK", "name": "KeEnergy.WebHmi_2.2.0.0"}],
            {"name": "KeEnergy.WebHmi_2.2.0.0"},
        ),
        (
            "get_device_info",
            "deviceControl?action=getDeviceInfo",
            [
                {
                    "ret": "OK",
                    "revNo": 2,
                    "orderNo": 12345678,
                    "serNo": 12345678,
                    "name": "MOCKED-NAME",
                    "variantNo": 0,
                },
            ],
            {"revNo": 2, "orderNo": 12345678, "serNo": 12345678, "name": "MOCKED-NAME", "variantNo": 0},
        ),
        (
            "get_timezone",
            "dateTime?action=getTimeZone",
            {"timezone": "Europe/Vienna"},
            "Europe/Vienna",
        ),
    ],
    ids=["get_info", "get_info_without_ret", "get_hmi_info", "get_device_info", "get_timezone"],
)
async def test_get_info(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    endpoint: str,
    payload: dict[str, Any] | list[dict[str, Any]],
    expected: dict[str, Any] | str,
) -> None:
    """Test that the info getters return the response without `ret`."""
    mock_api.post(f"http://mocked-host/{endpoint}", payload=payload)

    data: dict[str, Any] | str = await getattr(client.system, method)()

    assert data == expected

    mock_api.assert_called_once_with(
        url=f"http://mocked-host/{endpoint}",
        method="POST",
        headers={},
        ssl=False,
    )
