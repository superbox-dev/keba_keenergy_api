# Copyright 2023 Michael Hacker
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
from tests.conftest import WRITE_URL

GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]] = [
    ("get_name", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.name": "Boiler"}, "Boiler"),
    (
        "get_current_temperature",
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue": "58.900002"},
        58.9,
    ),
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode": "3"},
        "heat_up",
    ),
    (
        "get_operating_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode": "3"},
        3,
    ),
    ("get_target_temperature", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value": "47"}, 47.0),
    ("get_standby_temperature", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value": "0"}, 0.0),
    (
        "get_excess_energy_target_temperature",
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.excessEnergyTemp.value": "55"},
        55.0,
    ),
    (
        "get_excess_energy_target_temperature_hysteresis",
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.excessEnergyTemp.hyst": "5"},
        5.0,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "true"},
        "on",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "false"},
        "off",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "true"},
        1,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "false"},
        0,
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.useExcessEnergy": 2},
        "cooling",
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.useExcessEnergy": 0},
        0,
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.useExcessEnergy": 1},
        1,
    ),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.heatRequestTop": "true"},
        "on",
    ),
    (
        "get_heat_request",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.heatRequestTop": 1},
        1,
    ),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.heatRequestTop": "false"},
        "off",
    ),
    (
        "get_heat_request",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].values.heatRequestTop": 0},
        0,
    ),
    (
        "has_fresh_water_module",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.hotWaterTank[0].hasFreshWaterModule": "true"},
        "on",
    ),
    (
        "has_fresh_water_module",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.hotWaterTank[0].hasFreshWaterModule": 1},
        1,
    ),
    (
        "has_fresh_water_module",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.hotWaterTank[0].hasFreshWaterModule": "false"},
        "off",
    ),
    (
        "has_fresh_water_module",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.hotWaterTank[0].hasFreshWaterModule": 0},
        0,
    ),
    (
        "get_fresh_water_flow",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterFlow.values.actValue": "true"},
        "on",
    ),
    (
        "get_fresh_water_flow",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterFlow.values.actValue": 1},
        1,
    ),
    (
        "get_fresh_water_flow",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterFlow.values.actValue": "false"},
        "off",
    ),
    (
        "get_fresh_water_flow",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterFlow.values.actValue": 0},
        0,
    ),
    (
        "get_fresh_water_module_temperature",
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterTemp.values.actValue": "30"},
        30.0,
    ),
    (
        "get_fresh_water_module_pump_speed",
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterPump.values.setValueScaled": "0.40020001"},
        0.4002,
    ),
    (
        "get_circulation_return_temperature",
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].circTemp.values.actValue": "47.44"},
        47.44,
    ),
    (
        "get_circulation_pump_state",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].circPump.pump.values.setValueB": "true"},
        "on",
    ),
    (
        "get_circulation_pump_state",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].circPump.pump.values.setValueB": 1},
        1,
    ),
    (
        "get_circulation_pump_state",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].circPump.pump.values.setValueB": "false"},
        "off",
    ),
    (
        "get_circulation_pump_state",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].circPump.pump.values.setValueB": 0},
        0,
    ),
    (
        "has_fresh_water_module",
        {"position": 2},
        {"APPL.CtrlAppl.sParam.options.hotWaterTank[1].hasFreshWaterModule": "true"},
        "on",
    ),
]

LIMIT_GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int]] = [
    (
        "get_min_target_temperature",
        {},
        {
            "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
            "attributes": {"lowerLimit": "0", "upperLimit": "52"},
            "value": "50",
        },
        0,
    ),
    (
        "get_max_target_temperature",
        {},
        {
            "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
            "attributes": {"lowerLimit": "0", "upperLimit": "52"},
            "value": "50",
        },
        52,
    ),
    (
        "get_max_target_temperature",
        {"position": 2},
        {
            "name": "APPL.CtrlAppl.sParam.hotWaterTank[1].param.normalSetTempMax.value",
            "attributes": {"lowerLimit": "0", "upperLimit": "52"},
            "value": "50",
        },
        52,
    ),
]

INVALID_GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], str]] = [
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode": "10"},
        (
            "Can't convert value to human readable value! {'name': "
            "'APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode', 'value': '10'}"
        ),
    ),
]

SETTERS: list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]] = [
    ("set_operating_mode", "off", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode": "0"}),
    ("set_operating_mode", "OFF", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode": "0"}),
    ("set_operating_mode", 3, {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode": "3"}),
    ("set_target_temperature", 47, {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value": "47"}),
    ("set_standby_temperature", 10, {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value": "10"}),
    (
        "set_excess_energy_target_temperature",
        60,
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.excessEnergyTemp.value": "60"},
    ),
    (
        "set_excess_energy_target_temperature_hysteresis",
        3,
        {},
        {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.excessEnergyTemp.hyst": "3"},
    ),
    ("set_use_excess_energy", "off", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "0"}),
    ("set_use_excess_energy", "ON", {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "1"}),
    ("set_use_excess_energy", 1, {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "1"}),
    ("set_use_excess_energy", 0, {}, {"APPL.CtrlAppl.sParam.hotWaterTank[0].param.useExcessEnergy": "0"}),
]

INVALID_SETTERS: list[tuple[str, int | str, dict[str, Any], str]] = [
    ("set_use_excess_energy", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    (
        "set_operating_mode",
        "INVALID",
        {},
        "Invalid value! Allowed values are ['OFF', '0', 'AUTO', '1', 'ON', '2', 'HEAT_UP', '3']",
    ),
]


class TestHappyPathHotWaterTankSection:
    """Tests for the hot water tank endpoints with valid responses and input."""

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

        data: float | str = await getattr(client.hot_water_tank, method)(**kwargs)

        assert data == expected
        assert type(data) is type(expected)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize(("method", "kwargs", "item", "expected"), LIMIT_GETTERS)
    async def test_limit_getter(
        self,
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

        await getattr(client.hot_water_tank, method)(value, **kwargs)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
            method="POST",
            headers={},
            ssl=False,
        )


class TestUnhappyPathHotWaterTankSection:
    """Tests for the hot water tank endpoints with invalid responses and input."""

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
            await getattr(client.hot_water_tank, method)(**kwargs)

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
            await getattr(client.hot_water_tank, method)(value, **kwargs)

        mock_api.assert_not_called()
