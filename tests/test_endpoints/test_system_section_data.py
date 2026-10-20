# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_system_section.py`."""

from typing import Any
from typing import Final

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
