"""All API Constants."""

from dataclasses import dataclass
from enum import Enum
from typing import Final
from typing import TypeAlias

API_DEFAULT_TIMEOUT: int = 10


class EndpointPath:
    """The endpoint paths."""

    READ_WRITE_VARS: Final[str] = "/var/readWriteVars"
    DEVICE_CONTROL: Final[str] = "/deviceControl"
    SW_UPDATE: Final[str] = "/swupdate"


class BaseEnum(Enum):
    @classmethod
    def from_value(cls, value: int) -> "BaseEnum":
        """Get name from value."""
        for state in cls:
            if isinstance(state.value, tuple):
                if value in state.value:
                    return state
            elif state.value == value:
                return state

        raise ValueError


class SystemOperatingMode(BaseEnum):
    """Available system operating modes."""

    SETUP = -1
    STANDBY = 0
    SUMMER = 1
    AUTO_HEAT = 2
    AUTO_COOL = 3
    AUTO = 4


class SystemHasPhotovoltaics(BaseEnum):
    """Available has photovoltaics stats."""

    OFF = 0
    ON = 1


class BufferTankOperatingMode(BaseEnum):
    """Available buffer tank operating modes."""

    OFF = 0
    ON = 1
    HEAT_UP = 2


class HotWaterTankOperatingMode(BaseEnum):
    """Available hot water tank operating modes."""

    OFF = 0
    AUTO = 1
    ON = 2
    HEAT_UP = 3


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


class HeatPumpCompressorUseNightSpeed(BaseEnum):
    """Available compressor use night speed stats."""

    OFF = 0
    ON = 1


class HeatPumpHasPassiveCooling(BaseEnum):
    """Available has passive cooling stats."""

    OFF = 0
    ON = 1


class HeatCircuitHasRoomTemperature(BaseEnum):
    """Available has room temperature stats."""

    OFF = 0
    ON = 1


class HeatCircuitHasRoomHumidity(BaseEnum):
    """Available has room humidity stats."""

    OFF = 0
    ON = 1


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


class SolarCircuitOperatingMode(BaseEnum):
    """Available solar circuit operating modes."""

    OFF = 0
    ON = 1


class SolarCircuitHeatRequest(BaseEnum):
    """Available solar circuit heat request stats."""

    OFF = 0
    ON = 1


class BufferTankHeatRequest(BaseEnum):
    """Available buffer tank heat request stats."""

    OFF = 0
    ON = 1


class BufferTankCoolRequest(BaseEnum):
    """Available buffer tank cool request stats."""

    OFF = 0
    ON = 1


class HotWaterTankHeatRequest(BaseEnum):
    """Available hot water tank heat request stats."""

    OFF = 0
    ON = 1


class HotWaterTankHotWaterFlow(BaseEnum):
    """Available hot water tank hot water flow stats."""

    OFF = 0
    ON = 1


class HeatPumpHeatRequest(BaseEnum):
    """Available heat pump heat request stats."""

    OFF = 0
    ON = 1


class HeatCircuitCoolRequest(BaseEnum):
    """Available heat circuit cool request stats."""

    OFF = 0
    ON = 1
    FLOW_OFF = 2
    TEMPORARY_OFF = 3
    ROOM_OFF = 4
    OUTDOOR_OFF = 5
    INFLOW_OFF = 6


class HeatCircuitHeatRequest(BaseEnum):
    """Available heat circuit heat request stats."""

    OFF = 0
    ON = 1
    FLOW_OFF = 2
    TEMPORARY_OFF = 3
    ROOM_OFF = 4
    OUTDOOR_OFF = 5
    INFLOW_OFF = 6


class ExternalHeatSourceOperatingMode(BaseEnum):
    """Available external heat source operating modes."""

    OFF = 0
    ON = 1


class ExternalHeatSourceHeatRequest(BaseEnum):
    """Available external heat source heat request stats."""

    OFF = 0
    ON = 1


PAYLOAD_PREFIX: Final[str] = "APPL.CtrlAppl"


@dataclass
class EndpointProperties:
    """Properties from an endpoint."""

    value: str
    value_type: type[float | int | str]
    human_readable: type[Enum] | None = None
    quantity: int = 1

    @property
    def read_only(self) -> bool:
        """Set endpoint to read only."""
        return ".param." not in self.value


class System(Enum):
    """The system endpoint settings."""

    BUFFER_TANK_NUMBERS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfBuffers",
        value_type=int,
    )
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
    SOLAR_CIRCUIT_NUMBERS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfSolarCircuits",
        value_type=int,
    )
    EXTERNAL_HEAT_SOURCE_NUMBERS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.systemNumberOfExtHeatSources",
        value_type=int,
    )
    HAS_PHOTOVOLTAICS = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.options.hasPhotovoltaics",
        value_type=str,
        human_readable=SystemHasPhotovoltaics,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.param.operatingMode",
        value_type=int,
        human_readable=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.outdoorTemp.values.actValue",
        value_type=float,
    )
    CPU_USAGE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sProcData.globalCpuTimePercent",
        value_type=float,
    )
    WEBVIEW_CPU_USAGE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sProcData.processStatus[0].cpuTimePercent",
        value_type=float,
    )
    WEBSERVER_CPU_USAGE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sProcData.processStatus[1].cpuTimePercent",
        value_type=float,
    )
    CONTROL_CPU_USAGE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sProcData.processStatus[2].cpuTimePercent",
        value_type=float,
    )
    RAM_USAGE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sProcData.RAMstatus.tmpfs",
        value_type=int,
    )
    FREE_RAM = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sProcData.totFreeRAM",
        value_type=int,
    )


class BufferTank(Enum):
    """The buffer tank endpoint settings."""

    NAME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.name",
        value_type=str,
    )
    CURRENT_TOP_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].topTemp.values.actValue",
        value_type=float,
    )
    CURRENT_BOTTOM_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].midTemp.values.actValue",
        value_type=float,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.operatingMode",
        value_type=int,
        human_readable=BufferTankOperatingMode,
    )
    STANDBY_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].param.backupTemp",
        value_type=float,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.setTemp",
        value_type=float,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.heatRequestTop",
        value_type=str,
        human_readable=BufferTankHeatRequest,
    )
    COOL_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.bufferTank[%s].values.coolRequestBot",
        value_type=str,
        human_readable=BufferTankCoolRequest,
    )


class HotWaterTank(Enum):
    """The hot water tank endpoint settings."""

    NAME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.name",
        value_type=str,
    )
    CURRENT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].topTemp.values.actValue",
        value_type=float,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.operatingMode",
        value_type=int,
        human_readable=HotWaterTankOperatingMode,
    )
    STANDBY_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.reducedSetTempMax.value",
        value_type=float,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.hotWaterTank[%s].param.normalSetTempMax.value",
        value_type=float,
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
        human_readable=HeatPumpState,
    )
    SUBSTATE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].values.heatpumpSubState",
        value_type=int,
        human_readable=HeatPumpSubState,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].param.operatingMode",
        value_type=int,
        human_readable=HeatPumpOperatingMode,
    )
    COMPRESSOR_USE_NIGHT_SPEED = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatPumpPowerCtrl.param.useDayNightSpeed",
        value_type=str,
        human_readable=HeatPumpCompressorUseNightSpeed,
    )
    COMPRESSOR_NIGHT_SPEED = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].HeatPumpPowerCtrl.param.maxPowerScaledNight",
        value_type=float,
    )
    CIRCULATION_PUMP = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].CircPump.values.setValueScaled",
        value_type=float,
    )
    SOURCE_PUMP_SPEED = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].Source.values.setValueScaled",
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
    CONDENSER_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.tempCond",
        value_type=float,
    )
    VAPORIZER_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].OverHeatCtrl.values.tempVap",
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
    OPERATING_TIME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalData.operationalTimeS",
        value_type=int,
    )
    MAX_RUNTIME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalData.maxRunTimeS",
        value_type=int,
    )
    ACTIVATION_COUNTER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatpump[%s].operationalData.activationCounter",
        value_type=int,
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
    FLOW_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].heatCircuitMixer.flowTemp.values.actValue",
        value_type=float,
    )
    RETURN_FLOW_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].tempReflux.values.actValue",
        value_type=float,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.setValue",
        value_type=float,
    )
    TARGET_TEMPERATURE_DAY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.normalSetTemp",
        value_type=float,
    )
    HEATING_LIMIT_DAY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdDayTemp.value",
        value_type=float,
    )
    TARGET_TEMPERATURE_NIGHT = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.reducedSetTemp",
        value_type=float,
    )
    HEATING_LIMIT_NIGHT = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.thresholdNightTemp.value",
        value_type=float,
    )
    TARGET_TEMPERATURE_AWAY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.holidaySetTemp",
        value_type=float,
    )
    TARGET_TEMPERATURE_OFFSET = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.offsetRoomTemp",
        value_type=float,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].param.operatingMode",
        value_type=int,
        human_readable=HeatCircuitOperatingMode,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.heatRequest",
        value_type=int,
        human_readable=HeatCircuitHeatRequest,
    )
    COOL_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.heatCircuit[%s].values.coolRequest",
        value_type=int,
        human_readable=HeatCircuitCoolRequest,
    )


class SolarCircuit(Enum):
    """The solar circuit endpoint settings."""

    NAME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].param.name",
        value_type=str,
    )
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].param.operatingMode",
        value_type=int,
        human_readable=SolarCircuitOperatingMode,
    )
    SOURCE_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].collectorTemp.values.actValue",
        value_type=float,
    )
    PUMP_1 = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].values.pump1",
        value_type=float,
    )
    PUMP_2 = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].values.pump2",
        value_type=float,
    )
    CURRENT_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].referenceTemp.values.actValue",
        value_type=float,
        quantity=2,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].param.setTempMax.value",
        value_type=float,
        quantity=2,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.genericHeat[%s].values.heatRequest",
        value_type=str,
        human_readable=SolarCircuitHeatRequest,
        quantity=2,
    )
    HEATING_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].heatMeter.values.accumulatedHeat",
        value_type=float,
    )
    DAILY_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].heatMeter.values.heatDay",
        value_type=float,
    )
    ACTUAL_POWER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.solarCircuit[%s].heatMeter.values.power",
        value_type=float,
    )


class ExternalHeatSource(Enum):
    OPERATING_MODE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].param.operatingMode",
        value_type=int,
        human_readable=ExternalHeatSourceOperatingMode,
    )
    TARGET_TEMPERATURE = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].values.setTemp",
        value_type=float,
    )
    HEAT_REQUEST = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.values.setValueB",
        value_type=str,
        human_readable=ExternalHeatSourceHeatRequest,
    )
    OPERATING_TIME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.operationalData.operationalTimeS",
        value_type=int,
    )
    MAX_RUNTIME = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.operationalData.maxRunTimeS",
        value_type=int,
    )
    ACTIVATION_COUNTER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.extHeatSource[%s].DO.operationalData.activationCounter",
        value_type=int,
    )


class Photovoltaic(Enum):
    EXCESS_POWER = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.ElectricEnergyMeter.values.power",
        value_type=float,
    )
    DAILY_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.ElectricEnergyMeter.values.heatDay",
        value_type=float,
    )
    TOTAL_ENERGY = EndpointProperties(
        f"{PAYLOAD_PREFIX}.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
        value_type=float,
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
    PHOTOVOLTAIC = "photovoltaic"


Section: TypeAlias = (
    System | BufferTank | HotWaterTank | HeatPump | HeatCircuit | SolarCircuit | ExternalHeatSource | Photovoltaic
)
