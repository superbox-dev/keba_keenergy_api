# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the switch valve endpoints."""

import json
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from tests.conftest import READ_URL

GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]] = [
    ("get_position", {"human_readable": True}, {"APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition": "1"}, "open"),
    ("get_position", {"human_readable": False}, {"APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition": "0"}, 0),
    (
        "get_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition": "2"},
        "closed",
    ),
]


class TestHappyPathSwitchValveSection:
    """Tests for the switch valve endpoints with valid responses and input."""

    @pytest.mark.parametrize(("method", "kwargs", "response", "expected"), GETTERS)
    async def test_getter(
        self,
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
