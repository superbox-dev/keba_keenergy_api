# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Endpoint definitions of the KEBA KeEnergy Web HMI, one enum per device type."""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from keba_keenergy_api.constants import _BAR
from keba_keenergy_api.constants import _CELSIUS
from keba_keenergy_api.constants import _JOULE
from keba_keenergy_api.constants import _KELVIN
from keba_keenergy_api.constants import _KILOBYTE
from keba_keenergy_api.constants import _KILOWATT_HOUR
from keba_keenergy_api.constants import _MESSAGE_ID_SUFFIX
from keba_keenergy_api.constants import _MINUTE
from keba_keenergy_api.constants import _PAYLOAD_PREFIX
from keba_keenergy_api.constants import _PER_MILLE
from keba_keenergy_api.constants import _PERCENT
from keba_keenergy_api.constants import _SECOND
from keba_keenergy_api.constants import _WATT
from keba_keenergy_api.enums import BufferTankOperatingMode
from keba_keenergy_api.enums import DeviceType
from keba_keenergy_api.enums import DHWTankOperatingMode
from keba_keenergy_api.enums import ElectricEnergyMeterType
from keba_keenergy_api.enums import ExcessEnergyState
from keba_keenergy_api.enums import ExternalHeatSourceOperatingMode
from keba_keenergy_api.enums import HeatingCircuitOperatingMode
from keba_keenergy_api.enums import HeatingCircuitRequest
from keba_keenergy_api.enums import HeatingCircuitType
from keba_keenergy_api.enums import HeatMeterType
from keba_keenergy_api.enums import HeatPumpState
from keba_keenergy_api.enums import HeatPumpSubState
from keba_keenergy_api.enums import SolarCircuitOperatingMode
from keba_keenergy_api.enums import SwitchValvePosition
from keba_keenergy_api.enums import SystemOperatingMode

type EndpointType = type[bool | Enum | float | int | str]


@dataclass(frozen=True, kw_only=True)
class Endpoint:
    """Definition of a Web HMI variable.

    Attributes
    ----------
    path
        Variable path relative to ``APPL.CtrlAppl``, ``%s`` is replaced by the zero-based device index.
    value_type
        Type of the value: ``bool``, ``float``, ``int``, ``str`` or an enum.
    unit
        Unit of the value as the Web HMI delivers it, ``None`` for values without a unit or ratios (``0..1``).
    writable
        Whether the variable can be written. Paths containing ``.param.`` are always writable.
    message_id
        Path of the component node that has a message id (``state.msgId``) for this value, ``None`` if there is none.
    quantity
        Number of values per device, e.g. two consumers per solar circuit.

    """

    path: str
    value_type: EndpointType
    unit: str | None = None
    writable: bool = False
    message_id: str | None = None
    quantity: int = 1

    def __post_init__(self) -> None:
        """Derive the writable state from the path and validate the message id node."""
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


class _SectionEnum(Enum):
    """Base of the section enums, the device type is given as class keyword."""

    _value_: Endpoint
    device_type: ClassVar[DeviceType]

    def __init_subclass__(cls, *, device_type: DeviceType, **kwargs: object) -> None:
        """Set the device type of the section."""
        super().__init_subclass__(**kwargs)
        cls.device_type = device_type


class System(_SectionEnum, device_type=DeviceType.SYSTEM):
    """Endpoints of the system."""

    _NUMBER_OF_BUFFER_TANKS = Endpoint(
        path="sParam.options.systemNumberOfBuffers",
        value_type=int,
    )
    _NUMBER_OF_DHW_TANKS = Endpoint(
        path="sParam.options.systemNumberOfHotWaterTanks",
        value_type=int,
    )
    _NUMBER_OF_HEAT_PUMPS = Endpoint(
        path="sParam.options.systemNumberOfHeatPumps",
        value_type=int,
    )
    _NUMBER_OF_HEATING_CIRCUITS = Endpoint(
        path="sParam.options.systemNumberOfHeatingCircuits",
        value_type=int,
    )
    _NUMBER_OF_SOLAR_CIRCUITS = Endpoint(
        path="sParam.options.systemNumberOfSolarCircuits",
        value_type=int,
    )
    _NUMBER_OF_EXTERNAL_HEAT_SOURCES = Endpoint(
        path="sParam.options.systemNumberOfExtHeatSources",
        value_type=int,
    )
    _NUMBER_OF_SWITCH_VALVES = Endpoint(
        path="sParam.options.systemNumberOfSwitchValves",
        value_type=int,
    )
    HAS_PHOTOVOLTAICS = Endpoint(
        path="sParam.options.hasPhotovoltaics",
        value_type=bool,
    )
    HAS_OUTDOOR_TEMPERATURE = Endpoint(
        path="sParam.options.hasOutdoorTemp",
        value_type=bool,
    )
    OPERATING_MODE = Endpoint(
        path="sParam.param.operatingMode",
        value_type=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE = Endpoint(
        path="sParam.outdoorTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.outdoorTemp",
    )
    CPU_USAGE = Endpoint(
        path="sProcData.globalCpuTimePercent",
        value_type=float,
        unit=_PER_MILLE,
    )
    WEBVIEW_CPU_USAGE = Endpoint(
        path="sProcData.processStatus[0].cpuTimePercent",
        value_type=float,
        unit=_PER_MILLE,
    )
    WEBSERVER_CPU_USAGE = Endpoint(
        path="sProcData.processStatus[1].cpuTimePercent",
        value_type=float,
        unit=_PER_MILLE,
    )
    CONTROL_CPU_USAGE = Endpoint(
        path="sProcData.processStatus[2].cpuTimePercent",
        value_type=float,
        unit=_PER_MILLE,
    )
    TEMPORARY_MEMORY_USAGE = Endpoint(
        path="sProcData.RAMstatus.tmpfs",
        value_type=int,
        unit=_KILOBYTE,
    )
    FREE_RAM = Endpoint(
        path="sProcData.totFreeRAM",
        value_type=int,
        unit=_KILOBYTE,
    )
    FLASH_MAX_ERASE_COUNTER = Endpoint(
        path="sParam.values.UBIMaxEraseCounter",
        value_type=int,
    )


class BufferTank(_SectionEnum, device_type=DeviceType.BUFFER_TANK):
    """Endpoints of a buffer tank."""

    NAME = Endpoint(
        path="sParam.bufferTank[%s].param.name",
        value_type=str,
    )
    TOP_TEMPERATURE = Endpoint(
        path="sParam.bufferTank[%s].topTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.bufferTank[%s].topTemp",
    )
    BOTTOM_TEMPERATURE = Endpoint(
        path="sParam.bufferTank[%s].midTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.bufferTank[%s].midTemp",
    )
    OPERATING_MODE = Endpoint(
        path="sParam.bufferTank[%s].param.operatingMode",
        value_type=BufferTankOperatingMode,
    )
    BACKUP_TEMPERATURE = Endpoint(
        path="sParam.bufferTank[%s].param.backupTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_TEMPERATURE = Endpoint(
        path="sParam.bufferTank[%s].values.setTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = Endpoint(
        path="sParam.bufferTank[%s].param.excessEnergyTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = Endpoint(
        path="sParam.bufferTank[%s].param.excessEnergyTemp.hyst",
        value_type=float,
        unit=_KELVIN,
    )
    EXCESS_ENERGY_OUTDOOR_TEMPERATURE_LIMIT = Endpoint(
        path="sParam.bufferTank[%s].param.thresholdOutTempExcessEnergy.value",
        value_type=float,
        unit=_CELSIUS,
    )
    USE_EXCESS_ENERGY = Endpoint(
        path="sParam.bufferTank[%s].param.useExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_STATE = Endpoint(
        path="sParam.bufferTank[%s].values.useExcessEnergy",
        value_type=ExcessEnergyState,
    )
    HEATING_REQUEST = Endpoint(
        path="sParam.bufferTank[%s].values.heatRequestTop",
        value_type=bool,
    )
    COOLING_REQUEST = Endpoint(
        path="sParam.bufferTank[%s].values.coolRequestBot",
        value_type=bool,
    )


class DHWTank(_SectionEnum, device_type=DeviceType.DHW_TANK):
    """Endpoints of a DHW tank."""

    NAME = Endpoint(
        path="sParam.hotWaterTank[%s].param.name",
        value_type=str,
    )
    TEMPERATURE = Endpoint(
        path="sParam.hotWaterTank[%s].topTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.hotWaterTank[%s].topTemp",
    )
    OPERATING_MODE = Endpoint(
        path="sParam.hotWaterTank[%s].param.operatingMode",
        value_type=DHWTankOperatingMode,
    )
    BACKUP_TEMPERATURE = Endpoint(
        path="sParam.hotWaterTank[%s].param.reducedSetTempMax.value",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_TEMPERATURE = Endpoint(
        path="sParam.hotWaterTank[%s].param.normalSetTempMax.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = Endpoint(
        path="sParam.hotWaterTank[%s].param.excessEnergyTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = Endpoint(
        path="sParam.hotWaterTank[%s].param.excessEnergyTemp.hyst",
        value_type=float,
        unit=_KELVIN,
    )
    USE_EXCESS_ENERGY = Endpoint(
        path="sParam.hotWaterTank[%s].param.useExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_STATE = Endpoint(
        path="sParam.hotWaterTank[%s].values.useExcessEnergy",
        value_type=ExcessEnergyState,
    )
    HEATING_REQUEST = Endpoint(
        path="sParam.hotWaterTank[%s].values.heatRequestTop",
        value_type=bool,
    )
    HAS_FRESH_WATER_MODULE = Endpoint(
        path="sParam.options.hotWaterTank[%s].hasFreshWaterModule",
        value_type=bool,
    )
    FRESH_WATER_FLOW_ACTIVE = Endpoint(
        path="sParam.hotWaterTank[%s].FreshWater.freshWaterFlow.values.actValue",
        value_type=bool,
        message_id="sParam.hotWaterTank[%s].FreshWater.freshWaterFlow",
    )
    FRESH_WATER_TEMPERATURE = Endpoint(
        path="sParam.hotWaterTank[%s].FreshWater.freshWaterTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.hotWaterTank[%s].FreshWater.freshWaterTemp",
    )
    CIRCULATION_RETURN_TEMPERATURE = Endpoint(
        path="sParam.hotWaterTank[%s].circTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.hotWaterTank[%s].circTemp",
    )
    CIRCULATION_PUMP_ACTIVE = Endpoint(
        path="sParam.hotWaterTank[%s].circPump.pump.values.setValueB",
        value_type=bool,
        message_id="sParam.hotWaterTank[%s].circPump.pump",
    )


class HeatPump(_SectionEnum, device_type=DeviceType.HEAT_PUMP):
    """Endpoints of a heat pump."""

    NAME = Endpoint(
        path="sParam.heatpump[%s].param.name",
        value_type=str,
    )
    STATE = Endpoint(
        path="sParam.heatpump[%s].values.heatpumpState",
        value_type=HeatPumpState,
    )
    SUB_STATE = Endpoint(
        path="sParam.heatpump[%s].values.heatpumpSubState",
        value_type=HeatPumpSubState,
    )
    USE_COMPRESSOR_NIGHT_POWER_LIMIT = Endpoint(
        path="sParam.heatpump[%s].HeatPumpPowerCtrl.param.useDayNightSpeed",
        value_type=bool,
    )
    COMPRESSOR_NIGHT_POWER_LIMIT = Endpoint(
        path="sParam.heatpump[%s].HeatPumpPowerCtrl.param.maxPowerScaledNight",
        value_type=float,
    )
    CIRCULATION_PUMP_SPEED = Endpoint(
        path="sParam.heatpump[%s].CircPump.values.setValueScaled",
        value_type=float,
        message_id="sParam.heatpump[%s].CircPump",
    )
    SOURCE_ACTUATOR_SPEED = Endpoint(
        path="sParam.heatpump[%s].Source.values.setValueScaled",
        value_type=float,
        message_id="sParam.heatpump[%s].Source",
    )
    FLOW_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].TempHeatFlow.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].TempHeatFlow",
    )
    RETURN_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].TempHeatReflux.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].TempHeatReflux",
    )
    SOURCE_INLET_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].TempSourceIn.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].TempSourceIn",
    )
    SOURCE_OUTLET_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].TempSourceOut.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].TempSourceOut",
    )
    COMPRESSOR_INLET_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].TempCompressorIn.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].TempCompressorIn",
    )
    COMPRESSOR_OUTLET_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].TempCompressorOut.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].TempCompressorOut",
    )
    COMPRESSOR_SPEED = Endpoint(
        path="sParam.heatpump[%s].Compressor.values.setValueScaled",
        value_type=float,
        message_id="sParam.heatpump[%s].Compressor",
    )
    CONDENSATION_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].OverHeatCtrl.values.tempCond",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    EVAPORATION_TEMPERATURE = Endpoint(
        path="sParam.heatpump[%s].OverHeatCtrl.values.tempVap",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    TARGET_SUCTION_SUPERHEAT = Endpoint(
        path="sParam.heatpump[%s].OverHeatCtrl.values.setOH",
        value_type=float,
        unit=_KELVIN,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    SUCTION_SUPERHEAT = Endpoint(
        path="sParam.heatpump[%s].OverHeatCtrl.values.actOH",
        value_type=float,
        unit=_KELVIN,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    EXPANSION_VALVE_POSITION = Endpoint(
        path="sParam.heatpump[%s].OverHeatCtrl.values.stepperPos",
        value_type=int,
        message_id="sParam.heatpump[%s].OverHeatCtrl",
    )
    HIGH_PRESSURE = Endpoint(
        path="sParam.heatpump[%s].HighPressure.values.actValue",
        value_type=float,
        unit=_BAR,
        message_id="sParam.heatpump[%s].HighPressure",
    )
    LOW_PRESSURE = Endpoint(
        path="sParam.heatpump[%s].LowPressure.values.actValue",
        value_type=float,
        unit=_BAR,
        message_id="sParam.heatpump[%s].LowPressure",
    )
    REQUEST = Endpoint(
        path="sParam.heatpump[%s].values.request",
        value_type=bool,
    )
    EXCESS_ENERGY_ACTIVE = Endpoint(
        path="sParam.heatpump[%s].values.consumingExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_OPERATING_TIME = Endpoint(
        path="sParam.heatpump[%s].operationalDataExcessEnergy.operationalTimeS",
        value_type=int,
        unit=_SECOND,
    )
    EXCESS_ENERGY_MAX_RUNTIME = Endpoint(
        path="sParam.heatpump[%s].operationalDataExcessEnergy.maxRunTimeS",
        value_type=int,
        unit=_SECOND,
    )
    EXCESS_ENERGY_ACTIVATION_COUNTER = Endpoint(
        path="sParam.heatpump[%s].operationalDataExcessEnergy.activationCounter",
        value_type=int,
    )
    HEATING_THERMAL_POWER = Endpoint(
        path="sParam.heatpump[%s].HeatMeter.values.power",
        value_type=float,
        unit=_WATT,
        message_id="sParam.heatpump[%s].HeatMeter",
    )
    DHW_THERMAL_POWER = Endpoint(
        path="sParam.heatpump[%s].HotWaterMeter.values.power",
        value_type=float,
        unit=_WATT,
        message_id="sParam.heatpump[%s].HotWaterMeter",
    )
    ELECTRICAL_POWER = Endpoint(
        path="sParam.heatpump[%s].ElectricEnergyMeter.values.power",
        value_type=float,
        unit=_WATT,
        message_id="sParam.heatpump[%s].ElectricEnergyMeter",
    )
    COP = Endpoint(
        path="sParam.heatpump[%s].values.COP",
        value_type=float,
    )
    HEATING_THERMAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.heating.energy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    HEATING_ELECTRICAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.heating.electricalenergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    HEATING_SPF = Endpoint(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatioHeat",
        value_type=float,
    )
    COOLING_THERMAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.cooling.energy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    COOLING_ELECTRICAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.cooling.electricalenergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    COOLING_SPF = Endpoint(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatioCool",
        value_type=float,
    )
    DHW_THERMAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.energy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    DHW_ELECTRICAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.electricalenergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    DHW_SPF = Endpoint(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatioDomHotWater",
        value_type=float,
    )
    TOTAL_THERMAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.energy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    TOTAL_ELECTRICAL_ENERGY = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.electricalenergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_CONSUMPTION = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.consumedExcessEnergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_HEATING_CONSUMPTION = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.heating.consumedExcessEnergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_COOLING_CONSUMPTION = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.cooling.consumedExcessEnergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    EXCESS_ENERGY_DHW_CONSUMPTION = Endpoint(
        path="sStatisticalData.heatpump[%s].consumption.domHotWater.consumedExcessEnergy",
        value_type=float,
        unit=_KILOWATT_HOUR,
    )
    TOTAL_SPF = Endpoint(
        path="sStatisticalData.heatpump[%s].EnergyEfficiencyRatio",
        value_type=float,
    )
    HAS_ACTIVE_COOLING = Endpoint(
        path="sParam.options.heatpump[%s].hasActiveCooling",
        value_type=bool,
    )
    HAS_PASSIVE_COOLING = Endpoint(
        path="sParam.options.heatpump[%s].hasPassiveCooling",
        value_type=bool,
    )
    OPERATING_TIME = Endpoint(
        path="sParam.heatpump[%s].operationalData.operationalTimeS",
        value_type=int,
        unit=_SECOND,
    )
    MAX_RUNTIME = Endpoint(
        path="sParam.heatpump[%s].operationalData.maxRunTimeS",
        value_type=int,
        unit=_SECOND,
    )
    ACTIVATION_COUNTER = Endpoint(
        path="sParam.heatpump[%s].operationalData.activationCounter",
        value_type=int,
    )
    COMPRESSOR_FAILURE = Endpoint(
        path="sParam.heatpump[%s].FailureCompressor.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureCompressor",
    )
    SOURCE_FAILURE = Endpoint(
        path="sParam.heatpump[%s].FailureSource.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureSource",
    )
    SOURCE_ACTUATOR_FAILURE = Endpoint(
        path="sParam.heatpump[%s].FailureActuatorSource.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureActuatorSource",
    )
    THREE_PHASE_FAILURE = Endpoint(
        path="sParam.heatpump[%s].FailureThreePhase.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureThreePhase",
    )
    SOURCE_PRESSURE_FAILURE = Endpoint(
        path="sParam.heatpump[%s].FailureSrcPressure.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureSrcPressure",
    )
    VFD_FAILURE = Endpoint(
        path="sParam.heatpump[%s].FailureVFD.values.actValue",
        value_type=bool,
        message_id="sParam.heatpump[%s].FailureVFD",
    )
    ELECTRIC_ENERGY_METER_TYPE = Endpoint(
        path="sParam.options.heatpump[%s].ElectricEnergyMeter.type",
        value_type=ElectricEnergyMeterType,
    )
    HEAT_METER_TYPE = Endpoint(
        path="sParam.options.heatpump[%s].HeatMeter.type",
        value_type=HeatMeterType,
    )


class HeatingCircuit(_SectionEnum, device_type=DeviceType.HEATING_CIRCUIT):
    """Endpoints of a heating circuit."""

    NAME = Endpoint(
        path="sParam.heatCircuit[%s].param.name",
        value_type=str,
    )
    TYPE = Endpoint(
        path="sParam.options.heatCircuit[%s].type",
        value_type=HeatingCircuitType,
    )
    HAS_ROOM_TEMPERATURE = Endpoint(
        path="sParam.options.heatCircuit[%s].hasRoomTemp",
        value_type=bool,
    )
    ROOM_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].tempRoom.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatCircuit[%s].tempRoom",
    )
    HAS_ROOM_HUMIDITY = Endpoint(
        path="sParam.options.heatCircuit[%s].hasRoomHumidity",
        value_type=bool,
    )
    ROOM_HUMIDITY = Endpoint(
        path="sParam.heatCircuit[%s].humidityRoom.values.actValue",
        value_type=float,
        unit=_PERCENT,
        message_id="sParam.heatCircuit[%s].humidityRoom",
    )
    DEW_POINT = Endpoint(
        path="sParam.heatCircuit[%s].dewPoint.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatCircuit[%s].dewPoint",
    )
    TARGET_FLOW_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].values.flowSetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    HAS_MIXER = Endpoint(
        path="sParam.options.heatCircuit[%s].hasMixer",
        value_type=bool,
    )
    MIXER_FLOW_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].heatCircuitMixer.flowTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatCircuit[%s].heatCircuitMixer.flowTemp",
    )
    MIXER_RETURN_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].heatCircuitMixer.refluxTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatCircuit[%s].heatCircuitMixer.refluxTemp",
    )
    MIXER_SETPOINT = Endpoint(
        path="sParam.heatCircuit[%s].heatCircuitMixer.mixer.values.setValueScaled",
        value_type=float,
        message_id="sParam.heatCircuit[%s].heatCircuitMixer.mixer",
    )
    PUMP_ACTIVE = Endpoint(
        path="sParam.heatCircuit[%s].pump.values.setValueB",
        value_type=bool,
        message_id="sParam.heatCircuit[%s].pump",
    )
    HAS_RETURN_TEMPERATURE = Endpoint(
        path="sParam.options.heatCircuit[%s].hasRefluxTemp",
        value_type=bool,
    )
    RETURN_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].tempReflux.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.heatCircuit[%s].tempReflux",
    )
    TARGET_ROOM_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].values.setValue",
        value_type=float,
        unit=_CELSIUS,
    )
    USE_EXCESS_ENERGY = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergy.useExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_STATE = Endpoint(
        path="sParam.heatCircuit[%s].values.useExcessEnergy",
        value_type=ExcessEnergyState,
    )
    EXCESS_ENERGY_TARGET_ROOM_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergyTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_TARGET_ROOM_TEMPERATURE_HYSTERESIS = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergyTemp.hyst",
        value_type=float,
        unit=_KELVIN,
    )
    EXCESS_ENERGY_TARGET_ROOM_COOLING_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergyTempCool.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_TARGET_ROOM_COOLING_TEMPERATURE_HYSTERESIS = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergyTempCool.hyst",
        value_type=float,
        unit=_KELVIN,
    )
    SELECTED_TARGET_ROOM_TEMPERATURE = Endpoint(
        path="sParam.heatCircuit[%s].values.selectedSetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_ROOM_TEMPERATURE_NORMAL = Endpoint(
        path="sParam.heatCircuit[%s].param.normalSetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_ROOM_COOLING_TEMPERATURE_NORMAL = Endpoint(
        path="sParam.heatCircuit[%s].param.normalCoolSetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    HEATING_LIMIT_NORMAL = Endpoint(
        path="sParam.heatCircuit[%s].param.thresholdDayTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    COOLING_LIMIT_NORMAL = Endpoint(
        path="sParam.heatCircuit[%s].param.thresholdDayCoolTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_HEATING_LIMIT_NORMAL = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdDayTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_COOLING_LIMIT_NORMAL = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdDayCoolTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_ROOM_TEMPERATURE_REDUCED = Endpoint(
        path="sParam.heatCircuit[%s].param.reducedSetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_ROOM_COOLING_TEMPERATURE_REDUCED = Endpoint(
        path="sParam.heatCircuit[%s].param.reducedCoolSetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    HEATING_LIMIT_REDUCED = Endpoint(
        path="sParam.heatCircuit[%s].param.thresholdNightTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    COOLING_LIMIT_REDUCED = Endpoint(
        path="sParam.heatCircuit[%s].param.thresholdNightCoolTemp.value",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_HEATING_LIMIT_REDUCED = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdNightTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    EXCESS_ENERGY_COOLING_LIMIT_REDUCED = Endpoint(
        path="sParam.heatCircuit[%s].param.excessEnergy.thresholdNightCoolTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    TARGET_ROOM_TEMPERATURE_VACATION = Endpoint(
        path="sParam.heatCircuit[%s].param.holidaySetTemp",
        value_type=float,
        unit=_CELSIUS,
    )
    ROOM_TEMPERATURE_OFFSET = Endpoint(
        path="sParam.heatCircuit[%s].param.offsetRoomTemp",
        value_type=float,
        unit=_KELVIN,
    )
    OPERATING_MODE = Endpoint(
        path="sParam.heatCircuit[%s].param.operatingMode",
        value_type=HeatingCircuitOperatingMode,
    )
    HEATING_REQUEST = Endpoint(
        path="sParam.heatCircuit[%s].values.heatRequest",
        value_type=HeatingCircuitRequest,
    )
    COOLING_REQUEST = Endpoint(
        path="sParam.heatCircuit[%s].values.coolRequest",
        value_type=HeatingCircuitRequest,
    )
    VACATION_START = Endpoint(
        path="sParam.heatCircuit[%s].param.holiday.start",
        value_type=int,
    )
    VACATION_END = Endpoint(
        path="sParam.heatCircuit[%s].param.holiday.stop",
        value_type=int,
    )
    HEATING_CURVE_OFFSET = Endpoint(
        path="sParam.heatCircuit[%s].param.heatCurveOffset",
        value_type=float,
        unit=_KELVIN,
    )
    COOLING_CURVE_OFFSET = Endpoint(
        path="sParam.heatCircuit[%s].param.coolCurveOffset",
        value_type=float,
        unit=_KELVIN,
    )
    HEATING_CURVE_SLOPE = Endpoint(
        path="sParam.heatCircuit[%s].param.heatCurveGradient",
        value_type=float,
    )
    COOLING_CURVE_SLOPE = Endpoint(
        path="sParam.heatCircuit[%s].param.coolCurveGradient",
        value_type=float,
    )
    USE_CURVE_TABLE = Endpoint(
        path="sParam.heatCircuit[%s].param.enableHeatCurveLinTab",
        value_type=bool,
    )
    HEATING_CURVE = Endpoint(
        path="sParam.heatCircuit[%s].param.linTab.fileName",
        value_type=str,
    )
    COOLING_CURVE = Endpoint(
        path="sParam.heatCircuit[%s].param.coollinTab.fileName",
        value_type=str,
    )
    HAS_PUMP = Endpoint(
        path="sParam.options.heatCircuit[%s].hasPump",
        value_type=bool,
    )
    HAS_VARIABLE_SPEED_PUMP = Endpoint(
        path="sParam.options.heatCircuit[%s].hasVarSpeedPump",
        value_type=bool,
    )
    PUMP_SPEED = Endpoint(
        path="sParam.heatCircuit[%s].pumpAO.values.setValueScaled",
        value_type=float,
        message_id="sParam.heatCircuit[%s].pumpAO",
    )


class SolarCircuit(_SectionEnum, device_type=DeviceType.SOLAR_CIRCUIT):
    """Endpoints of a solar differential controller (*Diff. Regler*).

    ``CONSUMER_*`` endpoints have one value per consumer (two per solar circuit). A consumer can be a DHW tank,
    a buffer tank, a generic consumer or the heat pump source.
    """

    NAME = Endpoint(
        path="sParam.solarCircuit[%s].param.name",
        value_type=str,
    )
    OPERATING_MODE = Endpoint(
        path="sParam.solarCircuit[%s].param.operatingMode",
        value_type=SolarCircuitOperatingMode,
    )
    COLLECTOR_TEMPERATURE = Endpoint(
        path="sParam.solarCircuit[%s].collectorTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.solarCircuit[%s].collectorTemp",
    )
    PUMP_1_SPEED = Endpoint(
        path="sParam.solarCircuit[%s].values.pump1",
        value_type=float,
    )
    PUMP_2_SPEED = Endpoint(
        path="sParam.solarCircuit[%s].values.pump2",
        value_type=float,
    )
    CONSUMER_TEMPERATURE = Endpoint(
        path="sParam.genericHeat[%s].referenceTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.genericHeat[%s].referenceTemp",
        quantity=2,
    )
    CONSUMER_TARGET_TEMPERATURE = Endpoint(
        path="sParam.genericHeat[%s].param.setTempMax.value",
        value_type=float,
        unit=_CELSIUS,
        quantity=2,
    )
    CONSUMER_HEATING_REQUEST = Endpoint(
        path="sParam.genericHeat[%s].values.heatRequest",
        value_type=bool,
        quantity=2,
    )
    TOTAL_THERMAL_ENERGY = Endpoint(
        path="sParam.solarCircuit[%s].heatMeter.values.accumulatedHeat",
        value_type=float,
        unit=_JOULE,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    DAILY_THERMAL_ENERGY = Endpoint(
        path="sParam.solarCircuit[%s].heatMeter.values.heatDay",
        value_type=float,
        unit=_JOULE,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    THERMAL_POWER = Endpoint(
        path="sParam.solarCircuit[%s].heatMeter.values.power",
        value_type=float,
        unit=_WATT,
        message_id="sParam.solarCircuit[%s].heatMeter",
    )
    CONSUMER_1_PRIORITY = Endpoint(
        path="sParam.hmiRetainData.consumer1PrioritySolar[%s]",
        value_type=bool,
        writable=True,
    )
    _CONSUMER_PRIORITY = Endpoint(
        path="sParam.genericHeat[%s].param.priority",
        value_type=int,
        quantity=2,
    )


class ExternalHeatSource(_SectionEnum, device_type=DeviceType.EXTERNAL_HEAT_SOURCE):
    """Endpoints of an external heat source."""

    OPERATING_MODE = Endpoint(
        path="sParam.extHeatSource[%s].param.operatingMode",
        value_type=ExternalHeatSourceOperatingMode,
        message_id="sParam.extHeatSource[%s]",
    )
    TARGET_TEMPERATURE = Endpoint(
        path="sParam.extHeatSource[%s].values.setTemp",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.extHeatSource[%s]",
    )
    HEATING_REQUEST = Endpoint(
        path="sParam.extHeatSource[%s].DO.values.setValueB",
        value_type=bool,
        message_id="sParam.extHeatSource[%s].DO",
    )
    OPERATING_TIME = Endpoint(
        path="sParam.extHeatSource[%s].DO.operationalData.operationalTimeS",
        value_type=int,
        unit=_SECOND,
        message_id="sParam.extHeatSource[%s].DO",
    )
    MAX_RUNTIME = Endpoint(
        path="sParam.extHeatSource[%s].DO.operationalData.maxRunTimeS",
        value_type=int,
        unit=_SECOND,
        message_id="sParam.extHeatSource[%s].DO",
    )
    ACTIVATION_COUNTER = Endpoint(
        path="sParam.extHeatSource[%s].DO.operationalData.activationCounter",
        value_type=int,
        message_id="sParam.extHeatSource[%s].DO",
    )
    EXCESS_ENERGY_ACTIVE = Endpoint(
        path="sParam.extHeatSource[%s].values.consumingExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_OPERATING_TIME = Endpoint(
        path="sParam.extHeatSource[%s].operationalDataExcessEnergy.operationalTimeS",
        value_type=int,
        unit=_SECOND,
    )
    EXCESS_ENERGY_MAX_RUNTIME = Endpoint(
        path="sParam.extHeatSource[%s].operationalDataExcessEnergy.maxRunTimeS",
        value_type=int,
        unit=_SECOND,
    )
    EXCESS_ENERGY_ACTIVATION_COUNTER = Endpoint(
        path="sParam.extHeatSource[%s].operationalDataExcessEnergy.activationCounter",
        value_type=int,
    )
    USE_EXCESS_ENERGY = Endpoint(
        path="sParam.extHeatSource[%s].param.supportExcessEnergy",
        value_type=bool,
    )
    EXCESS_ENERGY_MIN_RUNTIME = Endpoint(
        path="sParam.extHeatSource[%s].param.minRunTimeExcessEnergy",
        value_type=int,
        unit=_MINUTE,
    )
    HAS_EMISSIONS = Endpoint(
        path="sParam.extHeatSource[%s].param.hasEmmission",
        value_type=bool,
    )


class SwitchValve(_SectionEnum, device_type=DeviceType.SWITCH_VALVE):
    """Endpoints of a switch valve."""

    POSITION = Endpoint(
        path="sParam.switchvalve[%s].values.actPosition",
        value_type=SwitchValvePosition,
    )


class PassiveCooling(_SectionEnum, device_type=DeviceType.PASSIVE_COOLING):
    """Endpoints of a passive cooling unit (one per heat pump)."""

    TEMPERATURE = Endpoint(
        path="sParam.passivecooling[%s].TempCoolPassive.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.passivecooling[%s].TempCoolPassive",
    )
    SWITCH_VALVE_POSITION = Endpoint(
        path="sParam.passivecooling[%s].SwitchValvePassiveCool.values.actPosition",
        value_type=SwitchValvePosition,
        message_id="sParam.passivecooling[%s].SwitchValvePassiveCool",
    )
    CIRCULATION_PUMP_SPEED = Endpoint(
        path="sParam.passivecooling[%s].Pump.values.setValueScaled",
        value_type=float,
        message_id="sParam.passivecooling[%s].Pump",
    )
    MIXER_TARGET_TEMPERATURE = Endpoint(
        path="sParam.passivecooling[%s].Mixer.values.setValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.passivecooling[%s].Mixer",
    )
    MIXER_FLOW_TEMPERATURE = Endpoint(
        path="sParam.passivecooling[%s].Mixer.flowTemp.values.actValue",
        value_type=float,
        unit=_CELSIUS,
        message_id="sParam.passivecooling[%s].Mixer.flowTemp",
    )
    MIXER_SETPOINT = Endpoint(
        path="sParam.passivecooling[%s].Mixer.mixer.values.setValueScaled",
        value_type=float,
        message_id="sParam.passivecooling[%s].Mixer.mixer",
    )


class Photovoltaics(_SectionEnum, device_type=DeviceType.PHOTOVOLTAICS):
    """Endpoints of the photovoltaics."""

    EXCESS_ENERGY_ACTIVE = Endpoint(
        path="sParam.photovoltaics.values.excessEnergyActive",
        value_type=bool,
    )
    EXCESS_POWER = Endpoint(
        path="sParam.photovoltaics.ElectricEnergyMeter.values.power",
        value_type=float,
        unit=_WATT,
        message_id="sParam.photovoltaics.ElectricEnergyMeter",
    )
    DAILY_EXCESS_ENERGY = Endpoint(
        path="sParam.photovoltaics.ElectricEnergyMeter.values.heatDay",
        value_type=float,
        unit=_JOULE,
        message_id="sParam.photovoltaics.ElectricEnergyMeter",
    )
    TOTAL_EXCESS_ENERGY = Endpoint(
        path="sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
        value_type=float,
        unit=_JOULE,
        message_id="sParam.photovoltaics.ElectricEnergyMeter",
    )


type Section = (
    BufferTank
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
