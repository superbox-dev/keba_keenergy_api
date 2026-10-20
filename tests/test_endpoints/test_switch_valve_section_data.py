# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_switch_valve_section.py`."""

from typing import Any
from typing import Final

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
    ("get_position", {"human_readable": True}, {"APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition": "1"}, "open"),
    ("get_position", {"human_readable": False}, {"APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition": "0"}, 0),
    (
        "get_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition": "2"},
        "closed",
    ),
]
