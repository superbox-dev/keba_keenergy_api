# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the system endpoints."""

import json
import re
from typing import Any
from typing import Final

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import WRITE_URL
from tests.conftest import case_id

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
    ("get_number_of_buffer_tanks", {}, {"APPL.CtrlAppl.sParam.options.systemNumberOfBuffers": "2"}, 2),
    ("get_number_of_hot_water_tanks", {}, {"APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks": "2"}, 2),
    ("get_number_of_heat_pumps", {}, {"APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps": "1"}, 1),
    ("get_number_of_heating_circuits", {}, {"APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits": "3"}, 3),
    ("get_number_of_external_heat_sources", {}, {"APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources": "1"}, 1),
    ("get_number_of_switch_valves", {}, {"APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves": "1"}, 1),
    ("has_photovoltaics", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.hasPhotovoltaics": "true"}, "on"),
    ("has_photovoltaics", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.hasPhotovoltaics": 1}, 1),
    ("has_photovoltaics", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.hasPhotovoltaics": "false"}, "off"),
    ("has_photovoltaics", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.hasPhotovoltaics": 0}, 0),
    (
        "has_outdoor_temperature",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.hasOutdoorTemp": "true"},
        "on",
    ),
    ("has_outdoor_temperature", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.hasOutdoorTemp": 1}, 1),
    (
        "has_outdoor_temperature",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.hasOutdoorTemp": "false"},
        "off",
    ),
    ("has_outdoor_temperature", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.hasOutdoorTemp": 0}, 0),
    ("get_operating_mode", {"human_readable": True}, {"APPL.CtrlAppl.sParam.param.operatingMode": "1"}, "summer"),
    ("get_operating_mode", {"human_readable": False}, {"APPL.CtrlAppl.sParam.param.operatingMode": "2"}, 2),
    ("get_cpu_usage", {}, {"APPL.CtrlAppl.sProcData.globalCpuTimePercent": "27"}, 2.7),
    ("get_webview_cpu_usage", {}, {"APPL.CtrlAppl.sProcData.processStatus[0].cpuTimePercent": "34"}, 3.4),
    ("get_webserver_cpu_usage", {}, {"APPL.CtrlAppl.sProcData.processStatus[1].cpuTimePercent": "67"}, 6.7),
    ("get_control_cpu_usage", {}, {"APPL.CtrlAppl.sProcData.processStatus[2].cpuTimePercent": "7"}, 0.7),
    ("get_ram_usage", {}, {"APPL.CtrlAppl.sProcData.RAMstatus.tmpfs": "6432"}, 6432),
    ("get_free_ram", {}, {"APPL.CtrlAppl.sProcData.totFreeRAM": "100060"}, 100060),
]

SETTERS: Final[list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]]] = [
    ("set_operating_mode", "summer", {}, {"APPL.CtrlAppl.sParam.param.operatingMode": "1"}),
    ("set_operating_mode", "AUTO_HEAT", {}, {"APPL.CtrlAppl.sParam.param.operatingMode": "2"}),
    ("set_operating_mode", 3, {}, {"APPL.CtrlAppl.sParam.param.operatingMode": "3"}),
]

INVALID_SETTERS: Final[list[tuple[str, int | str, dict[str, Any], str]]] = [
    (
        "set_operating_mode",
        "INVALID",
        {},
        (
            "Invalid value! Allowed values are ['SETUP', '-1', 'STANDBY', '0', "
            "'SUMMER', '1', 'AUTO_HEAT', '2', 'AUTO_COOL', '3', 'AUTO', '4']"
        ),
    ),
]

POSITION_NAMES: Final[list[str]] = [
    "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
    "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
    "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits",
    "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers",
    "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
    "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources",
    "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves",
]


class TestHappyPathSystemSection:
    """Tests for the system endpoints with valid responses and input."""

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

        await getattr(client.system, method)(value, **kwargs)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
            method="POST",
            headers={},
            ssl=False,
        )

    async def test_get_positions(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
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
        self,
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


class TestUnhappyPathSystemSection:
    """Tests for the system endpoints with invalid responses and input."""

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
            await getattr(client.system, method)(value, **kwargs)

        mock_api.assert_not_called()
