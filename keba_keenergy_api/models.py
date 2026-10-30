# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Data models of the KEBA KeEnergy API."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal
from typing import NamedTuple
from typing import NotRequired
from typing import TypedDict

from keba_keenergy_api.enums import AlarmPriority
from keba_keenergy_api.enums import MessageIdKind
from keba_keenergy_api.sections import Section

type Value = bool | Enum | float | int | str
type WriteValue = bool | Enum | float | int | str
type Readings = dict[Section, list[Reading]]
# Endpoints whose limits are read: all, none, only the read-only or only the writable ones.
type Limits = Literal["all", "none", "read_only", "writable"]


@dataclass(frozen=True, kw_only=True)
class Reading:
    """A value read from the Web HMI.

    Attributes
    ----------
    value
        The value converted to the type of the endpoint: ``bool``, ``float``, ``int``, ``str`` or an enum member.
    device_number
        Number of the device, starting at 1.
    consumer_number
        Number of the consumer of the device, starting at 1, only for endpoints with more than one value per device
        (the consumers of a solar circuit).
    lower_limit
        Lower limit of the value in the ``raw_unit``, as reported by the Web HMI. ``None`` if there is none or it was
        not read (``read(..., limits=...)``). Multiply it by ``display_factor`` for the display unit.
    upper_limit
        Upper limit of the value in the ``raw_unit``, as reported by the Web HMI. ``None`` if there is none or it was
        not read (``read(..., limits=...)``). Multiply it by ``display_factor`` for the display unit.
    message_id
        Message id of the component, only if it was read with ``read(..., message_ids=True)`` and the endpoint has
        one.
    raw_value
        The value exactly as the Web HMI delivers it, e.g. ``"25"`` for ``HeatPumpSubState.DRIP``, which has the
        values ``13`` and ``25``, or ``"0.54009795"``. ``value`` is its conversion to the type of the endpoint.
    raw_unit
        Unit of ``value`` and ``raw_value`` as the Web HMI delivers it, e.g. ``°C`` or ``J``, ``None`` for values
        without a unit or ratios (``0..1``).
    display_unit
        Unit the Web HMI shows, e.g. ``kW`` for a power delivered in ``W``, ``None`` for values without a unit.
    display_factor
        Factor from ``value`` to the display unit of the Web HMI, e.g. ``0.001`` for ``W`` to ``kW`` or ``100.0`` for a
        ratio (``0..1``) shown in ``%``. ``1.0`` if the value is shown unchanged. The ``value`` itself is never
        converted.
    display_precision
        Number of decimal places the Web HMI shows for ``value * display_factor``, ``None`` for values without a
        number format. The value itself is never rounded.

    """

    value: Value
    device_number: int
    consumer_number: int | None = None
    lower_limit: float | None = None
    upper_limit: float | None = None
    message_id: MessageId | None = None
    raw_value: str
    raw_unit: str | None = None
    display_unit: str | None = None
    display_factor: float = 1.0
    display_precision: int | None = None


@dataclass(frozen=True, kw_only=True)
class MessageId:
    """A message id (``state.msgId``) of a component.

    Attributes
    ----------
    value
        The raw message id, its meaning per component is unknown.
    kind
        The kind of the message id, like the Web HMI handles it.

    """

    value: int
    kind: MessageIdKind


@dataclass(frozen=True, kw_only=True)
class DeviceCounts:
    """Number of installed devices per device type, as configured in the control unit."""

    buffer_tank: int
    dhw_tank: int
    external_heat_source: int
    heat_pump: int
    heating_circuit: int
    solar_circuit: int
    switch_valve: int

    @property
    def passive_cooling(self) -> int:
        """Return the number of passive cooling units (one per heat pump)."""
        return self.heat_pump


class CurvePoint(NamedTuple):
    """Point of a heating or cooling curve."""

    outdoor: float
    flow: float


@dataclass(frozen=True, kw_only=True)
class CurveTable:
    """A curve table (line table) with the points of a heating or cooling curve.

    Attributes
    ----------
    name
        Name of the curve, e.g. ``HC1``.
    points
        Points of the curve, ordered by the outdoor temperature as in the Web HMI.

    """

    name: str
    points: tuple[CurvePoint, ...]


@dataclass(frozen=True, kw_only=True)
class Alarm:
    """A pending alarm of the control unit.

    Attributes
    ----------
    number
        Number of the alarm (``alarmNr``), e.g. ``700`` for a sensor break.
    component
        Number of the component that raised the alarm (``compNr``).
    instance
        Instance of the component (``instanceNr``), e.g. the number of the differential control.
    priority
        Priority of the alarm.
    acknowledgeable
        Whether the alarm must be acknowledged on the control unit (``quittable``).
    short_text
        Short text of the alarm in the requested language.
    long_text
        Long text of the alarm in the requested language, with the names configured on the control unit.
    timestamp
        Time the alarm was raised, as local time of the control unit without a timezone (see
        ``get_timezone()``).

    """

    number: int
    component: int
    instance: int
    priority: AlarmPriority
    acknowledgeable: bool
    short_text: str
    long_text: str
    timestamp: datetime


class SystemInfo(TypedDict):
    """Installed system software, e.g. ``{"name": "KeEnergy.MTec", "version": "2.2.2"}``."""

    name: str
    version: NotRequired[str]


class HmiInfo(TypedDict):
    """Installed Web HMI software, e.g. ``{"name": "KeEnergy.WebHmi_2.2.0.0"}``."""

    name: str


class DeviceInfo(TypedDict):
    """Information about the control unit."""

    name: str
    orderNo: int
    revNo: int
    serNo: int
    variantNo: int
