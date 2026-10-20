# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_photovoltaic_section.py`."""

from typing import Any
from typing import Final

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
    (
        "get_excess_energy_active",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": "true"},
        "on",
    ),
    (
        "get_excess_energy_active",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": 1},
        1,
    ),
    (
        "get_excess_energy_active",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": "false"},
        "off",
    ),
    (
        "get_excess_energy_active",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.photovoltaics.values.excessEnergyActive": 0},
        0,
    ),
    ("get_excess_power", {}, {"APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.power": "23.234"}, 23.23),
    (
        "get_daily_energy",
        {},
        {"APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.heatDay": "49.394"},
        49.39,
    ),
    (
        "get_total_energy",
        {},
        {"APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat": "349442.23"},
        349442.23,
    ),
]
