# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the buffer tank endpoints."""

import json
import re
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import WRITE_URL

GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]] = [
    ("get_name", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.name": "Puffer1"}, "Puffer1"),
    (
        "get_current_top_temperature",
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].topTemp.values.actValue": "45.0273"},
        45.03,
    ),
    (
        "get_current_bottom_temperature",
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].midTemp.values.actValue": "33.094"},
        33.09,
    ),
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "2"},
        "heat_up",
    ),
    (
        "get_operating_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "2"},
        2,
    ),
    ("get_standby_temperature", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.backupTemp": "10"}, 10.0),
    ("get_target_temperature", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].values.setTemp": "37.75"}, 37.75),
    (
        "get_excess_energy_target_temperature",
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.value": "55"},
        55.0,
    ),
    (
        "get_excess_energy_target_temperature_hysteresis",
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.hyst": "2"},
        2.0,
    ),
    (
        "get_outdoor_temperature_excess_energy_limit",
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.thresholdOutTempExcessEnergy.value": "25"},
        25.0,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "true"},
        "on",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "false"},
        "off",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "true"},
        1,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "false"},
        0,
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.useExcessEnergy": "2"},
        "cooling",
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.useExcessEnergy": "1"},
        1,
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.useExcessEnergy": "0"},
        "off",
    ),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.heatRequestTop": "true"},
        "on",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.bufferTank[0].values.heatRequestTop": 1}, 1),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.heatRequestTop": "false"},
        "off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.bufferTank[0].values.heatRequestTop": 0}, 0),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.coolRequestBot": "true"},
        "on",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.bufferTank[0].values.coolRequestBot": 1}, 1),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].values.coolRequestBot": "false"},
        "off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.bufferTank[0].values.coolRequestBot": 0}, 0),
]

INVALID_GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], str]] = [
    (
        "get_operating_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "-0.010321236"},
        (
            "Can't convert value to type \"int\"! {'name': "
            "'APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode', 'value': '-0.010321236'}"
        ),
    ),
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "10"},
        (
            "Can't convert value to human readable value! {'name': "
            "'APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode', 'value': '10'}"
        ),
    ),
]

SETTERS: list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]] = [
    ("set_operating_mode", "off", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "0"}),
    ("set_operating_mode", "ON", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "1"}),
    ("set_operating_mode", 2, {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode": "2"}),
    ("set_standby_temperature", 10, {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.backupTemp": "10"}),
    (
        "set_excess_energy_target_temperature",
        43,
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.value": "43"},
    ),
    (
        "set_excess_energy_target_temperature_hysteresis",
        3,
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.hyst": "3"},
    ),
    (
        "set_outdoor_temperature_excess_energy_limit",
        22,
        {},
        {"APPL.CtrlAppl.sParam.bufferTank[0].param.thresholdOutTempExcessEnergy.value": "22"},
    ),
    ("set_use_excess_energy", "off", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "0"}),
    ("set_use_excess_energy", "ON", {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "1"}),
    ("set_use_excess_energy", 1, {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "1"}),
    ("set_use_excess_energy", 0, {}, {"APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy": "0"}),
]

INVALID_SETTERS: list[tuple[str, int | str, dict[str, Any], str]] = [
    ("set_use_excess_energy", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    ("set_operating_mode", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1', 'HEAT_UP', '2']"),
]


class TestHappyPathBufferTankSection:
    """Tests for the buffer tank endpoints with valid responses and input."""

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

        data: float | str = await getattr(client.buffer_tank, method)(**kwargs)

        assert data == expected
        assert type(data) is type(expected)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize(("method", "value", "kwargs", "expected"), SETTERS)
    async def test_setter(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        method: str,
        value: float | str,
        kwargs: dict[str, Any],
        expected: dict[str, str],
    ) -> None:
        """Test that a setter writes the expected variables."""
        mock_api.post(WRITE_URL, payload={})

        await getattr(client.buffer_tank, method)(value, **kwargs)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
            method="POST",
            headers={},
            ssl=False,
        )


class TestUnhappyPathBufferTankSection:
    """Tests for the buffer tank endpoints with invalid responses and input."""

    @pytest.mark.parametrize(("method", "kwargs", "response", "message"), INVALID_GETTERS)
    async def test_invalid_getter(
        self,
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
            await getattr(client.buffer_tank, method)(**kwargs)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize(("method", "value", "kwargs", "message"), INVALID_SETTERS)
    async def test_invalid_setter(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        method: str,
        value: str,
        kwargs: dict[str, Any],
        message: str,
    ) -> None:
        """Test that a setter raises `APIError` for an invalid value and sends no request."""
        with pytest.raises(APIError, match=re.escape(message)):
            await getattr(client.buffer_tank, method)(value, **kwargs)

        mock_api.assert_not_called()
