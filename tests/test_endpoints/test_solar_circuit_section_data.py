# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_solar_circuit_section.py`."""

from typing import Any
from typing import Final

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
