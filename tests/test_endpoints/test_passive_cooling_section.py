# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the passive cooling endpoints."""

import json
from typing import Any

import pytest
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from tests.conftest import READ_URL

GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]] = [
    ("get_temperature", {}, {"APPL.CtrlAppl.sParam.passivecooling[0].TempCoolPassive.values.actValue": "20.6"}, 20.6),
    (
        "get_switch_valve_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.passivecooling[0].SwitchValvePassiveCool.values.actPosition": "1"},
        "open",
    ),
    (
        "get_switch_valve_position",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.passivecooling[0].SwitchValvePassiveCool.values.actPosition": "0"},
        0,
    ),
    (
        "get_switch_valve_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.passivecooling[0].SwitchValvePassiveCool.values.actPosition": "2"},
        "closed",
    ),
    (
        "get_circulation_pump_speed",
        {},
        {"APPL.CtrlAppl.sParam.passivecooling[0].Pump.values.setValueScaled": "0.2"},
        0.2,
    ),
    ("get_mixer_target_temperature", {}, {"APPL.CtrlAppl.sParam.passivecooling[0].Mixer.values.setValue": "22"}, 22.0),
    (
        "get_mixer_flow_temperature",
        {},
        {"APPL.CtrlAppl.sParam.passivecooling[0].Mixer.flowTemp.values.actValue": "22.1"},
        22.1,
    ),
    (
        "get_mixer_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.passivecooling[0].Mixer.mixer.values.setValueScaled": "-1"},
        "closed",
    ),
    (
        "get_mixer_position",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.passivecooling[0].Mixer.mixer.values.setValueScaled": "0"},
        0,
    ),
    (
        "get_mixer_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.passivecooling[0].Mixer.mixer.values.setValueScaled": "1"},
        "open",
    ),
]


class TestHappyPathPassiveCoolingSection:
    """Tests for the passive cooling endpoints with valid responses and input."""

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

        data: float | str = await getattr(client.passive_cooling, method)(**kwargs)

        assert data == expected
        assert type(data) is type(expected)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )
