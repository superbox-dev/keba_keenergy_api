# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the data models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from keba_keenergy_api.models import DeviceCounts


def test_device_counts_passive_cooling(counts: DeviceCounts) -> None:
    """Test that there is one passive cooling unit per heat pump."""
    assert counts.passive_cooling == counts.heat_pump
