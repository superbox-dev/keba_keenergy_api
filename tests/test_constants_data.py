# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for `test_constants.py`."""

from enum import Enum
from typing import Final

from keba_keenergy_api.constants import BufferTank
from keba_keenergy_api.constants import ExternalHeatSource
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import PassiveCooling
from keba_keenergy_api.constants import Photovoltaics
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import SwitchValve
from keba_keenergy_api.constants import System

SECTIONS: Final[tuple[type[Enum], ...]] = (
    System,
    BufferTank,
    HotWaterTank,
    HeatPump,
    HeatCircuit,
    SolarCircuit,
    ExternalHeatSource,
    SwitchValve,
    PassiveCooling,
    Photovoltaics,
)
