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
from keba_keenergy_api.sections import EndpointDefinition
from keba_keenergy_api.sections import ExternalHeatSource
from keba_keenergy_api.sections import HeatingCircuit
from keba_keenergy_api.sections import HeatPump
from keba_keenergy_api.sections import PassiveCooling
from keba_keenergy_api.sections import Photovoltaics
from keba_keenergy_api.sections import SolarCircuit
from keba_keenergy_api.sections import SwitchValve
from keba_keenergy_api.sections import System

if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion


def test_sections(snapshot: SnapshotAssertion) -> None:
    """Test the variables, types, units, display, writable state, message ids and quantities of all endpoints."""
    endpoints: dict[str, dict[str, Any]] = {
        str(endpoint): {
            "variable": endpoint.value.variable,
            "value_type": endpoint.value.value_type.__name__,
            "raw_unit": endpoint.value.raw_unit,
            "display_unit": endpoint.value.display_unit,
            "display_factor": endpoint.value.display_factor,
            "display_precision": endpoint.value.display_precision,
            "writable": endpoint.value.writable,
            "message_id": endpoint.value.message_id_variable,
            "quantity": endpoint.value.quantity,
        }
        for section_class in get_args(Endpoint.__value__)
        for endpoint in section_class
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
def test_device_type(section_class: type[Endpoint], expected: DeviceType) -> None:
    """Test that every endpoint class has its device type."""
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
        EndpointDefinition(path=path, value_type=float, message_id=message_id)


def test_endpoint_writable() -> None:
    """Test that a path containing `.param.` is writable and other paths are read-only by default."""
    assert EndpointDefinition(path="sParam.heatpump[%s].param.name", value_type=str).writable
    assert not EndpointDefinition(path="sParam.heatpump[%s].values.COP", value_type=float).writable
    assert EndpointDefinition(
        path="sParam.hmiRetainData.consumer1PrioritySolar[%s]", value_type=bool, writable=True
    ).writable


@pytest.mark.parametrize(
    ("endpoint", "expected"),
    [
        (HeatPump.CIRCULATION_PUMP_SPEED, (None, "%", 100.0, 0)),
        (HeatPump.COMPRESSOR_ESTIMATED_ELECTRICAL_POWER, ("W", "kW", 0.001, 2)),
        (HeatPump.COP, (None, None, 1.0, 2)),
        (System.OUTDOOR_TEMPERATURE, ("°C", "°C", 1.0, 1)),
        (System.OPERATING_MODE, (None, None, 1.0, None)),
    ],
    ids=["ratio_as_percent", "watt_as_kilowatt", "without_unit", "unit_unchanged", "enum"],
)
def test_endpoint_display(endpoint: Endpoint, expected: tuple[str | None, str | None, float, int | None]) -> None:
    """Test the display unit, factor and precision of the Web HMI, the display unit defaults to the unit."""
    assert (
        endpoint.value.raw_unit,
        endpoint.value.display_unit,
        endpoint.value.display_factor,
        endpoint.value.display_precision,
    ) == expected
