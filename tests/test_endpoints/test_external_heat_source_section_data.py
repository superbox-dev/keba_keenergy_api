# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_external_heat_source_section.py`."""

from typing import Any
from typing import Final

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
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
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "2"},
        "flue",
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

SETTERS: Final[list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]]] = [
    ("set_operating_mode", "on", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "1"}),
    ("set_operating_mode", "OFF", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "0"}),
    ("set_operating_mode", 1, {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "1"}),
    ("set_operating_mode", "flue", {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "2"}),
    ("set_operating_mode", 2, {}, {"APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode": "2"}),
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

INVALID_SETTERS: Final[list[tuple[str, int | str, dict[str, Any], str]]] = [
    ("set_use_excess_energy", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    (
        "set_operating_mode",
        "INVALID",
        {},
        "Invalid value! Allowed values are ['OFF', '0', 'ON', '1', 'FLUE', '2']",
    ),
]
