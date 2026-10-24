# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_passive_cooling_section.py`."""

from typing import Any
from typing import Final

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
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
