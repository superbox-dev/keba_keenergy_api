# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the value enums."""

import pytest

from keba_keenergy_api.enums import HeatPumpSubState
from keba_keenergy_api.enums import MessageIdKind
from keba_keenergy_api.enums import SystemOperatingMode


@pytest.mark.parametrize(
    ("value", "expected"),
    [(13, HeatPumpSubState.DRIP), (25, HeatPumpSubState.DRIP), (24, HeatPumpSubState.DEFROST_FAN)],
    ids=["first_value", "second_value", "single_value"],
)
def test_enum_with_more_values(value: int, expected: HeatPumpSubState) -> None:
    """Test that a member with more than one value is found by each of them."""
    assert HeatPumpSubState(value) is expected


def test_enum_invalid_value() -> None:
    """Test that an unknown value raises `ValueError`."""
    with pytest.raises(ValueError, match=r"^99 is not a valid SystemOperatingMode$"):
        SystemOperatingMode(99)


@pytest.mark.parametrize(
    ("message_id", "expected"),
    [(0, MessageIdKind.OK), (10, MessageIdKind.DEACTIVATED), (50, MessageIdKind.ERROR), (-1, MessageIdKind.ERROR)],
    ids=["ok", "deactivated", "error", "negative"],
)
def test_message_id_kind(message_id: int, expected: MessageIdKind) -> None:
    """Test the kind of a raw message id."""
    assert MessageIdKind.from_message_id(message_id) is expected
