# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the solar circuit endpoints."""

import json
import re
from typing import Any
from typing import Final

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import WRITE_URL
from tests.conftest import case_id

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
    ("get_name", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].param.name": "Diff. Regler 1"}, "Diff. Regler 1"),
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode": "1"},
        "on",
    ),
    (
        "get_operating_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode": "0"},
        0,
    ),
    (
        "get_priority_1_before_2",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[0]": "true"},
        "on",
    ),
    (
        "get_priority_1_before_2",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[0]": "false"},
        0,
    ),
    (
        "get_source_temperature",
        {},
        {"APPL.CtrlAppl.sParam.solarCircuit[0].collectorTemp.values.actValue": "22.426912"},
        22.43,
    ),
    ("get_pump_1_speed", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].values.pump1": "0.5"}, 0.5),
    ("get_pump_2_speed", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].values.pump2": "0.55"}, 0.55),
    (
        "get_current_temperature_1",
        {},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue": "55.753",
            "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue": "25.753",
        },
        55.75,
    ),
    (
        "get_current_temperature_2",
        {},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue": "55.753",
            "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue": "25.753",
        },
        25.75,
    ),
    (
        "get_target_temperature_1",
        {},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value": "55",
            "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value": "45",
        },
        55.0,
    ),
    (
        "get_target_temperature_2",
        {},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value": "55",
            "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value": "35",
        },
        35.0,
    ),
    (
        "get_heat_request_1",
        {"human_readable": True},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": "true",
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": "false",
        },
        "on",
    ),
    (
        "get_heat_request_1",
        {"human_readable": False},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": 1,
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": "true",
        },
        1,
    ),
    (
        "get_heat_request_1",
        {"human_readable": True},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": "false",
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": "true",
        },
        "off",
    ),
    (
        "get_heat_request_1",
        {"human_readable": False},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": 0,
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": "true",
        },
        0,
    ),
    (
        "get_heat_request_2",
        {"human_readable": True},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": "false",
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": "true",
        },
        "on",
    ),
    (
        "get_heat_request_2",
        {"human_readable": False},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": "true",
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": 1,
        },
        1,
    ),
    (
        "get_heat_request_2",
        {"human_readable": True},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": "true",
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": "false",
        },
        "off",
    ),
    (
        "get_heat_request_2",
        {"human_readable": False},
        {
            "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest": "true",
            "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest": 0,
        },
        0,
    ),
    ("get_heating_energy", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.accumulatedHeat": "8.43"}, 8.43),
    ("get_daily_energy", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.heatDay": "1.23"}, 1.23),
    ("get_actual_power", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.power": "3.23"}, 3.23),
]

SETTERS: Final[list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]]] = [
    ("set_operating_mode", "on", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode": "1"}),
    ("set_operating_mode", "OFF", {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode": "0"}),
    ("set_operating_mode", 1, {}, {"APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode": "1"}),
    (
        "set_priority_1_before_2",
        "on",
        {"position": 2},
        {
            "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[1]": "1",
            "APPL.CtrlAppl.sParam.genericHeat[2].param.priority": "14",
        },
    ),
    (
        "set_priority_1_before_2",
        "OFF",
        {"position": 2},
        {
            "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[1]": "0",
            "APPL.CtrlAppl.sParam.genericHeat[2].param.priority": "15",
        },
    ),
    (
        "set_priority_1_before_2",
        1,
        {"position": 2},
        {
            "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[1]": "1",
            "APPL.CtrlAppl.sParam.genericHeat[2].param.priority": "14",
        },
    ),
    ("set_target_temperature_1", 47, {}, {"APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value": "47"}),
    ("set_target_temperature_2", 37, {}, {"APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value": "37"}),
    (
        "set_target_temperature_1",
        47,
        {"position": 2},
        {"APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value": "47"},
    ),
    (
        "set_target_temperature_2",
        47,
        {"position": 2},
        {"APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value": "47"},
    ),
]

INVALID_SETTERS: Final[list[tuple[str, int | str, dict[str, Any], str]]] = [
    ("set_operating_mode", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    (
        "set_priority_1_before_2",
        "INVALID",
        {"position": 2},
        "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']",
    ),
]


class TestHappyPathSolarCircuitSection:
    """Tests for the solar circuit endpoints with valid responses and input."""

    @pytest.mark.parametrize(
        ("method", "kwargs", "response", "expected"),
        GETTERS,
        ids=[case_id(method, kwargs, *response.values(), expected) for method, kwargs, response, expected in GETTERS],
    )
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

        data: float | str = await getattr(client.solar_circuit, method)(**kwargs)

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

        await getattr(client.solar_circuit, method)(value, **kwargs)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
            method="POST",
            headers={},
            ssl=False,
        )


class TestUnhappyPathSolarCircuitSection:
    """Tests for the solar circuit endpoints with invalid responses and input."""

    @pytest.mark.parametrize(
        ("method", "value", "kwargs", "message"),
        INVALID_SETTERS,
        ids=[case_id(method, kwargs, value) for method, value, kwargs, _ in INVALID_SETTERS],
    )
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
            await getattr(client.solar_circuit, method)(value, **kwargs)

        mock_api.assert_not_called()
