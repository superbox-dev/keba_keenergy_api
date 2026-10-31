# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Endpoints of the KEBA KeEnergy Web HMI, one enum per device type."""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from keba_keenergy_api.constants import _BAR
from keba_keenergy_api.constants import _CELSIUS
from keba_keenergy_api.constants import _CUBIC_METER_PER_SECOND
from keba_keenergy_api.constants import _CUBIC_METER_PER_SECOND_TO_LITER_PER_HOUR
from keba_keenergy_api.constants import _HOUR
from keba_keenergy_api.constants import _JOULE
from keba_keenergy_api.constants import _JOULE_TO_KILOWATT_HOUR
from keba_keenergy_api.constants import _KELVIN
from keba_keenergy_api.constants import _KILOBYTE
from keba_keenergy_api.constants import _KILOGRAM_PER_HOUR
from keba_keenergy_api.constants import _KILOGRAM_PER_SECOND
from keba_keenergy_api.constants import _KILOGRAM_PER_SECOND_TO_KILOGRAM_PER_HOUR
from keba_keenergy_api.constants import _KILOWATT
from keba_keenergy_api.constants import _KILOWATT_HOUR
from keba_keenergy_api.constants import _LITER_PER_HOUR
from keba_keenergy_api.constants import _MESSAGE_ID_SUFFIX
from keba_keenergy_api.constants import _MINUTE
from keba_keenergy_api.constants import _PAYLOAD_PREFIX
from keba_keenergy_api.constants import _PER_MILLE
from keba_keenergy_api.constants import _PER_MILLE_TO_PERCENT
from keba_keenergy_api.constants import _PERCENT
from keba_keenergy_api.constants import _RATIO_TO_PERCENT
from keba_keenergy_api.constants import _SECOND
from keba_keenergy_api.constants import _SECOND_TO_HOUR
from keba_keenergy_api.constants import _SECOND_TO_MINUTE
from keba_keenergy_api.constants import _WATT
from keba_keenergy_api.constants import _WATT_TO_KILOWATT
from keba_keenergy_api.enums import BufferTankOperatingMode
from keba_keenergy_api.enums import CascadeState
from keba_keenergy_api.enums import CascadeStrategy
from keba_keenergy_api.enums import DeviceType
from keba_keenergy_api.enums import DHWTankOperatingMode
from keba_keenergy_api.enums import ElectricalEnergyMeterType
from keba_keenergy_api.enums import ExcessEnergyState
from keba_keenergy_api.enums import ExternalHeatSourceOperatingMode
from keba_keenergy_api.enums import HeatingCircuitOperatingMode
from keba_keenergy_api.enums import HeatingCircuitRequest
from keba_keenergy_api.enums import HeatingCircuitType
from keba_keenergy_api.enums import HeatMeterType
from keba_keenergy_api.enums import HeatPumpState
from keba_keenergy_api.enums import HeatPumpSubState
from keba_keenergy_api.enums import HeatPumpType
from keba_keenergy_api.enums import SolarCircuitOperatingMode
from keba_keenergy_api.enums import SuperheatControlState
from keba_keenergy_api.enums import SwitchValvePosition
from keba_keenergy_api.enums import SystemOperatingMode

type EndpointType = type[bool | Enum | float | int | str]


@dataclass(frozen=True, kw_only=True)
class EndpointDefinition:
    """Definition of a Web HMI variable.

    Attributes
    ----------
    path
        Variable path relative to ``APPL.CtrlAppl``, ``%s`` is replaced by the zero-based device index.
    value_type
        Type of the value: ``bool``, ``float``, ``int``, ``str`` or an enum.
    raw_unit
        Unit of the value as the Web HMI delivers it, ``None`` for values without a unit or ratios (``0..1``).
    display_unit
        Unit the Web HMI shows (``unitId``), ``raw_unit`` if the raw value is shown unchanged.
    display_factor
        Factor from the raw value to the display unit (display = raw * multiplier / divisor of the ``unitId``), e.g.
        ``100.0`` for a ratio (``0..1``) shown in ``%``. ``1.0`` if the raw value is shown unchanged.
    display_precision
        Number of decimal places the Web HMI shows (``postComma`` of the ``formatId`` of the variable) for the value
        converted with ``display_factor``. ``None`` for values without a number format (``bool``, enums, ``str``)
        and numbers the Web HMI delivers without a ``formatId``.
    writable
        Whether the variable can be written. Paths containing ``.param.`` are always writable.
    message_id
        Path of the component node that has a message id (``state.msgId``) for this value, ``None`` if there is none.
    quantity
        Number of values per device, e.g. two consumers per solar circuit.

    """

    path: str
    value_type: EndpointType
    raw_unit: str | None = None
    display_unit: str | None = None
    display_factor: float = 1.0
    display_precision: int | None = None
    writable: bool = False
    message_id: str | None = None
    quantity: int = 1

    def __post_init__(self) -> None:
        """Derive the writable state and display unit from the path and validate the message id node."""
        if self.display_unit is None:
            # The dataclass is frozen, so the derived value is set like in the generated __init__.
            object.__setattr__(self, "display_unit", self.raw_unit)

        if ".param." in self.path:
            # The dataclass is frozen, so the derived value is set like in the generated __init__.
            object.__setattr__(self, "writable", True)

        if self.message_id is not None and ("%s" in self.message_id) != self.has_device_index:
            msg: str = f"message id {self.message_id!r} doesn't match the device index of {self.path!r}"
            raise ValueError(msg)

    @property
    def has_device_index(self) -> bool:
        """Return whether the variable has one value per device (``%s`` in the path)."""
        return "%s" in self.path

    @property
    def variable(self) -> str:
        """Return the full variable name template, e.g. ``APPL.CtrlAppl.sParam.heatpump[%s].values.COP``."""
        return f"{_PAYLOAD_PREFIX}.{self.path}"

    @property
    def message_id_variable(self) -> str | None:
        """Return the full variable name template of the message id, or ``None`` if the endpoint has none."""
        if self.message_id is None:
            return None

        return f"{_PAYLOAD_PREFIX}.{self.message_id}.{_MESSAGE_ID_SUFFIX}"


class _DeviceTypeEnum(Enum):
    """Base of the enums of the endpoints of a device type, the device type is given as class keyword."""

    _value_: EndpointDefinition
    device_type: ClassVar[DeviceType]

    def __init_subclass__(cls, *, device_type: DeviceType, **kwargs: object) -> None:
        """Set the device type of the enum."""
        super().__init_subclass__(**kwargs)
        cls.device_type = device_type


class System(_DeviceTypeEnum, device_type=DeviceType.SYSTEM):
    """Endpoints of the system."""

    HAS_PHOTOVOLTAICS = EndpointDefinition(
        path="sParam.options.hasPhotovoltaics",
        value_type=bool,
    )
    HAS_OUTDOOR_TEMPERATURE_SENSOR = EndpointDefinition(
        path="sParam.options.hasOutdoorTemp",
        value_type=bool,
    )
    OPERATING_MODE = EndpointDefinition(
        path="sParam.param.operatingMode",
        value_type=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE = EndpointDefinition(
        path="sParam.outdoorTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.outdoorTemp",
    )
    CPU_USAGE = EndpointDefinition(
        path="sProcData.globalCpuTimePercent",
        value_type=float,
        raw_unit=_PER_MILLE,
        display_unit=_PERCENT,
        display_factor=_PER_MILLE_TO_PERCENT,
        display_precision=1,
    )
    WEBVIEW_CPU_USAGE = EndpointDefinition(
        path="sProcData.processStatus[0].cpuTimePercent",
        value_type=float,
        raw_unit=_PER_MILLE,
        display_unit=_PERCENT,
        display_factor=_PER_MILLE_TO_PERCENT,
        display_precision=1,
    )
    WEBSERVER_CPU_USAGE = EndpointDefinition(
        path="sProcData.processStatus[1].cpuTimePercent",
        value_type=float,
        raw_unit=_PER_MILLE,
        display_unit=_PERCENT,
        display_factor=_PER_MILLE_TO_PERCENT,
        display_precision=1,
    )
    CONTROL_CPU_USAGE = EndpointDefinition(
        path="sProcData.processStatus[2].cpuTimePercent",
        value_type=float,
        raw_unit=_PER_MILLE,
        display_unit=_PERCENT,
        display_factor=_PER_MILLE_TO_PERCENT,
        display_precision=1,
    )
    TEMPORARY_MEMORY_USAGE = EndpointDefinition(
        path="sProcData.RAMstatus.tmpfs",
        value_type=int,
        raw_unit=_KILOBYTE,
        display_precision=0,
    )
    FREE_RAM = EndpointDefinition(
        path="sProcData.totFreeRAM",
        value_type=int,
        raw_unit=_KILOBYTE,
        display_precision=0,
    )
    FLASH_MAX_ERASE_COUNTER = EndpointDefinition(
        path="sParam.values.UBIMaxEraseCounter",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_BUFFER_TANKS = EndpointDefinition(
        path="sParam.options.systemNumberOfBuffers",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_DHW_TANKS = EndpointDefinition(
        path="sParam.options.systemNumberOfHotWaterTanks",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_HEAT_PUMPS = EndpointDefinition(
        path="sParam.options.systemNumberOfHeatPumps",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_HEATING_CIRCUITS = EndpointDefinition(
        path="sParam.options.systemNumberOfHeatingCircuits",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_SOLAR_CIRCUITS = EndpointDefinition(
        path="sParam.options.systemNumberOfSolarCircuits",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_EXTERNAL_HEAT_SOURCES = EndpointDefinition(
        path="sParam.options.systemNumberOfExtHeatSources",
        value_type=int,
        display_precision=0,
    )
    _NUMBER_OF_SWITCH_VALVES = EndpointDefinition(
        path="sParam.options.systemNumberOfSwitchValves",
        value_type=int,
        display_precision=0,
    )


class BufferTank(_DeviceTypeEnum, device_type=DeviceType.BUFFER_TANK):
    """Endpoints of a buffer tank."""

    NAME = EndpointDefinition(
        path="sParam.bufferTank[%s].param.name",
        value_type=str,
    )
    OPERATING_MODE = EndpointDefinition(
        path="sParam.bufferTank[%s].param.operatingMode",
        value_type=BufferTankOperatingMode,
    )
    BACKUP_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].param.backupTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].values.setTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    HEATING_REQUEST = EndpointDefinition(
        path="sParam.bufferTank[%s].values.heatRequestTop",
        value_type=bool,
    )
    COOLING_REQUEST = EndpointDefinition(
        path="sParam.bufferTank[%s].values.coolRequestBot",
        value_type=bool,
    )
    TOP_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].topTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.bufferTank[%s].topTemp",
    )
    BOTTOM_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].midTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.bufferTank[%s].midTemp",
    )
    FLOW_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].flowTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.bufferTank[%s].flowTemp",
    )
    RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].refluxTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.bufferTank[%s].refluxTemp",
    )
    USE_EXCESS_ENERGY = EndpointDefinition(
        path="sParam.bufferTank[%s].param.useExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.bufferTank[%s].param.excessEnergyTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = EndpointDefinition(
        path="sParam.bufferTank[%s].param.excessEnergyTemp.hyst",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    EXCESS_ENERGY_OUTDOOR_TEMPERATURE_LIMIT = EndpointDefinition(
        path="sParam.bufferTank[%s].param.thresholdOutTempExcessEnergy.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_STATE = EndpointDefinition(
        path="sParam.bufferTank[%s].values.useExcessEnergy",
        value_type=ExcessEnergyState,
    )


class DHWTank(_DeviceTypeEnum, device_type=DeviceType.DHW_TANK):
    """Endpoints of a DHW tank."""

    NAME = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.name",
        value_type=str,
    )
    HAS_FRESH_WATER_MODULE = EndpointDefinition(
        path="sParam.options.hotWaterTank[%s].hasFreshWaterModule",
        value_type=bool,
    )
    OPERATING_MODE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.operatingMode",
        value_type=DHWTankOperatingMode,
    )
    TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.normalSetTempMax.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    BACKUP_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.reducedSetTempMax.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    HEATING_REQUEST = EndpointDefinition(
        path="sParam.hotWaterTank[%s].values.heatRequestTop",
        value_type=bool,
    )
    CIRCULATION_PUMP_ACTIVE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].circPump.pump.values.setValueB",
        value_type=bool,
        message_id="sParam.hotWaterTank[%s].circPump.pump",
    )
    TOP_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].topTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.hotWaterTank[%s].topTemp",
    )
    BOTTOM_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].botTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.hotWaterTank[%s].botTemp",
    )
    CIRCULATION_RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].circTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.hotWaterTank[%s].circTemp",
    )
    FRESH_WATER_FLOW_ACTIVE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].FreshWater.freshWaterFlow.values.actValue",
        value_type=bool,
        message_id="sParam.hotWaterTank[%s].FreshWater.freshWaterFlow",
    )
    FRESH_WATER_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].FreshWater.freshWaterTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=2,
        message_id="sParam.hotWaterTank[%s].FreshWater.freshWaterTemp",
    )
    USE_EXCESS_ENERGY = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.useExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.excessEnergyTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = EndpointDefinition(
        path="sParam.hotWaterTank[%s].param.excessEnergyTemp.hyst",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    EXCESS_ENERGY_STATE = EndpointDefinition(
        path="sParam.hotWaterTank[%s].values.useExcessEnergy",
        value_type=ExcessEnergyState,
    )


class HeatPump(_DeviceTypeEnum, device_type=DeviceType.HEAT_PUMP):
    """Endpoints of a heat pump."""

    NAME = EndpointDefinition(
        path="sParam.heatpump[%s].param.name",
        value_type=str,
    )
    MODEL = EndpointDefinition(
        path="sParam.heatpump[%s].heatPumpTypeName",
        value_type=str,
    )
    TYPE = EndpointDefinition(
        path="sParam.options.heatpump[%s].heatpumpType",
        value_type=HeatPumpType,
    )
    HAS_ACTIVE_COOLING = EndpointDefinition(
        path="sParam.options.heatpump[%s].hasActiveCooling",
        value_type=bool,
    )
    HAS_PASSIVE_COOLING = EndpointDefinition(
        path="sParam.options.heatpump[%s].hasPassiveCooling",
        value_type=bool,
    )
    HAS_REVERSE_CYCLE_DEFROST = EndpointDefinition(
        path="sParam.options.heatpump[%s].defrostingMode",
        value_type=bool,
    )
    HEAT_METER_TYPE = EndpointDefinition(
        path="sParam.options.heatpump[%s].HeatMeter.type",
        value_type=HeatMeterType,
    )
    ELECTRICAL_ENERGY_METER_TYPE = EndpointDefinition(
        path="sParam.options.heatpump[%s].ElectricEnergyMeter.type",
        value_type=ElectricalEnergyMeterType,
    )
    USE_COMPRESSOR_NIGHT_POWER_LIMIT = EndpointDefinition(
        path="sParam.heatpump[%s].HeatPumpPowerCtrl.param.useDayNightSpeed",
        value_type=bool,
    )
    COMPRESSOR_NIGHT_POWER_LIMIT = EndpointDefinition(
        path="sParam.heatpump[%s].HeatPumpPowerCtrl.param.maxPowerScaledNight",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    STATE = EndpointDefinition(
        path="sParam.heatpump[%s].values.heatpumpState",
        value_type=HeatPumpState,
    )
    SUB_STATE = EndpointDefinition(
        path="sParam.heatpump[%s].values.heatpumpSubState",
        value_type=HeatPumpSubState,
    )
    STATE_DURATION = EndpointDefinition(
        path="sParam.heatpump[%s].values.stateTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_MINUTE,
        display_factor=_SECOND_TO_MINUTE,
        display_precision=1,
    )
    STATE_REMAINING_TIME = EndpointDefinition(
        path="sParam.heatpump[%s].values.remainTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_MINUTE,
        display_factor=_SECOND_TO_MINUTE,
        display_precision=1,
    )
    REQUEST = EndpointDefinition(
        path="sParam.heatpump[%s].values.request",
        value_type=bool,
    )
    TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].values.setTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    COOLING_ACTIVE = EndpointDefinition(
        path="sParam.heatpump[%s].OpModeCooling.values.setValueB",
        value_type=bool,
        message_id="sParam.heatpump[%s].OpModeCooling",
    )
    ELECTRIC_DEFROST_ACTIVE = EndpointDefinition(
        path="sParam.heatpump[%s].ElectricDefrost.values.setValueB",
        value_type=bool,
        message_id="sParam.heatpump[%s].ElectricDefrost",
    )
    OIL_HEATER_ACTIVE = EndpointDefinition(
        path="sParam.heatpump[%s].OilHeater.values.setValueB",
        value_type=bool,
        message_id="sParam.heatpump[%s].OilHeater",
    )
    CONDENSATE_HEATER_ACTIVE = EndpointDefinition(
        path="sParam.heatpump[%s].CondensateHeater.values.setValueB",
        value_type=bool,
        message_id="sParam.heatpump[%s].CondensateHeater",
    )
    FLOW_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempHeatFlow.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempHeatFlow",
    )
    RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempHeatReflux.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempHeatReflux",
    )
    CIRCULATION_PUMP_SPEED = EndpointDefinition(
        path="sParam.heatpump[%s].CircPump.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.heatpump[%s].CircPump",
    )
    SOURCE_INLET_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempSourceIn.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempSourceIn",
    )
    SOURCE_OUTLET_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempSourceOut.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempSourceOut",
    )
    SOURCE_VOLUME_FLOW = EndpointDefinition(
        path="sParam.heatpump[%s].SourceFlowMeter.values.actValue",
        value_type=float,
        raw_unit=_CUBIC_METER_PER_SECOND,
        display_unit=_LITER_PER_HOUR,
        display_factor=_CUBIC_METER_PER_SECOND_TO_LITER_PER_HOUR,
        display_precision=0,
        message_id="sParam.heatpump[%s].SourceFlowMeter",
    )
    SOURCE_PRESSURE = EndpointDefinition(
        path="sParam.heatpump[%s].SourcePressure.values.actValue",
        value_type=float,
        raw_unit=_BAR,
        display_precision=2,
        message_id="sParam.heatpump[%s].SourcePressure",
    )
    SOURCE_ACTUATOR_SPEED = EndpointDefinition(
        path="sParam.heatpump[%s].Source.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.heatpump[%s].Source",
    )
    OUTDOOR_UNIT_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempSourceUnit.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempSourceUnit",
    )
    EVAPORATION_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.tempVap",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    LOW_PRESSURE = EndpointDefinition(
        path="sParam.heatpump[%s].LowPressure.values.actValue",
        value_type=float,
        raw_unit=_BAR,
        display_precision=2,
        message_id="sParam.heatpump[%s].LowPressure",
    )
    TARGET_SUCTION_SUPERHEAT = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.setOH",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    SUCTION_SUPERHEAT = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.actOH",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    SUPERHEAT_CONTROL_STATE = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.state",
        value_type=SuperheatControlState,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    MOP_ACTIVE = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.MOPactive",
        value_type=bool,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    COMPRESSOR_INLET_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempCompressorIn.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempCompressorIn",
    )
    COMPRESSOR_SPEED = EndpointDefinition(
        path="sParam.heatpump[%s].Compressor.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.heatpump[%s].Compressor",
    )
    COMPRESSOR_ESTIMATED_ELECTRICAL_POWER = EndpointDefinition(
        path="sParam.heatpump[%s].CompPowerEstim.values.electricPower",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].CompPowerEstim",
    )
    COMPRESSOR_ESTIMATED_REFRIGERATING_CAPACITY = EndpointDefinition(
        path="sParam.heatpump[%s].CompPowerEstim.values.coolingCapacity",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].CompPowerEstim",
    )
    OIL_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempOil.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempOil",
    )
    COMPRESSOR_OUTLET_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempCompressorOut.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempCompressorOut",
    )
    HIGH_PRESSURE = EndpointDefinition(
        path="sParam.heatpump[%s].HighPressure.values.actValue",
        value_type=float,
        raw_unit=_BAR,
        display_precision=2,
        message_id="sParam.heatpump[%s].HighPressure",
    )
    CONDENSATION_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.tempCond",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    CONDENSER_OUTLET_TEMPERATURE = EndpointDefinition(
        path="sParam.heatpump[%s].TempCondenserOut.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatpump[%s].TempCondenserOut",
    )
    EXPANSION_VALVE_POSITION = EndpointDefinition(
        path="sParam.heatpump[%s].OverHeatCtrl.values.stepperPos",
        value_type=int,
        display_precision=0,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    EXCESS_ENERGY_ACTIVE = EndpointDefinition(
        path="sParam.heatpump[%s].values.consumingExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_OPERATING_TIME = EndpointDefinition(
        path="sParam.heatpump[%s].operationalDataExcessEnergy.operationalTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_MAX_RUNTIME = EndpointDefinition(
        path="sParam.heatpump[%s].operationalDataExcessEnergy.maxRunTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    EXCESS_ENERGY_ACTIVATION_COUNTER = EndpointDefinition(
        path="sParam.heatpump[%s].operationalDataExcessEnergy.activationCounter",
        value_type=int,
        display_precision=0,
    )
    HEATING_METER_THERMAL_POWER = EndpointDefinition(
        path="sParam.heatpump[%s].HeatMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].HeatMeter",
    )
    HEATING_METER_ACCUMULATED_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].HeatMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.heatpump[%s].HeatMeter",
    )
    HEATING_METER_DAILY_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].HeatMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].HeatMeter",
    )
    HEATING_METER_MASS_FLOW = EndpointDefinition(
        path="sParam.heatpump[%s].HeatMeter.values.massFlow",
        value_type=float,
        raw_unit=_KILOGRAM_PER_SECOND,
        display_unit=_KILOGRAM_PER_HOUR,
        display_factor=_KILOGRAM_PER_SECOND_TO_KILOGRAM_PER_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].HeatMeter",
    )
    DHW_METER_THERMAL_POWER = EndpointDefinition(
        path="sParam.heatpump[%s].HotWaterMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].HotWaterMeter",
    )
    DHW_METER_ACCUMULATED_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].HotWaterMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.heatpump[%s].HotWaterMeter",
    )
    DHW_METER_DAILY_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].HotWaterMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].HotWaterMeter",
    )
    DHW_METER_MASS_FLOW = EndpointDefinition(
        path="sParam.heatpump[%s].HotWaterMeter.values.massFlow",
        value_type=float,
        raw_unit=_KILOGRAM_PER_SECOND,
        display_unit=_KILOGRAM_PER_HOUR,
        display_factor=_KILOGRAM_PER_SECOND_TO_KILOGRAM_PER_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].HotWaterMeter",
    )
    COOLING_METER_THERMAL_POWER = EndpointDefinition(
        path="sParam.heatpump[%s].CoolMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].CoolMeter",
    )
    COOLING_METER_ACCUMULATED_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].CoolMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.heatpump[%s].CoolMeter",
    )
    COOLING_METER_DAILY_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].CoolMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].CoolMeter",
    )
    COOLING_METER_MASS_FLOW = EndpointDefinition(
        path="sParam.heatpump[%s].CoolMeter.values.massFlow",
        value_type=float,
        raw_unit=_KILOGRAM_PER_SECOND,
        display_unit=_KILOGRAM_PER_HOUR,
        display_factor=_KILOGRAM_PER_SECOND_TO_KILOGRAM_PER_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].CoolMeter",
    )
    SOURCE_METER_THERMAL_POWER = EndpointDefinition(
        path="sParam.heatpump[%s].SourceMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].SourceMeter",
    )
    SOURCE_METER_ACCUMULATED_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].SourceMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.heatpump[%s].SourceMeter",
    )
    SOURCE_METER_DAILY_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].SourceMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].SourceMeter",
    )
    SOURCE_METER_MASS_FLOW = EndpointDefinition(
        path="sParam.heatpump[%s].SourceMeter.values.massFlow",
        value_type=float,
        raw_unit=_KILOGRAM_PER_SECOND,
        display_unit=_KILOGRAM_PER_HOUR,
        display_factor=_KILOGRAM_PER_SECOND_TO_KILOGRAM_PER_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].SourceMeter",
    )
    METER_ELECTRICAL_POWER = EndpointDefinition(
        path="sParam.heatpump[%s].ElectricEnergyMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.heatpump[%s].ElectricEnergyMeter",
    )
    METER_ACCUMULATED_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].ElectricEnergyMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.heatpump[%s].ElectricEnergyMeter",
    )
    METER_DAILY_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sParam.heatpump[%s].ElectricEnergyMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.heatpump[%s].ElectricEnergyMeter",
    )
    COP = EndpointDefinition(
        path="sParam.heatpump[%s].values.COP",
        value_type=float,
        display_precision=2,
    )
    HEATING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.heating.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    HEATING_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.heating.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    HEATING_SPF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatioHeat",
        value_type=float,
    )
    HEATING_PF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].OverallEERHeat",
        value_type=float,
        display_precision=2,
    )
    HEATING_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.heating.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    COOLING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.cooling.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    COOLING_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.cooling.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    COOLING_SPF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatioCool",
        value_type=float,
        display_precision=2,
    )
    COOLING_PF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].OverallEERCool",
        value_type=float,
        display_precision=2,
    )
    COOLING_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.cooling.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    DHW_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DHW_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DHW_SPF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatioDomHotWater",
        value_type=float,
    )
    DHW_PF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].OverallEERDomHotWater",
        value_type=float,
        display_precision=2,
    )
    DHW_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    DEFROST_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.data.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DEFROST_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.data.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DEFROST_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.data.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    DEFROST_CYCLES = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.cycles",
        value_type=int,
        display_precision=0,
    )
    FAILED_DEFROST_CYCLES = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.failedCycles",
        value_type=int,
        display_precision=0,
    )
    TOTAL_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    TOTAL_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    TOTAL_SPF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatio",
        value_type=float,
        display_precision=2,
    )
    TOTAL_PF = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].OverallEER",
        value_type=float,
        display_precision=2,
    )
    TOTAL_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    # The Web HMI has no text and unit for the thermal excess energy per mode, the unit is the one of the total
    # and of all other energy values of the same mode (`kWhwithoutConv`, raw kWh).
    EXCESS_ENERGY_HEATING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.heating.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_HEATING_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.heating.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_COOLING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.cooling.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_COOLING_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.cooling.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_DHW_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_DHW_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_DEFROST_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.data.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_DEFROST_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.defrost.data.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.heatpump[%s].consumption.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    OPERATING_TIME = EndpointDefinition(
        path="sParam.heatpump[%s].operationalData.operationalTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=0,
    )
    MAX_RUNTIME = EndpointDefinition(
        path="sParam.heatpump[%s].operationalData.maxRunTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    ACTIVATION_COUNTER = EndpointDefinition(
        path="sParam.heatpump[%s].operationalData.activationCounter",
        value_type=int,
        display_precision=0,
    )
    COMPRESSOR_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailureCompressor.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureCompressor",
    )
    SOURCE_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailureSource.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureSource",
    )
    SOURCE_ACTUATOR_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailureActuatorSource.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureActuatorSource",
    )
    THREE_PHASE_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailureThreePhase.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureThreePhase",
    )
    SOURCE_PRESSURE_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailureSrcPressure.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureSrcPressure",
    )
    VFD_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailureVFD.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureVFD",
    )
    HIGH_PRESSURE_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailurePressureHigh.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailurePressureHigh",
    )
    LOW_PRESSURE_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].FailurePressureLow.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailurePressureLow",
    )
    PHASE_MONITOR_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].PhaseMonitor.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].PhaseMonitor",
    )
    GAS_LEAK_FAILURE = EndpointDefinition(
        path="sParam.heatpump[%s].GasLeakSensor.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].GasLeakSensor",
    )

    CASCADE_STATE = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].values.state",
        value_type=CascadeState,
    )
    CASCADE_POWER_LEVEL = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].values.actPowerScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    CASCADE_PRIORITY = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.priority",
        value_type=int,
        display_precision=0,
    )
    USE_CASCADE_MODE_PRIORITIES = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.useModePriorities",
        value_type=bool,
    )
    CASCADE_COOLING_PRIORITY = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.priorityCool",
        value_type=int,
        display_precision=0,
    )
    CASCADE_DHW_PRIORITY = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.priorityDHW",
        value_type=int,
        display_precision=0,
    )
    USE_CASCADE_DHW_HEATING = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.domesticHWheatup",
        value_type=bool,
    )
    CASCADE_LOCKED = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.isLocked",
        value_type=bool,
    )
    CASCADE_FORCED_ACTIVATION = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.isForced",
        value_type=bool,
    )
    CASCADE_STARTUP_TIME = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.startupTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_precision=0,
    )
    CASCADE_POST_RUN_TIME = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.cooldownTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_precision=0,
    )
    CASCADE_SOURCE_FLUSH_TIME = EndpointDefinition(
        path="sParam.cascade.heatpump[%s].param.sourceFlushTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_precision=0,
    )


class HeatingCircuit(_DeviceTypeEnum, device_type=DeviceType.HEATING_CIRCUIT):
    """Endpoints of a heating circuit."""

    NAME = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.name",
        value_type=str,
    )
    TYPE = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].type",
        value_type=HeatingCircuitType,
    )
    HAS_ROOM_TEMPERATURE_SENSOR = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].hasRoomTemp",
        value_type=bool,
    )
    HAS_ROOM_HUMIDITY_SENSOR = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].hasRoomHumidity",
        value_type=bool,
    )
    HAS_MIXER = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].hasMixer",
        value_type=bool,
    )
    HAS_RETURN_TEMPERATURE_SENSOR = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].hasRefluxTemp",
        value_type=bool,
    )
    HAS_PUMP = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].hasPump",
        value_type=bool,
    )
    HAS_VARIABLE_SPEED_PUMP = EndpointDefinition(
        path="sParam.options.heatCircuit[%s].hasVarSpeedPump",
        value_type=bool,
    )
    OPERATING_MODE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.operatingMode",
        value_type=HeatingCircuitOperatingMode,
    )
    TARGET_ROOM_TEMPERATURE_NORMAL = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.normalSetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_ROOM_COOLING_TEMPERATURE_NORMAL = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.normalCoolSetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    HEATING_LIMIT_NORMAL = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.thresholdDayTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    COOLING_LIMIT_NORMAL = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.thresholdDayCoolTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_ROOM_TEMPERATURE_REDUCED = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.reducedSetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_ROOM_COOLING_TEMPERATURE_REDUCED = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.reducedCoolSetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    HEATING_LIMIT_REDUCED = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.thresholdNightTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    COOLING_LIMIT_REDUCED = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.thresholdNightCoolTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_ROOM_TEMPERATURE_VACATION = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.holidaySetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    # Unix timestamp in seconds (UTC), the Web HMI sets the start to 00:00:00 and the end to 23:59:59 local time.
    VACATION_START = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.holiday.start",
        value_type=int,
    )
    VACATION_END = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.holiday.stop",
        value_type=int,
    )
    ROOM_TEMPERATURE_OFFSET = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.offsetRoomTemp",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    USE_CURVE_TABLE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.enableHeatCurveLinTab",
        value_type=bool,
    )
    HEATING_CURVE_OFFSET = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.heatCurveOffset",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    HEATING_CURVE_SLOPE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.heatCurveGradient",
        value_type=float,
        display_precision=2,
    )
    HEATING_CURVE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.linTab.fileName",
        value_type=str,
    )
    COOLING_CURVE_OFFSET = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.coolCurveOffset",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    COOLING_CURVE_SLOPE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.coolCurveGradient",
        value_type=float,
        display_precision=2,
    )
    COOLING_CURVE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.coollinTab.fileName",
        value_type=str,
    )
    SELECTED_TARGET_ROOM_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.selectedSetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
    )
    TARGET_ROOM_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.setValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_FLOW_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.flowSetTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    HEATING_REQUEST = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.heatRequest",
        value_type=HeatingCircuitRequest,
    )
    COOLING_REQUEST = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.coolRequest",
        value_type=HeatingCircuitRequest,
    )
    ROOM_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].tempRoom.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatCircuit[%s].tempRoom",
    )
    ROOM_HUMIDITY = EndpointDefinition(
        path="sParam.heatCircuit[%s].humidityRoom.values.actValue",
        value_type=float,
        raw_unit=_PERCENT,
        display_precision=0,
        message_id="sParam.heatCircuit[%s].humidityRoom",
    )
    DEW_POINT = EndpointDefinition(
        path="sParam.heatCircuit[%s].dewPoint.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatCircuit[%s].dewPoint",
    )
    FILTERED_OUTDOOR_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.filteredOutTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    MIXER_FLOW_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].heatCircuitMixer.flowTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatCircuit[%s].heatCircuitMixer.flowTemp",
    )
    MIXER_RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].heatCircuitMixer.refluxTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatCircuit[%s].heatCircuitMixer.refluxTemp",
    )
    MIXER_SETPOINT = EndpointDefinition(
        path="sParam.heatCircuit[%s].heatCircuitMixer.mixer.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.heatCircuit[%s].heatCircuitMixer.mixer",
    )
    RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].tempReflux.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.heatCircuit[%s].tempReflux",
    )
    PUMP_ACTIVE = EndpointDefinition(
        path="sParam.heatCircuit[%s].pump.values.setValueB",
        value_type=bool,
        message_id="sParam.heatCircuit[%s].pump",
    )
    PUMP_SPEED = EndpointDefinition(
        path="sParam.heatCircuit[%s].pumpAO.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.heatCircuit[%s].pumpAO",
    )
    USE_EXCESS_ENERGY = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergy.useExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_TARGET_ROOM_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergyTemp.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_TARGET_ROOM_TEMPERATURE_HYSTERESIS = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergyTemp.hyst",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    EXCESS_ENERGY_TARGET_ROOM_COOLING_TEMPERATURE = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergyTempCool.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_TARGET_ROOM_COOLING_TEMPERATURE_HYSTERESIS = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergyTempCool.hyst",
        value_type=float,
        raw_unit=_KELVIN,
        display_precision=1,
    )
    EXCESS_ENERGY_HEATING_LIMIT_NORMAL = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdDayTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_COOLING_LIMIT_NORMAL = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdDayCoolTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_HEATING_LIMIT_REDUCED = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdNightTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_COOLING_LIMIT_REDUCED = EndpointDefinition(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdNightCoolTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    EXCESS_ENERGY_STATE = EndpointDefinition(
        path="sParam.heatCircuit[%s].values.useExcessEnergy",
        value_type=ExcessEnergyState,
    )


class SolarCircuit(_DeviceTypeEnum, device_type=DeviceType.SOLAR_CIRCUIT):
    """Endpoints of a solar differential controller (*Diff. Regler*).

    ``CONSUMER_*`` endpoints have one value per consumer (two per solar circuit). A consumer can be a DHW tank,
    a buffer tank, a generic consumer or the heat pump source.
    """

    NAME = EndpointDefinition(
        path="sParam.solarCircuit[%s].param.name",
        value_type=str,
    )
    OPERATING_MODE = EndpointDefinition(
        path="sParam.solarCircuit[%s].param.operatingMode",
        value_type=SolarCircuitOperatingMode,
    )
    CONSUMER_TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.genericHeat[%s].param.setTempMax.value",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        quantity=2,
    )
    CONSUMER_1_PRIORITY = EndpointDefinition(
        path="sParam.hmiRetainData.consumer1PrioritySolar[%s]",
        value_type=bool,
        writable=True,
    )
    CONSUMER_HEATING_REQUEST = EndpointDefinition(
        path="sParam.genericHeat[%s].values.heatRequest",
        value_type=bool,
        quantity=2,
    )
    COLLECTOR_TEMPERATURE = EndpointDefinition(
        path="sParam.solarCircuit[%s].collectorTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.solarCircuit[%s].collectorTemp",
    )
    CONSUMER_TEMPERATURE = EndpointDefinition(
        path="sParam.genericHeat[%s].referenceTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.genericHeat[%s].referenceTemp",
        quantity=2,
    )
    PUMP_1_SPEED = EndpointDefinition(
        path="sParam.solarCircuit[%s].values.pump1",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    PUMP_2_SPEED = EndpointDefinition(
        path="sParam.solarCircuit[%s].values.pump2",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    METER_THERMAL_POWER = EndpointDefinition(
        path="sParam.solarCircuit[%s].heatMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=0,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    METER_ACCUMULATED_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.solarCircuit[%s].heatMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    METER_DAILY_THERMAL_ENERGY = EndpointDefinition(
        path="sParam.solarCircuit[%s].heatMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    METER_MASS_FLOW = EndpointDefinition(
        path="sParam.solarCircuit[%s].heatMeter.values.massFlow",
        value_type=float,
        raw_unit=_KILOGRAM_PER_SECOND,
        display_unit=_KILOGRAM_PER_HOUR,
        display_factor=_KILOGRAM_PER_SECOND_TO_KILOGRAM_PER_HOUR,
        display_precision=1,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.solarCircuit[%s].consumption.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=1,
    )
    OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.solarCircuit[%s].consumption.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    _CONSUMER_PRIORITY = EndpointDefinition(
        path="sParam.genericHeat[%s].param.priority",
        value_type=int,
        quantity=2,
    )


class ExternalHeatSource(_DeviceTypeEnum, device_type=DeviceType.EXTERNAL_HEAT_SOURCE):
    """Endpoints of an external heat source."""

    HAS_EMISSIONS = EndpointDefinition(
        path="sParam.extHeatSource[%s].param.hasEmmission",
        value_type=bool,
    )
    OPERATING_MODE = EndpointDefinition(
        path="sParam.extHeatSource[%s].param.operatingMode",
        value_type=ExternalHeatSourceOperatingMode,
        message_id="sParam.extHeatSource[%s]",
    )
    TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.extHeatSource[%s].values.setTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.extHeatSource[%s]",
    )
    HEATING_REQUEST = EndpointDefinition(
        path="sParam.extHeatSource[%s].DO.values.setValueB",
        value_type=bool,
        message_id="sParam.extHeatSource[%s].DO",
    )
    TEMPERATURE = EndpointDefinition(
        path="sParam.extHeatSource[%s].TI.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.extHeatSource[%s].TI",
    )
    RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.extHeatSource[%s].TempReflux.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.extHeatSource[%s].TempReflux",
    )
    USE_EXCESS_ENERGY = EndpointDefinition(
        path="sParam.extHeatSource[%s].param.supportExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_MIN_RUNTIME = EndpointDefinition(
        path="sParam.extHeatSource[%s].param.minRunTimeExcessEnergy",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_MINUTE,
        display_factor=_SECOND_TO_MINUTE,
        display_precision=0,
    )
    EXCESS_ENERGY_ACTIVE = EndpointDefinition(
        path="sParam.extHeatSource[%s].values.consumingExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_OPERATING_TIME = EndpointDefinition(
        path="sParam.extHeatSource[%s].operationalDataExcessEnergy.operationalTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_MAX_RUNTIME = EndpointDefinition(
        path="sParam.extHeatSource[%s].operationalDataExcessEnergy.maxRunTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    EXCESS_ENERGY_ACTIVATION_COUNTER = EndpointDefinition(
        path="sParam.extHeatSource[%s].operationalDataExcessEnergy.activationCounter",
        value_type=int,
        display_precision=0,
    )
    OPERATING_TIME = EndpointDefinition(
        path="sParam.extHeatSource[%s].DO.operationalData.operationalTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=0,
        message_id="sParam.extHeatSource[%s].DO",
    )
    MAX_RUNTIME = EndpointDefinition(
        path="sParam.extHeatSource[%s].DO.operationalData.maxRunTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
        message_id="sParam.extHeatSource[%s].DO",
    )
    ACTIVATION_COUNTER = EndpointDefinition(
        path="sParam.extHeatSource[%s].DO.operationalData.activationCounter",
        value_type=int,
        display_precision=0,
        message_id="sParam.extHeatSource[%s].DO",
    )

    CASCADE_STATE = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].values.state",
        value_type=CascadeState,
    )
    CASCADE_POWER_LEVEL = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].values.actPowerScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    CASCADE_PRIORITY = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.priority",
        value_type=int,
        display_precision=0,
    )
    USE_CASCADE_MODE_PRIORITIES = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.useModePriorities",
        value_type=bool,
    )
    CASCADE_COOLING_PRIORITY = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.priorityCool",
        value_type=int,
        display_precision=0,
    )
    CASCADE_DHW_PRIORITY = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.priorityDHW",
        value_type=int,
        display_precision=0,
    )
    USE_CASCADE_DHW_HEATING = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.domesticHWheatup",
        value_type=bool,
    )
    CASCADE_LOCKED = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.isLocked",
        value_type=bool,
    )
    CASCADE_FORCED_ACTIVATION = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.isForced",
        value_type=bool,
    )
    CASCADE_STARTUP_TIME = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.startupTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_precision=0,
    )
    CASCADE_POST_RUN_TIME = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.cooldownTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_precision=0,
    )
    CASCADE_SOURCE_FLUSH_TIME = EndpointDefinition(
        path="sParam.cascade.extHeatSource[%s].param.sourceFlushTimeS",
        value_type=int,
        raw_unit=_SECOND,
        display_precision=0,
    )


class Cascade(_DeviceTypeEnum, device_type=DeviceType.CASCADE):
    """Endpoints of the cascade, which distributes the power to the heat pumps and external heat sources.

    The cascade also runs with only one heat generator, its statistics are summed over all heat generators.
    """

    USE_CASCADE_CONTROL = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.cascadeControl",
        value_type=bool,
    )
    USE_DHW_CASCADE_CONTROL = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.cascadeControlDHW",
        value_type=bool,
    )
    STRATEGY = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.strategy",
        value_type=CascadeStrategy,
    )
    MODULATION_RANGE = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.modulationPowerDeltaScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    OVERDRIVE_LIMIT = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.overdrivePowerScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    USE_SYNCHRONIZED_DEFROST = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.sychronizedDefrosting",
        value_type=bool,
    )
    USE_SYNCHRONIZED_UTILITY_LOCK = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.sychronizedExternalLock",
        value_type=bool,
    )
    USE_MULTI_SOURCE_MODULATION = EndpointDefinition(
        path="sParam.cascade.cascadeControl.param.useMultiSourceModulation",
        value_type=bool,
    )
    TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.setTemp",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
    )
    TARGET_POWER_LEVEL = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.setPowerScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    POWER_LEVEL = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.actPowerScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    NOMINAL_POWER = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.nominalSumPower",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=0,
    )
    THERMAL_POWER = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.sumPowerGeneration",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
    )
    ELECTRICAL_POWER = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.sumPowerConsumption",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
    )
    EXCESS_ENERGY_TARGET_POWER_LEVEL = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.setPVPowerScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
    )
    COP = EndpointDefinition(
        path="sParam.cascade.cascadeControl.values.COP",
        value_type=float,
        display_precision=2,
    )
    HEATING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.heating.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    HEATING_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.heating.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    HEATING_SPF = EndpointDefinition(
        path="sStatisticalData.cascade.EnergyEfficiencyRatioHeat",
        value_type=float,
    )
    HEATING_PF = EndpointDefinition(
        path="sStatisticalData.cascade.OverallEERHeat",
        value_type=float,
        display_precision=2,
    )
    HEATING_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.heating.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    COOLING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.cooling.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    COOLING_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.cooling.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    COOLING_SPF = EndpointDefinition(
        path="sStatisticalData.cascade.EnergyEfficiencyRatioCool",
        value_type=float,
        display_precision=2,
    )
    COOLING_PF = EndpointDefinition(
        path="sStatisticalData.cascade.OverallEERCool",
        value_type=float,
        display_precision=2,
    )
    COOLING_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.cooling.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    DHW_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.domHotWater.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DHW_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.domHotWater.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DHW_SPF = EndpointDefinition(
        path="sStatisticalData.cascade.EnergyEfficiencyRatioDomHotWater",
        value_type=float,
    )
    DHW_PF = EndpointDefinition(
        path="sStatisticalData.cascade.OverallEERDomHotWater",
        value_type=float,
        display_precision=2,
    )
    DHW_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.domHotWater.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    DEFROST_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.data.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DEFROST_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.data.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    DEFROST_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.data.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    DEFROST_CYCLES = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.cycles",
        value_type=int,
        display_precision=0,
    )
    FAILED_DEFROST_CYCLES = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.failedCycles",
        value_type=int,
        display_precision=0,
    )
    TOTAL_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.energy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    TOTAL_ELECTRICAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.electricalenergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    TOTAL_SPF = EndpointDefinition(
        path="sStatisticalData.cascade.EnergyEfficiencyRatio",
        value_type=float,
        display_precision=2,
    )
    TOTAL_PF = EndpointDefinition(
        path="sStatisticalData.cascade.OverallEER",
        value_type=float,
        display_precision=2,
    )
    TOTAL_OPERATING_TIME = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.operatingtime",
        value_type=int,
        raw_unit=_SECOND,
        display_unit=_HOUR,
        display_factor=_SECOND_TO_HOUR,
        display_precision=1,
    )
    # The Web HMI has no text and unit for the thermal excess energy per mode, the unit is the one of the total
    # and of all other energy values of the same mode (`kWhwithoutConv`, raw kWh).
    EXCESS_ENERGY_HEATING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.heating.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_HEATING_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.heating.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_COOLING_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.cooling.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_COOLING_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.cooling.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_DHW_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.domHotWater.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_DHW_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.domHotWater.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_DEFROST_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.data.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_DEFROST_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.defrost.data.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_THERMAL_ENERGY = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.energyExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )
    EXCESS_ENERGY_CONSUMPTION = EndpointDefinition(
        path="sStatisticalData.cascade.consumption.consumedExcessEnergy",
        value_type=float,
        raw_unit=_KILOWATT_HOUR,
        display_precision=0,
    )


class SwitchValve(_DeviceTypeEnum, device_type=DeviceType.SWITCH_VALVE):
    """Endpoints of a switch valve."""

    POSITION = EndpointDefinition(
        path="sParam.switchvalve[%s].values.actPosition",
        value_type=SwitchValvePosition,
    )


class PassiveCooling(_DeviceTypeEnum, device_type=DeviceType.PASSIVE_COOLING):
    """Endpoints of a passive cooling unit (one per heat pump)."""

    MIXER_TARGET_TEMPERATURE = EndpointDefinition(
        path="sParam.passivecooling[%s].Mixer.values.setValue",
        value_type=float,
        raw_unit=_CELSIUS,
        message_id="sParam.passivecooling[%s].Mixer",
    )
    TEMPERATURE = EndpointDefinition(
        path="sParam.passivecooling[%s].TempCoolPassive.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.passivecooling[%s].TempCoolPassive",
    )
    FLOW_TEMPERATURE = EndpointDefinition(
        path="sParam.passivecooling[%s].TempFlow.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.passivecooling[%s].TempFlow",
    )
    RETURN_TEMPERATURE = EndpointDefinition(
        path="sParam.passivecooling[%s].TempReflux.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.passivecooling[%s].TempReflux",
    )
    SWITCH_VALVE_POSITION = EndpointDefinition(
        path="sParam.passivecooling[%s].SwitchValvePassiveCool.values.actPosition",
        value_type=SwitchValvePosition,
        message_id="sParam.passivecooling[%s].SwitchValvePassiveCool",
    )
    CIRCULATION_PUMP_SPEED = EndpointDefinition(
        path="sParam.passivecooling[%s].Pump.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.passivecooling[%s].Pump",
    )
    MIXER_FLOW_TEMPERATURE = EndpointDefinition(
        path="sParam.passivecooling[%s].Mixer.flowTemp.values.actValue",
        value_type=float,
        raw_unit=_CELSIUS,
        display_precision=1,
        message_id="sParam.passivecooling[%s].Mixer.flowTemp",
    )
    MIXER_SETPOINT = EndpointDefinition(
        path="sParam.passivecooling[%s].Mixer.mixer.values.setValueScaled",
        value_type=float,
        display_unit=_PERCENT,
        display_factor=_RATIO_TO_PERCENT,
        display_precision=0,
        message_id="sParam.passivecooling[%s].Mixer.mixer",
    )


class Photovoltaics(_DeviceTypeEnum, device_type=DeviceType.PHOTOVOLTAICS):
    """Endpoints of the photovoltaics."""

    EXCESS_ENERGY_ACTIVE = EndpointDefinition(
        path="sParam.photovoltaics.values.excessEnergyActive",
        value_type=bool,
    )
    METER_EXCESS_POWER = EndpointDefinition(
        path="sParam.photovoltaics.ElectricEnergyMeter.values.power",
        value_type=float,
        raw_unit=_WATT,
        display_unit=_KILOWATT,
        display_factor=_WATT_TO_KILOWATT,
        display_precision=2,
        message_id="sParam.photovoltaics.ElectricEnergyMeter",
    )
    METER_ACCUMULATED_EXCESS_ENERGY = EndpointDefinition(
        path="sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=0,
        message_id="sParam.photovoltaics.ElectricEnergyMeter",
    )
    METER_DAILY_EXCESS_ENERGY = EndpointDefinition(
        path="sParam.photovoltaics.ElectricEnergyMeter.values.heatDay",
        value_type=float,
        raw_unit=_JOULE,
        display_unit=_KILOWATT_HOUR,
        display_factor=_JOULE_TO_KILOWATT_HOUR,
        display_precision=1,
        message_id="sParam.photovoltaics.ElectricEnergyMeter",
    )


type Endpoint = (
    BufferTank
    | Cascade
    | DHWTank
    | ExternalHeatSource
    | HeatingCircuit
    | HeatPump
    | PassiveCooling
    | Photovoltaics
    | SolarCircuit
    | SwitchValve
    | System
)
