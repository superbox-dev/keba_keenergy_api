# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the external heat source endpoints."""

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
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "1"},
        "on",
    ),
    (
        "get_operating_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "0"},
        0,
    ),
    ("get_target_temperature", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].values.setTemp": "22.56"}, 22.56),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.values.setValueB": "true"},
        "on",
    ),
    (
        "get_heat_request",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.values.setValueB": 1},
        1,
    ),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.values.setValueB": "false"},
        "off",
    ),
    (
        "get_heat_request",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.values.setValueB": 0},
        0,
    ),
    (
        "get_operating_time",
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.operationalTimeS": "3809028"},
        3809028,
    ),
    ("get_max_runtime", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.maxRunTimeS": "602403"}, 602403),
    (
        "get_activation_counter",
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.activationCounter": "477"},
        477,
    ),
    (
        "get_consuming_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].values.consumingExcessEnergy": "true"},
        "on",
    ),
    (
        "get_consuming_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].values.consumingExcessEnergy": 1},
        1,
    ),
    (
        "get_consuming_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].values.consumingExcessEnergy": "false"},
        "off",
    ),
    (
        "get_consuming_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].values.consumingExcessEnergy": 0},
        0,
    ),
    (
        "get_excess_energy_operating_time",
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].operationalDataExcessEnergy.operationalTimeS": "3809028"},
        3809028,
    ),
    (
        "get_excess_energy_max_runtime",
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].operationalDataExcessEnergy.maxRunTimeS": "602403"},
        602403,
    ),
    (
        "get_excess_energy_activation_counter",
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].operationalDataExcessEnergy.activationCounter": "477"},
        477,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "true"},
        "on",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "false"},
        "off",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "true"},
        1,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "false"},
        0,
    ),
    (
        "get_min_runtime_excess_energy",
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.minRunTimeExcessEnergy": "2"},
        2,
    ),
]

SETTERS: list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]] = [
    ("set_operating_mode", "on", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "1"}),
    ("set_operating_mode", "OFF", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "0"}),
    ("set_operating_mode", 1, {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "1"}),
    ("set_use_excess_energy", "off", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "0"}),
    ("set_use_excess_energy", "ON", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "1"}),
    ("set_use_excess_energy", 1, {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "1"}),
    ("set_use_excess_energy", 0, {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.supportExcessEnergy": "0"}),
    (
        "set_min_runtime_excess_energy",
        5,
        {},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.minRunTimeExcessEnergy": "5"},
    ),
]

INVALID_SETTERS: list[tuple[str, int | str, dict[str, Any], str]] = [
    ("set_use_excess_energy", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    ("set_operating_mode", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
]


class TestHappyPathExternalHeatSourceSection:
    """Tests for the external heat source endpoints with valid responses and input."""

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

        data: float | str = await getattr(client.external_heat_source, method)(**kwargs)

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

        await getattr(client.external_heat_source, method)(value, **kwargs)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
            method="POST",
            headers={},
            ssl=False,
        )


class TestUnhappyPathExternalHeatSourceSection:
    """Tests for the external heat source endpoints with invalid responses and input."""

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
            await getattr(client.external_heat_source, method)(value, **kwargs)

        mock_api.assert_not_called()
