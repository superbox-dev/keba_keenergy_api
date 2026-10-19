# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the photovoltaics endpoints."""

import json
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from tests.conftest import READ_URL

GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]] = [
    (
        "get_excess_energy_active",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": "true"},
        "on",
    ),
    (
        "get_excess_energy_active",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": 1},
        1,
    ),
    (
        "get_excess_energy_active",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": "false"},
        "off",
    ),
    (
        "get_excess_energy_active",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": 0},
        0,
    ),
    ("get_excess_power", {}, {"APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.power": "23.234"}, 23.23),
    (
        "get_daily_energy",
        {},
        {"APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.heatDay": "49.394"},
        49.39,
    ),
    (
        "get_total_energy",
        {},
        {"APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat": "349442.23"},
        349442.23,
    ),
]


class TestHappyPathPhotovoltaicsSection:
    """Tests for the photovoltaics endpoints with valid responses and input."""

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

        data: float | str = await getattr(client.photovoltaics, method)(**kwargs)

        assert data == expected
        assert type(data) is type(expected)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )
