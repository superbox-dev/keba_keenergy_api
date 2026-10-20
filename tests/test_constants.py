# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the endpoint definitions."""

from enum import Enum

import pytest

from keba_keenergy_api.constants import FloatEndpoint
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import SectionPrefix
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import System
from keba_keenergy_api.endpoints import BaseEndpoints
from tests.test_constants_data import SECTIONS


class TestConstants:
    """Tests for the endpoint definitions in `constants.py`."""

    @pytest.mark.parametrize(
        ("section", "expected"),
        [
            (HeatPump.HAS_VFD_FAILURE, "APPL.CtrlAppl.sParam.heatpump[%s].FailureVFD.state.msgId"),
            (System.OUTDOOR_TEMPERATURE, "APPL.CtrlAppl.sParam.outdoorTemp.state.msgId"),
            (SolarCircuit.CURRENT_TEMPERATURE, "APPL.CtrlAppl.sParam.genericHeat[%s].referenceTemp.state.msgId"),
            (HeatPump.STATE, None),
            (HeatCircuit.HAS_ROOM_TEMPERATURE, None),
        ],
        ids=[
            "heat_pump_failure",
            "system",
            "solar_circuit",
            "heat_pump_without_message_id",
            "heat_circuit_without_message_id",
        ],
    )
    def test_message_id_path(self, section: Enum, expected: str | None) -> None:
        """Test the message id path of an endpoint."""
        assert section.value.message_id_path == expected

    def test_message_id_requires_act_value(self) -> None:
        """Test that `has_message_id` raises `ValueError` for a path without `values.actValue`."""
        with pytest.raises(
            ValueError,
            match=r"message id is not supported for 'APPL\.CtrlAppl\.sParam\.heatpump\[%s\]\.values\.COP'",
        ):
            FloatEndpoint("APPL.CtrlAppl.sParam.heatpump[%s].values.COP", has_message_id=True)

    @pytest.mark.parametrize("section", SECTIONS, ids=lambda section: section.__name__)
    def test_every_section_has_prefix(self, section: type[Enum]) -> None:
        # `read_data()` groups the values by these prefixes.
        """Test that every section enum has a `SectionPrefix` member."""
        assert BaseEndpoints.KEY_PATTERN.sub("_", section.__name__).lower() in set(SectionPrefix)

    @pytest.mark.parametrize("section", [member for enum in SECTIONS for member in enum], ids=str)
    def test_every_act_value_has_message_id(self, section: Enum) -> None:
        # Every sensor value (values.actValue) has a confirmed state.msgId on the control unit.
        """Test that exactly the `values.actValue` endpoints have a message id."""
        assert section.value.has_message_id is section.value.value.endswith(".values.actValue")

    @pytest.mark.parametrize(
        ("path", "expected_read_only"),
        [
            ("APPL.CtrlAppl.sParam.heatpump[%s].param.name", False),
            ("APPL.CtrlAppl.sParam.heatpump[%s].values.COP", True),
        ],
        ids=["writable", "read_only"],
    )
    def test_read_only(self, path: str, *, expected_read_only: bool) -> None:
        """Test that only paths containing `.param.` are writable."""
        assert FloatEndpoint(path).read_only is expected_read_only

    def test_extra_writes(self) -> None:
        """Test the extra writes of `SolarCircuit.PRIORITY_1_BEFORE_2`."""
        assert HeatPump.STATE.value.extra_writes([1]) == {}
        assert SolarCircuit.PRIORITY_1_BEFORE_2.value.extra_writes([1, 0, None, 2]) == {
            SolarCircuit["_PRIORITY"]: [14, None, 15, None, None, None, None, None],
        }
