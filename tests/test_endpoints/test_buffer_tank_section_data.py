# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_buffer_tank_section.py`."""

from typing import Any
from typing import Final

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
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

INVALID_GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], str]]] = [
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

SETTERS: Final[list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]]] = [
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

INVALID_SETTERS: Final[list[tuple[str, int | str, dict[str, Any], str]]] = [
    ("set_use_excess_energy", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    ("set_operating_mode", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1', 'HEAT_UP', '2']"),
]
