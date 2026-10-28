# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Value enums of the KEBA KeEnergy Web HMI."""

from enum import Enum
from enum import StrEnum

from keba_keenergy_api.constants import _DEACTIVATED_MESSAGE_ID
from keba_keenergy_api.constants import _OK_MESSAGE_ID


class _BaseEnum(Enum):
    """Base enum that also matches values inside tuple members, e.g. ``DRIP = (13, 25)``."""

    @classmethod
    def _missing_(cls, value: object) -> _BaseEnum:
        """Return the enum member matching the given value."""
        # Scalar values are already matched by Enum itself, only tuple members are left.
        for member in cls:
            if isinstance(member._value_, tuple) and value in member._value_:
                return member

        msg: str = f"{value!r} is not a valid {cls.__name__}"
        raise ValueError(msg)


class DeviceType(StrEnum):
    """Device types of the control unit, one per section."""

    BUFFER_TANK = "buffer_tank"
    CASCADE = "cascade"
    DHW_TANK = "dhw_tank"
    EXTERNAL_HEAT_SOURCE = "external_heat_source"
    HEATING_CIRCUIT = "heating_circuit"
    HEAT_PUMP = "heat_pump"
    PASSIVE_COOLING = "passive_cooling"
    PHOTOVOLTAICS = "photovoltaics"
    SOLAR_CIRCUIT = "solar_circuit"
    SWITCH_VALVE = "switch_valve"
    SYSTEM = "system"


class MessageIdKind(Enum):
    """Kinds of a message id (``state.msgId``), like ``MsgIdKind`` of the Web HMI.

    ``OK`` (``0``) means the value is valid, ``DEACTIVATED`` (``10``) that the component is not configured and
    ``ERROR`` (any other value) that the component exists but its value is not valid.
    """

    OK = "ok"
    DEACTIVATED = "deactivated"
    ERROR = "error"

    @classmethod
    def from_message_id(cls, message_id: int) -> MessageIdKind:
        """Return the kind of a raw message id.

        Parameters
        ----------
        message_id
            The raw message id, e.g. ``Reading.message_id.value``.

        Returns
        -------
        MessageIdKind
            The kind of the message id.

        Examples
        --------
        >>> MessageIdKind.from_message_id(10)
        <MessageIdKind.DEACTIVATED: 'deactivated'>

        """
        if message_id == _OK_MESSAGE_ID:
            return cls.OK

        if message_id == _DEACTIVATED_MESSAGE_ID:
            return cls.DEACTIVATED

        return cls.ERROR


class SystemOperatingMode(_BaseEnum):
    """Operating modes of the system (Setup, Standby, Summer, AutoHeat, AutoCool, FullAuto)."""

    SETUP = -1
    STANDBY = 0
    SUMMER = 1
    AUTO_HEATING = 2
    AUTO_COOLING = 3
    AUTO = 4


class BufferTankOperatingMode(_BaseEnum):
    """Operating modes of a buffer tank (Off, On, Manual load)."""

    OFF = 0
    ON = 1
    MANUAL_CHARGE = 2


class DHWTankOperatingMode(_BaseEnum):
    """Operating modes of a DHW tank (Off, Auto, On, Manual load)."""

    OFF = 0
    AUTO = 1
    ON = 2
    MANUAL_CHARGE = 3


class ExcessEnergyState(_BaseEnum):
    """States of the excess energy use of a buffer tank, DHW tank or heating circuit (Off, Heat, Cool)."""

    OFF = 0
    HEATING = 1
    COOLING = 2


class HeatPumpType(_BaseEnum):
    """Types of a heat pump by its source (Brine, Water, Air, DX, Air-Brine, Multi source, DX source)."""

    BRINE = 0
    WATER = 1
    AIR = 2
    DX = 3
    AIR_BRINE = 4
    MULTI_SOURCE = 5
    DX_SOURCE = 6


class HeatPumpState(_BaseEnum):
    """States of a heat pump."""

    STANDBY = 0
    PRE_RUN = 1
    AUTOMATIC = 2
    DEFROST = 3
    COOLING = 4
    POST_RUN = 5
    PUMP_DOWN = 6
    SHUTDOWN = 7
    ERROR = 8
    SOURCE_FLUSH = 9


class HeatPumpSubState(_BaseEnum):
    """Substates of a heat pump. Some substates have more than one value."""

    NONE = 0
    OIL_PREHEATING = 1
    PUMP_PRE_RUN = (2, 3)
    RANDOM_DELAY = 4
    PRESSURE_EQUALIZATION = (5, 21, 22)
    DEFROST_PRE_RUN = 6
    DEFROST_MONITORING = 7
    SNOW_DETECTION = 8
    FLUSHING = 9
    DEFROST_INITIALIZATION = 10
    PRE_RUN_HEAT_UP = 11
    DEFROST = 12
    DRIP = (13, 25)
    DEFROST_END = 14
    OPENING = (15, 16)
    COMPRESSOR_POST_RUN = 17
    PUMP_POST_RUN = 18
    LUBRICATION_PULSE = 19
    REDUCED_SPEED = (20, 26)
    COMPRESSOR_DELAY = 23
    DEFROST_FAN = 24
    SWITCHING_HEATING_COOLING = 27
    WAITING_FOR_COMPRESSOR = (28, 33)
    COMPRESSOR_STOP = 29
    BIVALENT_LOCK = 30
    LOCKED = 31
    RETURN_OFF = 32
    MIXER_OPEN = 34
    ZONE_VALVE = 35
    ELECTRIC_DEFROST = 36
    COUNTERFLOW_VALVE = 37


class SuperheatControlState(_BaseEnum):
    """States of the superheat control of a heat pump (Undefined, Init, Reference, Run, Manual mode)."""

    UNDEFINED = 0
    INITIALIZING = 1
    REFERENCING = 2
    RUNNING = 3
    MANUAL = 4


class HeatingCircuitType(_BaseEnum):
    """Types of a heating circuit (Heating, Cooling, Heat/Cool)."""

    HEATING = 0
    COOLING = 1
    HEATING_AND_COOLING = 2
    HEATING_AND_ACTIVE_COOLING = 3


class HeatingCircuitOperatingMode(_BaseEnum):
    """Operating modes of a heating circuit (Off, Auto, Normal, Reduced, Vacation, Party, External)."""

    OFF = 0
    AUTO = 1
    NORMAL = 2
    REDUCED = 3
    VACATION = 4
    PARTY = 5
    EXTERNAL = 8
    ROOM_CONTROL = 9


class HeatingCircuitRequest(_BaseEnum):
    """Heating and cooling request states of a heating circuit, with the reason why the request is off."""

    OFF = 0
    ACTIVE = 1
    RETURN_OFF = 2
    TEMPERATURE_PRIORITY_OFF = 3
    ROOM_OFF = 4
    OUTDOOR_OFF = 5
    FLOW_OFF = 6


class SwitchValvePosition(_BaseEnum):
    """Positions of a switch valve.

    The names are neutral, as the Web HMI texts depend on the format and can differ between controllers
    (e.g. neutral / HW / Pos.2 or neutral / open / closed).
    """

    NEUTRAL = 0
    POSITION_1 = 1
    POSITION_2 = 2


class SolarCircuitOperatingMode(_BaseEnum):
    """Operating modes of a solar circuit (Off, On)."""

    OFF = 0
    ON = 1


class CascadeStrategy(_BaseEnum):
    """Strategies of the cascade to distribute the power to the heat generators (Balanced, Priority)."""

    BALANCED = 0
    PRIORITY = 1


class CascadeState(_BaseEnum):
    """States of a heat generator in the cascade.

    (Standby, Active, Error, Blocked, Forced, Emergency cooling, Not available, DHW)
    """

    STANDBY = 0
    ACTIVE = 1
    ERROR = 2
    LOCKED = 3
    FORCED_ACTIVATION = 4
    EMERGENCY_COOLING = 5
    NOT_AVAILABLE = 6
    DHW_HEATING = 7


class ExternalHeatSourceOperatingMode(_BaseEnum):
    """Operating modes of an external heat source (Off, On, Flue)."""

    OFF = 0
    ON = 1
    FLUE = 2


class ElectricalEnergyMeterType(_BaseEnum):
    """Types of the electric energy meter of a heat pump (not existing, S0 meter, via inverter)."""

    NONE = 0
    S0 = 2
    INVERTER = 5


class HeatMeterType(_BaseEnum):
    """Types of the heat meter of a heat pump (not existing, S0 meter, vortex)."""

    NONE = 0
    S0 = 2
    VORTEX = 3
