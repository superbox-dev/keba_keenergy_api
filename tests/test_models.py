# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the data models."""

from typing import TYPE_CHECKING
from typing import get_type_hints

import pytest

from keba_keenergy_api.models import Alarm
from keba_keenergy_api.models import CurvePoint
from keba_keenergy_api.models import CurveTable
from keba_keenergy_api.models import DeviceCounts
from keba_keenergy_api.models import DeviceInfo
from keba_keenergy_api.models import HmiInfo
from keba_keenergy_api.models import MessageId
from keba_keenergy_api.models import Reading
from keba_keenergy_api.models import SystemInfo
from keba_keenergy_api.sections import Endpoint

if TYPE_CHECKING:
    from typing import Any


def test_device_counts_passive_cooling(counts: DeviceCounts) -> None:
    """Test that there is one passive cooling unit per heat pump."""
    assert counts.passive_cooling == counts.heat_pump


@pytest.mark.parametrize(
    "model",
    [Alarm, CurvePoint, CurveTable, DeviceCounts, DeviceInfo, Endpoint, HmiInfo, MessageId, Reading, SystemInfo],
    ids=[
        "alarm",
        "curve_point",
        "curve_table",
        "device_counts",
        "device_info",
        "endpoint",
        "hmi_info",
        "message_id",
        "reading",
        "system_info",
    ],
)
def test_model_type_hints(model: type[Any]) -> None:
    """Test that the field types of a public model can be resolved at runtime, e.g. by `typing.get_type_hints()`."""
    assert get_type_hints(model)
