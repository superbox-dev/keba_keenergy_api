"""All API Constants."""

from enum import Enum
from enum import IntEnum
from typing import Final
from typing import NamedTuple
from typing import TypeAlias

API_DEFAULT_TIMEOUT: int = 10


class EndpointPath:
    """The endpoint paths."""

    READ_WRITE_VARS: Final[str] = "/var/readWriteVars"
    DEVICE_CONTROL: Final[str] = "/deviceControl"
    SW_UPDATE: Final[str] = "/swupdate"


class SystemOperatingMode(IntEnum):
    """Available system operating modes."""

    SETUP = -1
    STANDBY = 0
    SUMMER = 1
    AUTO_HEAT = 2
    AUTO_COOL = 3
    AUTO = 4


class HotWaterTankOperatingMode(IntEnum):
    """Available hot water tank operating modes."""

    OFF = 0
    AUTO = 1
    ON = 2
    HEAT_UP = 3


class HeatPumpState(IntEnum):
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


class HeatPumpOperatingMode(IntEnum):
    """Available heat pump operating modes."""

    OFF = 0
    ON = 1
    BACKUP = 2


class HeatPumpCompressorUseNightSpeed(IntEnum):
    """Available compressor use night speed stats."""

    OFF = 0
    ON = 1


class HeatPumpHasPassiveCooling(IntEnum):
    """Available has passive cooling stats."""

    OFF = 0
    ON = 1


class HeatCircuitHasRoomTemperature(IntEnum):
    """Available has room temperature stats."""

    OFF = 0
    ON = 1


class HeatCircuitHasRoomHumidity(IntEnum):
    """Available has room humidity stats."""

    OFF = 0
    ON = 1


class HeatCircuitOperatingMode(IntEnum):
    """Available heat circuit operating modes."""

    OFF = 0
    AUTO = 1
    DAY = 2
    NIGHT = 3
    HOLIDAY = 4
    PARTY = 5
    EXTERNAL = 8
    ROOM_CONTROL = 9


class HotWaterTankHeatRequest(IntEnum):
    """Available hot water tank heat request stats."""

    OFF = 0
    ON = 1


class HotWaterTankHotWaterFlow(IntEnum):
    """Available hot water tank hot water flow stats."""

    OFF = 0
    ON = 1


class HeatPumpHeatRequest(IntEnum):
    """Available heat pump heat request stats."""

    OFF = 0
    ON = 1


class HeatCircuitHeatRequest(IntEnum):
    """Available heat circuit heat request stats."""

    OFF = 0
    ON = 1
    FLOW_OFF = 2
    TEMPORARY_OFF = 3
    ROOM_OFF = 4
    OUTDOOR_OFF = 5
    INFLOW_OFF = 6


class HeatCircuitExternalCoolRequest(IntEnum):
    """Available heat circuit external cool request stats."""

    OFF = 0
    ON = 1


class HeatCircuitExternalHeatRequest(IntEnum):
    """Available heat circuit external heat request stats."""

    OFF = 0
    ON = 1


PAYLOAD_PREFIX: Final[str] = "APPL.CtrlAppl"


class EndpointProperties(NamedTuple):
    """Properties from an endpoint."""

    value: str
    value_type: type[float | int | str]
    read_only: bool = True
    human_readable: type[Enum] | None = None


class System(Enum):
    """The system endpoint settings."""

    HOT_WATER_TANK_NUMBERS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfHotWaterTanks",
        value_type=int,
    )
    HEAT_PUMP_NUMBERS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfHeatPumps",
        value_type=int,
    )
    HEAT_CIRCUIT_NUMBERS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfHeatingCircuits",
        value_type=int,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.outdoorTemp.values.actValue",
        value_type=float,
    )


class HotWaterTank(Enum):
    """The hot water tank endpoint settings."""

    CURRENT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].topTemp.values.actValue",
        value_type=float,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HotWaterTankOperatingMode,
    )
    STANDBY_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.reducedSetTempMax.value",
        value_type=float,
        read_only=False,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.normalSetTempMax.value",
        value_type=float,
        read_only=False,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].values.heatRequestTop",
        value_type=str,
        human_readable=HotWaterTankHeatRequest,
    )
    HOT_WATER_FLOW = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].FreshWater.freshWaterFlow.values.actValue",
        value_type=str,
        human_readable=HotWaterTankHotWaterFlow,
    )
    FRESH_WATER_MODULE_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].FreshWater.freshWaterTemp.values.actValue",
        value_type=float,
    )


class HeatPump(Enum):
    """The heat pump endpoint settings."""

    NAME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].param.name",
        value_type=str,
    )
    STATE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.heatpumpState",
        value_type=int,
        read_only=False,
        human_readable=HeatPumpState,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HeatPumpOperatingMode,
    )
    COMPRESSOR_USE_NIGHT_SPEED = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatPumpPowerCtrl.param.useDayNightSpeed",
        value_type=str,
        read_only=False,
        human_readable=HeatPumpCompressorUseNightSpeed,
    )
    COMPRESSOR_NIGHT_SPEED = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatPumpPowerCtrl.param.maxPowerScaledNight",
        value_type=float,
        read_only=False,
    )
    CIRCULATION_PUMP = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].CircPump.values.setValueScaled",
        value_type=float,
    )
    FLOW_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempHeatFlow.values.actValue",
        value_type=float,
    )
    RETURN_FLOW_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempHeatReflux.values.actValue",
        value_type=float,
    )
    SOURCE_INPUT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempSourceIn.values.actValue",
        value_type=float,
    )
    SOURCE_OUTPUT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempSourceOut.values.actValue",
        value_type=float,
    )
    COMPRESSOR_INPUT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempCompressorIn.values.actValue",
        value_type=float,
    )
    COMPRESSOR_OUTPUT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].TempCompressorOut.values.actValue",
        value_type=float,
    )
    COMPRESSOR = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].Compressor.values.setValueScaled",
        value_type=float,
    )
    HIGH_PRESSURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HighPressure.values.actValue",
        value_type=float,
    )
    LOW_PRESSURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].LowPressure.values.actValue",
        value_type=float,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.request",
        value_type=str,
        human_readable=HeatPumpHeatRequest,
    )
    COMPRESSOR_POWER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].ElectricEnergyMeter.values.power",
        value_type=float,
    )
    HEATING_POWER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatMeter.values.power",
        value_type=float,
    )
    HOT_WATER_POWER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HotWaterMeter.values.power",
        value_type=float,
    )
    COP = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.COP",
        value_type=float,
    )
    HEATING_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.heating.energy",
        value_type=float,
    )
    HEATING_ENERGY_CONSUMPTION = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.heating.electricalenergy",
        value_type=float,
    )
    HEATING_SPF = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatioHeat",
        value_type=float,
    )
    COOLING_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.cooling.energy",
        value_type=float,
    )
    COOLING_ENERGY_CONSUMPTION = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.cooling.electricalenergy",
        value_type=float,
    )
    COOLING_SPF = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatioCool",
        value_type=float,
    )
    HOT_WATER_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.domHotWater.energy",
        value_type=float,
    )
    HOT_WATER_ENERGY_CONSUMPTION = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.domHotWater.electricalenergy",
        value_type=float,
    )
    HOT_WATER_SPF = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatioDomHotWater",
        value_type=float,
    )
    TOTAL_THERMAL_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.energy",
        value_type=float,
    )
    TOTAL_ENERGY_CONSUMPTION = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].consumption.electricalenergy",
        value_type=float,
    )
    TOTAL_SPF = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sStatisticalData.heatpump[%s].EnergyEfficiencyRatio",
        value_type=float,
    )
    HAS_PASSIVE_COOLING = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.heatpump[%s].hasPassiveCooling",
        value_type=str,
        human_readable=HeatPumpHasPassiveCooling,
    )


class HeatCircuit(Enum):
    """The heat circuit endpoint settings."""

    NAME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.name",
        value_type=str,
    )
    HAS_ROOM_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasRoomTemp",
        value_type=str,
        human_readable=HeatCircuitHasRoomTemperature,
    )
    ROOM_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].tempRoom.values.actValue",
        value_type=float,
    )
    HAS_ROOM_HUMIDITY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.heatCircuit[%s].hasRoomHumidity",
        value_type=str,
        human_readable=HeatCircuitHasRoomHumidity,
    )
    ROOM_HUMIDITY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].humidityRoom.values.actValue",
        value_type=float,
    )
    DEW_POINT = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].dewPoint.values.actValue",
        value_type=float,
    )
    FLOW_TEMPERATURE_SETPOINT = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.flowSetTemp",
        value_type=float,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.setValue",
        value_type=float,
    )
    TARGET_TEMPERATURE_DAY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.normalSetTemp",
        value_type=float,
        read_only=False,
    )
    HEATING_LIMIT_DAY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdDayTemp.value",
        value_type=float,
    )
    TARGET_TEMPERATURE_NIGHT = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.reducedSetTemp",
        value_type=float,
        read_only=False,
    )
    HEATING_LIMIT_NIGHT = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdNightTemp.value",
        value_type=float,
    )
    TARGET_TEMPERATURE_AWAY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.holidaySetTemp",
        value_type=float,
        read_only=False,
    )
    TARGET_TEMPERATURE_OFFSET = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.offsetRoomTemp",
        value_type=float,
        read_only=False,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.heatRequest",
        value_type=int,
        human_readable=HeatCircuitHeatRequest,
    )
    EXTERNAL_COOL_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.external.coolRequest",
        value_type=str,
        human_readable=HeatCircuitExternalCoolRequest,
    )
    EXTERNAL_HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.external.heatRequest",
        value_type=str,
        human_readable=HeatCircuitExternalHeatRequest,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HeatCircuitOperatingMode,
    )


class SectionPrefix(str, Enum):
    """Section prefixes."""

    SYSTEM = "system"
    HOT_WATER_TANK = "hot_water_tank"
    HEAT_PUMP = "heat_pump"
    HEAT_CIRCUIT = "heat_circuit"


Section: TypeAlias = System | HotWaterTank | HeatPump | HeatCircuit
