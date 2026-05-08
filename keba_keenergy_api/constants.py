"""All API Constants."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from typing import Any
from typing import Final
from typing import TypeAlias

API_DEFAULT_TIMEOUT: int = 10


class EndpointPath:
    """The endpoint paths."""

    READ_WRITE_VARS: Final[str] = "/var/readWriteVars"
    READ_VAR_CHILDREN: Final[str] = "/var/readVarChildren"
    DEVICE_CONTROL: Final[str] = "/deviceControl"
    SW_UPDATE: Final[str] = "/swupdate"
    DATE_TIME: Final[str] = "/dateTime"


class BaseEnum(Enum):
    @classmethod
    def _missing_(cls, value: object) -> "BaseEnum":
        for member in cls:
            member_value = member._value_

            if isinstance(member_value, tuple):
                if value in member_value:
                    return member
            elif value == member_value:  # pragma: no cover
                return member

        msg: str = f"{value!r} is not a valid {cls.__name__}"
        raise ValueError(msg)


class BoolEnum(BaseEnum):
    """Bool enum for ON / OFF."""

    OFF = 0
    ON = 1


class SystemOperatingMode(BaseEnum):
    """Available system operating modes."""

    SETUP = -1
    STANDBY = 0
    SUMMER = 1
    AUTO_HEAT = 2
    AUTO_COOL = 3
    AUTO = 4


class BufferTankOperatingMode(BaseEnum):
    """Available buffer tank operating modes."""

    OFF = 0
    ON = 1
    HEAT_UP = 2


class BufferTankExcessEnergyMode(BaseEnum):
    """Available buffer tank excess energy modes."""

    OFF = 0
    HEATING = 1
    COOLING = 2


class HotWaterTankOperatingMode(BaseEnum):
    """Available hot water tank operating modes."""

    OFF = 0
    AUTO = 1
    ON = 2
    HEAT_UP = 3


class HotWaterTankExcessEnergyMode(BaseEnum):
    """Available  hot water tank excess energy modes."""

    OFF = 0
    HEATING = 1
    COOLING = 2


class HeatPumpState(BaseEnum):
    """Available heat pump stats."""

    STANDBY = 0
    FLOW = 1
    AUTO_HEAT = 2
    DEFROST = 3
    AUTO_COOL = 4
    INFLOW = 5
    PUMP_DOWN = 6
    SHUTDOWN = 7
    ERROR = 8


class HeatPumpSubState(BaseEnum):
    """Available heat pump sub stats."""

    NONE = 0
    OIL_PREHEATING = 1
    PUMP_PRE_RUN = (2, 3)
    RANDOM_DELAY = 4
    PRESSURE_EQUALIZATION = (5, 21, 22)
    DEFROST_PRE_FLOW = 6
    DEFROST_MONITORING = 7
    SNOW_DETECTION = 8
    FLUSHING = 9
    DEFROST_INITIALIZATION = 10
    PREHEAT_FLOW = 11
    DEFROST = 12
    DRIP = (13, 25)
    DEFROST_END = 14
    OPEN = (15, 16)
    COMPRESSOR_POST_RUN = 17
    PUMP_POST_RUN = 18
    LUBRICATION_PULSE = 19
    REDUCED_SPEED = (20, 26)
    COMPRESSOR_DELAY = 23
    DEFROST_VENTING = 24
    SWITCH_HEATING_COOLING = 27
    WAIT_FOR_COMPRESSOR = (28, 33)
    COMPRESSOR_STOP = 29
    BIVALENT_LOCK = 30
    LOCKED = 31
    RETURN_FLOW_OFF = 32
    MIXER_OPEN = 34
    ZONE_VALVE = 35
    ELECTRIC_DEFROST = 36
    COUNTERFLOW_VALVE = 37


class HeatPumpOperatingMode(BaseEnum):
    """Available heat pump operating modes."""

    OFF = 0
    ON = 1
    BACKUP = 2


class HeatCircuitMode(BaseEnum):
    """Available heat circuit modes."""

    HEATING = 0
    COOLING = 1
    HEATING_AND_COOLING = 2
    HEATING_AND_ACTIVE_COOLING = 3


class HeatCircuitExcessEnergyMode(BaseEnum):
    """Available heat circuit excess energy modes."""

    OFF = 0
    HEATING = 1
    COOLING = 2


class HeatCircuitOperatingMode(BaseEnum):
    """Available heat circuit operating modes."""

    OFF = 0
    AUTO = 1
    DAY = 2
    NIGHT = 3
    HOLIDAY = 4
    PARTY = 5
    EXTERNAL = 8
    ROOM_CONTROL = 9


class SolarCircuitPriority(BaseEnum):
    """Available solar circuit priority."""

    LOW = 14
    HIGH = 15


class HeatCircuitHeatRequest(BaseEnum):
    """Available heat circuit heat request stats."""

    OFF = 0
    ON = 1
    FLOW_OFF = 2
    TEMPORARY_OFF = 3
    ROOM_OFF = 4
    OUTDOOR_OFF = 5
    INFLOW_OFF = 6


class HeatCircuitCoolRequest(BaseEnum):
    """Available heat circuit cool request stats."""

    OFF = 0
    ON = 1
    FLOW_OFF = 2
    TEMPORARY_OFF = 3
    ROOM_OFF = 4
    OUTDOOR_OFF = 5
    INFLOW_OFF = 6


MIN_HEATING_CURVE_POINTS: Final[int] = 7
MAX_HEATING_CURVE_POINTS: Final[int] = 16


class SwitchValvePosition(BaseEnum):
    """Available switch valve positons."""

    NEUTRAL = 0
    OPEN = 1
    CLOSED = 2


class MixerSwitchValvePosition(BaseEnum):
    """Available mixer switch valve positons."""

    CLOSED = -1
    OFF = 0
    OPEN = 1


PAYLOAD_PREFIX: Final[str] = "APPL.CtrlAppl"


@dataclass
class Endpoint:
    value: str
    value_type: type[Any]
    human_readable: type[Enum] | None = None
    normalize: Callable[[Any], Any] = lambda x: x
    quantity: int = 1
    read_only: bool = True

    def __post_init__(self) -> None:
        if ".param." in self.value:
            self.read_only = False


@dataclass
class FloatEndpoint(Endpoint):
    value_type: type[float] = float
    decimals: int = 2


@dataclass
class IntegerEndpoint(Endpoint):
    value_type: type[int] = int


@dataclass
class StringEndpoint(Endpoint):
    value_type: type[str] = str


@dataclass
class SolarCircuitPriority1Before2StringEndpoint(StringEndpoint):
    @staticmethod
    def helper(modes: list[int | None]) -> dict["Section", Any]:
        """Add extra calls."""
        # The switch in the Web HMI calls to API endpoints
        # If priority_1 is on then priority is 14 and if off the priority is 15

        priorities: list[int | None] = list(
            chain.from_iterable(
                (
                    (SolarCircuitPriority.LOW.value if m == 1 else SolarCircuitPriority.HIGH.value if m == 0 else None),
                    None,
                )
                for m in modes
            ),
        )

        return {SolarCircuit._PRIORITY: priorities}  # noqa: SLF001


class System(Enum):
    """The system endpoint settings."""

    BUFFER_TANK_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfBuffers",
    )
    HOT_WATER_TANK_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfHotWaterTanks",
    )
    HEAT_PUMP_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfHeatPumps",
    )
    HEAT_CIRCUIT_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfHeatingCircuits",
    )
    SOLAR_CIRCUIT_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfSolarCircuits",
    )
    EXTERNAL_HEAT_SOURCE_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfExtHeatSources",
    )
    SWITCH_VALVE_NUMBERS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfSwitchValves",
    )
    HAS_PHOTOVOLTAICS = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.hasPhotovoltaics",
        human_readable=BoolEnum,
    )
    HAS_OUTDOOR_TEMPERATURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.hasOutdoorTemp",
        human_readable=BoolEnum,
    )
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.param.operatingMode",
        human_readable=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.outdoorTemp.values.actValue",
    )
    CPU_USAGE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sProcData.globalCpuTimePercent",
    )
    WEBVIEW_CPU_USAGE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sProcData.processStatus[0].cpuTimePercent",
    )
    WEBSERVER_CPU_USAGE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sProcData.processStatus[1].cpuTimePercent",
    )
    CONTROL_CPU_USAGE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sProcData.processStatus[2].cpuTimePercent",
    )
    RAM_USAGE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sProcData.RAMstatus.tmpfs",
    )
    FREE_RAM = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sProcData.totFreeRAM",
    )


class BufferTank(Enum):
    """The buffer tank endpoint settings."""

    NAME = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.name",
    )
    CURRENT_TOP_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].topTemp.values.actValue",
    )
    CURRENT_BOTTOM_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].midTemp.values.actValue",
    )
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.operatingMode",
        human_readable=BufferTankOperatingMode,
    )
    STANDBY_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.backupTemp",
    )
    TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.setTemp",
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.excessEnergyTemp.value",
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.excessEnergyTemp.hyst",
    )
    OUTDOOR_TEMPERATURE_EXCESS_ENERGY_LIMIT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.thresholdOutTempExcessEnergy.value",
    )
    USE_EXCESS_ENERGY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.useExcessEnergy",
        human_readable=BoolEnum,
    )
    EXCESS_ENERGY_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.useExcessEnergy",
        human_readable=BufferTankExcessEnergyMode,
    )
    HEAT_REQUEST = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.heatRequestTop",
        human_readable=BoolEnum,
    )
    COOL_REQUEST = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.coolRequestBot",
        human_readable=BoolEnum,
    )


class HotWaterTank(Enum):
    """The hot water tank endpoint settings."""

    NAME = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.name",
    )
    CURRENT_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].topTemp.values.actValue",
    )
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.operatingMode",
        human_readable=HotWaterTankOperatingMode,
    )
    STANDBY_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.reducedSetTempMax.value",
    )
    TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.normalSetTempMax.value",
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.excessEnergyTemp.value",
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.excessEnergyTemp.hyst",
    )
    USE_EXCESS_ENERGY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.useExcessEnergy",
        human_readable=BoolEnum,
    )
    EXCESS_ENERGY_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].values.useExcessEnergy",
        human_readable=HotWaterTankExcessEnergyMode,
    )
    HEAT_REQUEST = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].values.heatRequestTop",
        human_readable=BoolEnum,
    )
    HAS_FRESH_WATER_MODULE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.hotWaterTank[%s].hasFreshWaterModule",
        human_readable=BoolEnum,
    )
    FRESH_WATER_FLOW = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].FreshWater.freshWaterFlow.values.actValue",
        human_readable=BoolEnum,
    )
    FRESH_WATER_MODULE_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].FreshWater.freshWaterTemp.values.actValue",
    )
    FRESH_WATER_MODULE_PUMP_SPEED = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].FreshWater.freshWaterPump.values.setValueScaled",
        decimals=4,
    )
    CIRCULATION_RETURN_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].circTemp.values.actValue",
    )
    CIRCULATION_PUMP_STATE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].circPump.pump.values.setValueB",
        human_readable=BoolEnum,
    )


class HeatPump(Enum):
    """The heat pump endpoint settings."""

    NAME = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].param.name",
    )
    STATE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.heatpumpState",
        human_readable=HeatPumpState,
    )
    SUBSTATE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.heatpumpSubState",
        human_readable=HeatPumpSubState,
    )
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].param.operatingMode",
        human_readable=HeatPumpOperatingMode,
    )
    COMPRESSOR_USE_NIGHT_SPEED = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatPumpPowerCtrl.param.useDayNightSpeed",
        human_readable=BoolEnum,
    )
    COMPRESSOR_NIGHT_SPEED = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatPumpPowerCtrl.param.maxPowerScaledNight",
    )
    CIRCULATION_PUMP_SPEED = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].CircPump.values.setValueScaled",
        decimals=4,
    )
    SOURCE_PUMP_SPEED = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].Source.values.setValueScaled",
        decimals=4,
    )
    FLOW_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempHeatFlow.values.actValue",
    )
    RETURN_FLOW_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempHeatReflux.values.actValue",
    )
    SOURCE_INPUT_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempSourceIn.values.actValue",
    )
    SOURCE_OUTPUT_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempSourceOut.values.actValue",
    )
    COMPRESSOR_INPUT_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempCompressorIn.values.actValue",
    )
    COMPRESSOR_OUTPUT_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempCompressorOut.values.actValue",
    )
    COMPRESSOR = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].Compressor.values.setValueScaled",
        decimals=4,
    )
    CONDENSER_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.tempCond",
    )
    VAPORIZER_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.tempVap",
    )
    TARGET_OVERHEATING = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.setOH",
    )
    CURRENT_OVERHEATING = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.actOH",
    )
    EXPANSION_VALVE_POSITION = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.stepperPos",
    )
    HIGH_PRESSURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HighPressure.values.actValue",
    )
    LOW_PRESSURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].LowPressure.values.actValue",
    )
    HEAT_REQUEST = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.request",
        human_readable=BoolEnum,
    )
    CONSUMING_EXCESS_ENERGY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.consumingExcessEnergy",
        human_readable=BoolEnum,
    )
    EXCESS_ENERGY_OPERATING_TIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalDataExcessEnergy.operationalTimeS",
    )
    EXCESS_ENERGY_MAX_RUNTIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalDataExcessEnergy.maxRunTimeS",
    )
    EXCESS_ENERGY_ACTIVATION_COUNTER = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalDataExcessEnergy.activationCounter",
    )
    # TOTAL_HEATING_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatMeter.values.accumulatedHeat",
    # )
    # DAILY_HEATING_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatMeter.values.heatDay",
    # )
    HEATING_POWER = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatMeter.values.power",
    )
    HEATING_MASS_FLOW_RATE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatMeter.values.massFlow",
    )
    # TOTAL_COOLING_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].CoolMeter.values.accumulatedHeat",
    # )
    # DAILY_COOLING_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].CoolMeter.values.heatDay",
    # )
    # COOLING_POWER = FloatEndpoint(
    #     value_type=float,
    # )
    COOLING_MASS_FLOW_RATE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].CoolMeter.values.massFlow",
    )
    # TOTAL_HOT_WATER_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HotWaterMeter.values.accumulatedHeat",
    # )
    # DAILY_HOT_WATER_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HotWaterMeter.values.heatDay",
    # )
    HOT_WATER_POWER = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HotWaterMeter.values.power",
    )
    HOT_WATER_MASS_FLOW_RATE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HotWaterMeter.values.massFlow",
    )
    # TOTAL_COMPRESSOR_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].ElectricEnergyMeter.values.accumulatedHeat",
    # )
    # DAILY_COMPRESSOR_ENERGY = FloatEndpoint(
    #     f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].ElectricEnergyMeter.values.heatDay",
    # )
    COMPRESSOR_POWER = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].ElectricEnergyMeter.values.power",
    )
    COP = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.COP",
    )
    HEATING_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.heating.energy",
    )
    HEATING_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.heating.electricalenergy",
    )
    HEATING_SPF = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatioHeat",
    )
    COOLING_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.cooling.energy",
    )
    COOLING_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.cooling.electricalenergy",
    )
    COOLING_SPF = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatioCool",
    )
    HOT_WATER_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.domHotWater.energy",
    )
    HOT_WATER_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.domHotWater.electricalenergy",
    )
    HOT_WATER_SPF = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatioDomHotWater",
    )
    TOTAL_THERMAL_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.energy",
    )
    TOTAL_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.electricalenergy",
    )
    EXCESS_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.consumedExcessEnergy",
    )
    HEATING_EXCESS_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.heating.consumedExcessEnergy",
    )
    COOLING_EXCESS_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.cooling.consumedExcessEnergy",
    )
    HOT_WATER_EXCESS_ENERGY_CONSUMPTION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.domHotWater.consumedExcessEnergy",
    )
    TOTAL_SPF = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatio",
    )
    HAS_ACTIVE_COOLING = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].hasActiveCooling",
        human_readable=BoolEnum,
    )
    HAS_PASSIVE_COOLING = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].hasPassiveCooling",
        human_readable=BoolEnum,
    )
    OPERATING_TIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalData.operationalTimeS",
    )
    MAX_RUNTIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalData.maxRunTimeS",
    )
    ACTIVATION_COUNTER = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalData.activationCounter",
    )
    HAS_COMPRESSOR_FAILURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].FailureCompressor.values.actValue",
        human_readable=BoolEnum,
    )
    HAS_SOURCE_FAILURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].FailureSource.values.actValue",
        human_readable=BoolEnum,
    )
    HAS_SOURCE_ACTUATOR_FAILURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].FailureActuatorSource.values.actValue",
        human_readable=BoolEnum,
    )
    HAS_THREE_PHASE_FAILURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].FailureThreePhase.values.actValue",
        human_readable=BoolEnum,
    )
    HAS_SOURCE_PRESSURE_FAILURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].FailureSrcPressure.values.actValue",
        human_readable=BoolEnum,
    )
    HAS_VFD_FAILURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].FailureVFD.values.actValue",
        human_readable=BoolEnum,
    )
    ELECTRIC_ENERGY_METER_TYPE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].ElectricEnergyMeter.type",
    )
    HEAT_METER_TYPE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].HeatMeter.type",
    )
    COOL_METER_TYPE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].CoolMeter.type",
    )
    HOT_WATER_METER_TYPE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].HotWaterMeter.type",
    )


class HeatCircuit(Enum):
    """The heat circuit endpoint settings."""

    NAME = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.name",
    )
    MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].type",
        human_readable=HeatCircuitMode,
    )
    HAS_ROOM_TEMPERATURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasRoomTemp",
        human_readable=BoolEnum,
    )
    ROOM_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].tempRoom.values.actValue",
    )
    HAS_ROOM_HUMIDITY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasRoomHumidity",
        human_readable=BoolEnum,
    )
    ROOM_HUMIDITY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].humidityRoom.values.actValue",
    )
    DEW_POINT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].dewPoint.values.actValue",
    )
    FLOW_TEMPERATURE_SETPOINT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.flowSetTemp",
    )
    HAS_MIXER = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasMixer",
        human_readable=BoolEnum,
    )
    MIXER_FLOW_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].heatCircuitMixer.flowTemp.values.actValue",
    )
    MIXER_RETURN_FLOW_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].heatCircuitMixer.refluxTemp.values.actValue",
    )
    MIXER_POSITION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].heatCircuitMixer.mixer.values.setValueScaled",
        human_readable=MixerSwitchValvePosition,
        normalize=lambda v: (v >= 1) - (v <= -1),
    )

    PUMP_STATE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].pump.values.setValueB",
        human_readable=BoolEnum,
    )
    HAS_RETURN_FLOW_TEMPERATURE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasRefluxTemp",
        human_readable=BoolEnum,
    )
    RETURN_FLOW_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].tempReflux.values.actValue",
    )
    TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.setValue",
    )
    USE_EXCESS_ENERGY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergy.useExcessEnergy",
        human_readable=BoolEnum,
    )
    EXCESS_ENERGY_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.useExcessEnergy",
        human_readable=HeatCircuitExcessEnergyMode,
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergyTemp.value",
    )
    EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergyTemp.hyst",
    )
    EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergyTempCool.value",
    )
    EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE_HYSTERESIS = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergyTempCool.hyst",
    )
    SELECTED_TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.selectedSetTemp",
    )
    TARGET_TEMPERATURE_DAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.normalSetTemp",
    )
    TARGET_COOLING_TEMPERATURE_DAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.normalCoolSetTemp",
    )
    HEATING_LIMIT_DAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdDayTemp.value",
    )
    COOLING_LIMIT_DAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdDayCoolTemp.value",
    )
    EXCESS_ENERGY_HEATING_LIMIT_DAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergy.thresholdDayTemp",
    )
    EXCESS_ENERGY_COOLING_LIMIT_DAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergy.thresholdDayCoolTemp",
    )
    TARGET_TEMPERATURE_NIGHT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.reducedSetTemp",
    )
    TARGET_COOLING_TEMPERATURE_NIGHT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.reducedCoolSetTemp",
    )
    HEATING_LIMIT_NIGHT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdNightTemp.value",
    )
    COOLING_LIMIT_NIGHT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdNightCoolTemp.value",
    )
    EXCESS_ENERGY_HEATING_LIMIT_NIGHT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergy.thresholdNightTemp",
    )
    EXCESS_ENERGY_COOLING_LIMIT_NIGHT = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.excessEnergy.thresholdNightCoolTemp",
    )
    TARGET_TEMPERATURE_AWAY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.holidaySetTemp",
    )
    TARGET_TEMPERATURE_OFFSET = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.offsetRoomTemp",
    )
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.operatingMode",
        human_readable=HeatCircuitOperatingMode,
    )
    HEAT_REQUEST = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.heatRequest",
        human_readable=HeatCircuitHeatRequest,
    )
    COOL_REQUEST = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.coolRequest",
        human_readable=HeatCircuitCoolRequest,
    )
    AWAY_START_DATE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.holiday.start",
    )
    AWAY_END_DATE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.holiday.stop",
    )
    HEATING_CURVE_OFFSET = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.heatCurveOffset",
    )
    COOLING_CURVE_OFFSET = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.coolCurveOffset",
    )
    HEATING_CURVE_SLOPE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.heatCurveGradient",
    )
    COOLING_CURVE_SLOPE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.coolCurveGradient",
    )
    USE_HEATING_CURVE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.enableHeatCurveLinTab",
        human_readable=BoolEnum,
    )
    HEATING_CURVE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.linTab.fileName",
    )
    COOLING_CURVE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.coollinTab.fileName",
    )
    HAS_PUMP = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasPump",
        human_readable=BoolEnum,
    )
    HAS_VAR_SPEED_PUMP = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasVarSpeedPump",
        human_readable=BoolEnum,
    )
    PUMP_SPEED = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].pumpAO.values.setValueScaled",
        decimals=4,
    )


class LineTablePool(Enum):
    """Pool of heating curve points.

    This is not a real section and read and write are only allowed with `client.heat_circuit.get_heating_curves()`
    and `client.heat_circuit.set_heating_curves()`.

    """

    HEATING_CURVE_NAME = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.linTabPool[%s].name",
    )
    HEATING_CURVE_POINTS = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.linTabPool[%s].noOfPoints",
        read_only=False,
    )
    HEATING_CURVE_POINT_X = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.linTabPool[%s].points[%s].x",
        read_only=False,
    )
    HEATING_CURVE_POINT_Y = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.linTabPool[%s].points[%s].y",
        read_only=False,
    )
    SAVE_HEATING_CURVE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.linTabPool[%s].verCnt",
        read_only=False,
    )


class SolarCircuit(Enum):
    """The solar circuit endpoint settings."""

    NAME = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].param.name",
    )
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].param.operatingMode",
        human_readable=BoolEnum,
    )
    SOURCE_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].collectorTemp.values.actValue",
    )
    PUMP_1 = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].values.pump1",
    )
    PUMP_2 = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].values.pump2",
    )
    CURRENT_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].referenceTemp.values.actValue",
        quantity=2,
    )
    TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].param.setTempMax.value",
        quantity=2,
    )
    HEAT_REQUEST = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].values.heatRequest",
        human_readable=BoolEnum,
        quantity=2,
    )
    HEATING_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].heatMeter.values.accumulatedHeat",
    )
    DAILY_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].heatMeter.values.heatDay",
    )
    ACTUAL_POWER = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].heatMeter.values.power",
    )
    PRIORITY_1_BEFORE_2 = SolarCircuitPriority1Before2StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.hmiRetainData.consumer1PrioritySolar[%s]",
        human_readable=BoolEnum,
        read_only=False,
    )
    _PRIORITY = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].param.priority",
        quantity=2,
    )


class ExternalHeatSource(Enum):
    OPERATING_MODE = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].param.operatingMode",
        human_readable=BoolEnum,
    )
    TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].values.setTemp",
    )
    HEAT_REQUEST = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.values.setValueB",
        human_readable=BoolEnum,
    )
    OPERATING_TIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.operationalData.operationalTimeS",
    )
    MAX_RUNTIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.operationalData.maxRunTimeS",
    )
    ACTIVATION_COUNTER = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.operationalData.activationCounter",
    )
    CONSUMING_EXCESS_ENERGY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].values.consumingExcessEnergy",
        human_readable=BoolEnum,
    )
    EXCESS_ENERGY_OPERATING_TIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].operationalDataExcessEnergy.operationalTimeS",
    )
    EXCESS_ENERGY_MAX_RUNTIME = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].operationalDataExcessEnergy.maxRunTimeS",
    )
    EXCESS_ENERGY_ACTIVATION_COUNTER = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].operationalDataExcessEnergy.activationCounter",
    )
    USE_EXCESS_ENERGY = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].param.supportExcessEnergy",
        human_readable=BoolEnum,
    )
    MIN_RUNTIME_EXCESS_ENERGY = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].param.minRunTimeExcessEnergy",
        value_type=int,
    )


class SwitchValve(Enum):
    POSITION = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.switchvalve[%s].values.actPosition",
        human_readable=SwitchValvePosition,
    )


class PassiveCooling(Enum):
    TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.passivecooling[%s].TempCoolPassive.values.actValue",
    )
    SWITCH_VALVE_POSITION = IntegerEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.passivecooling[%s].SwitchValvePassiveCool.values.actPosition",
        human_readable=SwitchValvePosition,
    )
    CIRCULATION_PUMP_SPEED = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.passivecooling[%s].Pump.values.setValueScaled",
        decimals=4,
    )
    MIXER_TARGET_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.passivecooling[%s].Mixer.values.setValue",
    )
    MIXER_FLOW_TEMPERATURE = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.passivecooling[%s].Mixer.flowTemp.values.actValue",
    )
    MIXER_POSITION = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.passivecooling[%s].Mixer.mixer.values.setValueScaled",
        human_readable=MixerSwitchValvePosition,
        normalize=lambda v: (v >= 1) - (v <= -1),
    )


class Photovoltaics(Enum):
    EXCESS_ENERGY_ACTIVE = StringEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.values.excessEnergyActive",
        human_readable=BoolEnum,
    )
    EXCESS_POWER = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.ElectricEnergyMeter.values.power",
    )
    DAILY_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.ElectricEnergyMeter.values.heatDay",
    )
    TOTAL_ENERGY = FloatEndpoint(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
    )


class SectionPrefix(str, Enum):
    """Section prefixes."""

    SYSTEM = "system"
    BUFFER_TANK = "buffer_tank"
    HOT_WATER_TANK = "hot_water_tank"
    HEAT_PUMP = "heat_pump"
    HEAT_CIRCUIT = "heat_circuit"
    SOLAR_CIRCUIT = "solar_circuit"
    EXTERNAL_HEAT_SOURCE = "external_heat_source"
    SWITCH_VALVE = "switch_valve"
    PASSIVE_COOLING = "passive_cooling"
    PHOTOVOLTAICS = "photovoltaics"


Section: TypeAlias = (
    System
    | BufferTank
    | HotWaterTank
    | HeatPump
    | HeatCircuit
    | SolarCircuit
    | ExternalHeatSource
    | SwitchValve
    | PassiveCooling
    | Photovoltaics
)
