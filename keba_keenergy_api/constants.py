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


class HeatPumpOperatingMode(IntEnum):
    """Available heat pump operating modes."""

    OFF = 0
    ON = 1
    BACKUP = 2


class HeatCircuitOperatingMode(IntEnum):
    """Available heat circuit operating modes."""

    OFF = 0
    AUTO = 1
    DAY = 2
    NIGHT = 3
    HOLIDAY = 4
    PARTY = 5
    EXTERN = 8


class HotWaterTankHeatRequest(str, Enum):
    """Available hot water tank heat request stats."""

    OFF = "false"
    ON = "true"


class HeatPumpHeatRequest(str, Enum):
    """Available heat pump heat request stats."""

    OFF = "false"
    ON = "true"


class HeatCircuitHeatRequest(str, Enum):
    """Available heat circuit heat request stats."""

    OFF = "0"
    ON = "1"
    TEMPORARY_OFF = "3"
    OUTDOOR_TEMPERATURE_OFF = "5"


class HeatCircuitExternalCoolRequest(str, Enum):
    """Available heat circuit external cool request stats."""

    OFF = "false"
    ON = "true"


class HeatCircuitExternalHeatRequest(str, Enum):
    """Available heat circuit external heat request stats."""

    OFF = "false"
    ON = "true"


SYSTEM_PREFIX: Final[str] = "APPL.CtrlAppl.sParam"
HOT_WATER_TANK_PREFIX: Final[str] = f"{SYSTEM_PREFIX}.hotWaterTank"
HEAT_PUMP_PREFIX: Final[str] = f"{SYSTEM_PREFIX}.heatpump"
HEAT_CIRCUIT_PREFIX: Final[str] = f"{SYSTEM_PREFIX}.heatCircuit"


class EndpointProperties(NamedTuple):
    """Properties from an endpoint."""

    value: str
    value_type: type[float | int | str]
    read_only: bool = True
    human_readable: type[Enum] | None = None


class System(Enum):
    """The system endpoint settings."""

    HOT_WATER_TANK_NUMBERS = EndpointProperties(
        "options.systemNumberOfHotWaterTanks",
        value_type=int,
    )
    HEAT_PUMP_NUMBERS = EndpointProperties(
        "options.systemNumberOfHeatPumps",
        value_type=int,
    )
    HEAT_CIRCUIT_NUMBERS = EndpointProperties(
        "options.systemNumberOfHeatingCircuits",
        value_type=int,
    )
    OPERATING_MODE = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE = EndpointProperties(
        "outdoorTemp.values.actValue",
        value_type=float,
    )


class HotWaterTank(Enum):
    """The hot water tank endpoint settings."""

    TEMPERATURE = EndpointProperties("topTemp.values.actValue", float)
    OPERATING_MODE = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HotWaterTankOperatingMode,
    )
    MIN_TEMPERATURE = EndpointProperties(
        "param.reducedSetTempMax.value",
        float,
        read_only=False,
    )
    MAX_TEMPERATURE = EndpointProperties(
        "param.normalSetTempMax.value",
        float,
        read_only=False,
    )
    HEAT_REQUEST = EndpointProperties(
        "values.heatRequestTop",
        value_type=str,
        human_readable=HotWaterTankHeatRequest,
    )


class HeatPump(Enum):
    """The heat pump endpoint settings."""

    NAME = EndpointProperties("param.name", value_type=str)
    STATE = EndpointProperties(
        "values.heatpumpState",
        value_type=int,
        read_only=False,
        human_readable=HeatPumpState,
    )
    OPERATING_MODE = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HeatPumpOperatingMode,
    )
    CIRCULATION_PUMP = EndpointProperties(
        "CircPump.values.setValueScaled",
        value_type=float,
    )
    INFLOW_TEMPERATURE = EndpointProperties(
        "TempHeatFlow.values.actValue",
        value_type=float,
    )
    REFLUX_TEMPERATURE = EndpointProperties(
        "TempHeatReflux.values.actValue",
        value_type=float,
    )
    SOURCE_INPUT_TEMPERATURE = EndpointProperties(
        "TempSourceIn.values.actValue",
        value_type=float,
    )
    SOURCE_OUTPUT_TEMPERATURE = EndpointProperties(
        "TempSourceOut.values.actValue",
        value_type=float,
    )
    COMPRESSOR_INPUT_TEMPERATURE = EndpointProperties(
        "TempCompressorIn.values.actValue",
        value_type=float,
    )
    COMPRESSOR_OUTPUT_TEMPERATURE = EndpointProperties(
        "TempCompressorOut.values.actValue",
        value_type=float,
    )
    COMPRESSOR = EndpointProperties(
        "Compressor.values.setValueScaled",
        value_type=float,
    )
    HIGH_PRESSURE = EndpointProperties(
        "HighPressure.values.actValue",
        value_type=float,
    )
    LOW_PRESSURE = EndpointProperties(
        "LowPressure.values.actValue",
        value_type=float,
    )
    HEAT_REQUEST = EndpointProperties(
        "values.request",
        value_type=str,
        human_readable=HeatPumpHeatRequest,
    )


class HeatCircuit(Enum):
    """The heat circuit endpoint settings."""

    NAME = EndpointProperties(
        "param.name",
        value_type=str,
    )
    TEMPERATURE = EndpointProperties(
        "values.setValue",
        value_type=float,
    )
    DAY_TEMPERATURE = EndpointProperties(
        "param.normalSetTemp",
        value_type=float,
        read_only=False,
    )
    DAY_TEMPERATURE_THRESHOLD = EndpointProperties(
        "param.thresholdDayTemp.value",
        value_type=float,
    )
    NIGHT_TEMPERATURE = EndpointProperties(
        "param.reducedSetTemp",
        value_type=float,
        read_only=False,
    )
    NIGHT_TEMPERATURE_THRESHOLD = EndpointProperties(
        "param.thresholdNightTemp.value",
        value_type=float,
    )
    HOLIDAY_TEMPERATURE = EndpointProperties(
        "param.holidaySetTemp",
        value_type=float,
        read_only=False,
    )
    TEMPERATURE_OFFSET = EndpointProperties(
        "param.offsetRoomTemp",
        value_type=float,
        read_only=False,
    )
    HEAT_REQUEST = EndpointProperties(
        "values.heatRequest",
        value_type=str,
        human_readable=HeatCircuitHeatRequest,
    )
    EXTERNAL_COOL_REQUEST = EndpointProperties(
        "param.external.coolRequest",
        value_type=str,
        human_readable=HeatCircuitExternalCoolRequest,
    )
    EXTERNAL_HEAT_REQUEST = EndpointProperties(
        "param.external.heatRequest",
        value_type=str,
        human_readable=HeatCircuitExternalHeatRequest,
    )
    OPERATING_MODE = EndpointProperties(
        "param.operatingMode",
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
