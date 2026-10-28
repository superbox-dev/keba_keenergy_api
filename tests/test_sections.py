# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the endpoint definitions."""

from typing import TYPE_CHECKING
from typing import Any
from typing import get_args

import pytest

from keba_keenergy_api.enums import DeviceType
from keba_keenergy_api.sections import BufferTank
from keba_keenergy_api.sections import Cascade
from keba_keenergy_api.sections import DHWTank
from keba_keenergy_api.sections import Endpoint
from keba_keenergy_api.sections import ExternalHeatSource
from keba_keenergy_api.sections import HeatingCircuit
from keba_keenergy_api.sections import HeatPump
from keba_keenergy_api.sections import PassiveCooling
from keba_keenergy_api.sections import Photovoltaics
from keba_keenergy_api.sections import Section
from keba_keenergy_api.sections import SolarCircuit
from keba_keenergy_api.sections import SwitchValve
from keba_keenergy_api.sections import System

if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion


def test_sections(snapshot: SnapshotAssertion) -> None:
    """Test the variables, types, units, writable state, message ids and quantities of all endpoints."""
    endpoints: dict[str, dict[str, Any]] = {
        str(section): {
            "variable": section.value.variable,
            "value_type": section.value.value_type.__name__,
            "unit": section.value.unit,
            "writable": section.value.writable,
            "message_id": section.value.message_id_variable,
            "quantity": section.value.quantity,
        }
        for section_class in get_args(Section.__value__)
        for section in section_class
    }

    assert endpoints == snapshot


@pytest.mark.parametrize(
    ("section_class", "expected"),
    [
        (BufferTank, DeviceType.BUFFER_TANK),
        (Cascade, DeviceType.CASCADE),
        (DHWTank, DeviceType.DHW_TANK),
        (ExternalHeatSource, DeviceType.EXTERNAL_HEAT_SOURCE),
        (HeatingCircuit, DeviceType.HEATING_CIRCUIT),
        (HeatPump, DeviceType.HEAT_PUMP),
        (PassiveCooling, DeviceType.PASSIVE_COOLING),
        (Photovoltaics, DeviceType.PHOTOVOLTAICS),
        (SolarCircuit, DeviceType.SOLAR_CIRCUIT),
        (SwitchValve, DeviceType.SWITCH_VALVE),
        (System, DeviceType.SYSTEM),
    ],
    ids=[device_type.value for device_type in DeviceType],
)
def test_device_type(section_class: type[Section], expected: DeviceType) -> None:
    """Test that every section class has its device type."""
    assert section_class.device_type is expected


@pytest.mark.parametrize(
    ("path", "message_id"),
    [
        ("sParam.heatpump[%s].Compressor.values.setValueScaled", "sParam.heatpump[0].Compressor"),
        ("sParam.outdoorTemp.values.actValue", "sParam.heatpump[%s]"),
    ],
    ids=["missing_device_index", "extra_device_index"],
)
def test_endpoint_message_id_device_index(path: str, message_id: str) -> None:
    """Test that a message id node with another device index than the path is rejected."""
    with pytest.raises(ValueError, match=r"^message id '.*' doesn't match the device index of '.*'$"):
        Endpoint(path=path, value_type=float, message_id=message_id)


def test_endpoint_writable() -> None:
    """Test that a path containing `.param.` is writable and other paths are read-only by default."""
    assert Endpoint(path="sParam.heatpump[%s].param.name", value_type=str).writable
    assert not Endpoint(path="sParam.heatpump[%s].values.COP", value_type=float).writable
    assert Endpoint(path="sParam.hmiRetainData.consumer1PrioritySolar[%s]", value_type=bool, writable=True).writable
