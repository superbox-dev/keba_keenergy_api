# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the hot water tank endpoints."""

import json
import re
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import TIMEOUT
from tests.conftest import WRITE_URL
from tests.conftest import case_id
from tests.test_endpoints.test_hot_water_tank_section_data import GETTERS
from tests.test_endpoints.test_hot_water_tank_section_data import INVALID_GETTERS
from tests.test_endpoints.test_hot_water_tank_section_data import INVALID_SETTERS
from tests.test_endpoints.test_hot_water_tank_section_data import LIMIT_GETTERS
from tests.test_endpoints.test_hot_water_tank_section_data import SETTERS


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

    data: float | str = await getattr(client.hot_water_tank, method)(**kwargs)

    assert data == expected
    assert type(data) is type(expected)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in response]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
    )


@pytest.mark.parametrize(
    ("method", "kwargs", "response", "message"),
    INVALID_GETTERS,
    ids=[case_id(method, kwargs, *response.values()) for method, kwargs, response, _ in INVALID_GETTERS],
)
async def test_getter_invalid_value(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    kwargs: dict[str, Any],
    response: dict[str, Any],
    message: str,
) -> None:
    """Test that a getter raises `APIError` for a value that can't be converted."""
    mock_api.post(READ_URL, payload=[{"name": name, "value": value} for name, value in response.items()])

    with pytest.raises(APIError, match=re.escape(message)):
        await getattr(client.hot_water_tank, method)(**kwargs)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in response]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
    )


@pytest.mark.parametrize(
    ("method", "kwargs", "item", "expected"),
    LIMIT_GETTERS,
    ids=[case_id(method, kwargs, expected) for method, kwargs, _, expected in LIMIT_GETTERS],
)
async def test_limit_getter(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    kwargs: dict[str, Any],
    item: dict[str, Any],
    expected: float,
) -> None:
    """Test that a limit getter returns the limit from the attributes and not the value."""
    mock_api.post(READ_URL, payload=[item])

    data: float = await getattr(client.hot_water_tank, method)(**kwargs)

    assert data == expected
    assert type(data) is type(expected)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": item["name"], "attr": "1"}]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
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

    await getattr(client.hot_water_tank, method)(value, **kwargs)

    mock_api.assert_called_once_with(
        url=WRITE_URL,
        data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
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
        await getattr(client.hot_water_tank, method)(value, **kwargs)

    mock_api.assert_not_called()
