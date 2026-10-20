# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the switch valve endpoints."""

import json
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from tests.conftest import READ_URL
from tests.conftest import case_id
from tests.test_endpoints.test_switch_valve_section_data import GETTERS


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

    data: float | str = await getattr(client.switch_valve, method)(**kwargs)

    assert data == expected
    assert type(data) is type(expected)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in response]),
        method="POST",
        headers={},
        ssl=False,
    )
