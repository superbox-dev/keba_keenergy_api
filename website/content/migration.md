---
sidebar_position: 6
---

# Migration from 2.x

3.0 is a typed low-level API. The section clients (`client.heat_pump`, …) with their `get_*` and `set_*` methods are
gone, everything is read with `read()` and written with `write()`. Two sections and many endpoints and enum
members are renamed to the technical terms, see the tables [below](#sections).

## Imports

| 2.x                                    | 3.0                                                           |
|----------------------------------------|---------------------------------------------------------------|
| `keba_keenergy_api.api`                | `keba_keenergy_api.client` (or `keba_keenergy_api`)           |
| `keba_keenergy_api.constants` sections | `keba_keenergy_api.sections`                                  |
| `keba_keenergy_api.constants` enums    | `keba_keenergy_api.enums`                                     |
| `keba_keenergy_api.endpoints` types    | `keba_keenergy_api.models`                                    |
| `keba_keenergy_api.error`              | `keba_keenergy_api.exceptions`                                |
| `InvalidJsonError`                     | `InvalidResponseError`                                        |

## Client

```python
# 2.x
client = KebaKeEnergyAPI("ap4400.local", "test", "test", ssl=True, skip_ssl_verification=True)

# 3.0
client = KebaKeEnergyAPI("ap4400.local", username="test", password="test", ssl=True, verify_ssl=False)
```

## Reading

```python
# 2.x
data = await client.read_data(request=[HeatCircuit.TARGET_TEMPERATURE_DAY], human_readable=True)
data["heat_circuit"]["target_temperature_day"][0]["value"]  # 20.5

# 3.0
readings = await client.read([HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL])
readings[HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL][0].value  # 20.5
```

- The readings are keyed by the section, with one `Reading` per device instead of a dict with `value` and
  `attributes`.
- Values are typed: `bool` instead of `"on"` / `"off"`, enum members instead of lowercase names.
- Values are not rounded or scaled anymore and the mixer setpoint (`MIXER_SETPOINT`, was `MIXER_POSITION`) is the raw
  setpoint `-1..1` instead of `closed` / `off` / `open`.
- The heating curve points are no longer part of the read response, use `get_curve_tables()`.
- `read_message_ids()` is replaced by `read(..., message_ids=True)`, which reads the message ids with the values in
  the same request and sets `Reading.message_id` (`value` and `kind`) instead of the raw number.

## Writing

```python
# 2.x
await client.heat_circuit.set_operating_mode(mode="day", position=2)
await client.write_data(request={HeatCircuit.TARGET_TEMPERATURE_DAY: (20, None, 21)})

# 3.0
await client.write(
    {
        HeatingCircuit.OPERATING_MODE: [None, HeatingCircuitOperatingMode.NORMAL],
        HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL: [20, None, 21],
    }
)
```

`write()` takes a sequence of values per section (also for one device) and raises an `APIError` for a read-only
section or a value of the wrong type instead of ignoring it.

## Methods

| 2.x | 3.0 |
|---|---|
| `read_data(request, position, human_readable, extra_attributes)` | `read(sections, *, counts)` |
| `write_data(request)` | `write(values)` |
| `filter_request(request, position)` | `filter_supported(sections, *, counts)` |
| `read_message_ids(request, position)` | `read(sections, *, counts, message_ids=True)` |
| `client.system.get_positions()` | `get_device_counts()` |
| `client.system.get_info()` | `get_system_info()` |
| `client.system.get_hmi_info()` | `get_hmi_info()` |
| `client.system.get_device_info()` | `get_device_info()` |
| `client.system.get_timezone()` | `get_timezone()` |
| `client.heat_circuit.get_heating_curve_points()` | `get_curve_tables()` |
| `client.heat_circuit.set_heating_curve_points()` | `set_curve_table_points()` |
| all other `client.<section>.get_*()` / `set_*()` / `has_*()` | `read()` / `write()` |

## Sections

| 2.x | 3.0 |
|---|---|
| `HeatCircuit` | `HeatingCircuit` |
| `HotWaterTank` | `DHWTank` |

`get_device_counts()` returns `DeviceCounts` with the fields `heating_circuit` and `dhw_tank` for these sections.

## Constants and models

| 2.x | 3.0 |
|---|---|
| `MIN_HEATING_CURVE_POINTS`, `MAX_HEATING_CURVE_POINTS` | `MIN_CURVE_TABLE_POINTS`, `MAX_CURVE_TABLE_POINTS` |
| heating curve points as `(outdoor, flow)` tuples | `CurveTable` with `CurvePoint`s |

## Endpoints

The section is the 2.x name, see [Sections](#sections) for the renamed ones.

| Section | 2.x | 3.0 |
|---|---|---|
| `System` | `BUFFER_TANK_NUMBERS` | private, use `get_device_counts()` |
| `System` | `HOT_WATER_TANK_NUMBERS` | private, use `get_device_counts()` |
| `System` | `HEAT_PUMP_NUMBERS` | private, use `get_device_counts()` |
| `System` | `HEAT_CIRCUIT_NUMBERS` | private, use `get_device_counts()` |
| `System` | `SOLAR_CIRCUIT_NUMBERS` | private, use `get_device_counts()` |
| `System` | `EXTERNAL_HEAT_SOURCE_NUMBERS` | private, use `get_device_counts()` |
| `System` | `SWITCH_VALVE_NUMBERS` | private, use `get_device_counts()` |
| `System` | `RAM_USAGE` | `TEMPORARY_MEMORY_USAGE` |
| `System` | `FLASH_ERASE_COUNTER` | `FLASH_MAX_ERASE_COUNTER` |
| `BufferTank` | `CURRENT_TOP_TEMPERATURE` | `TOP_TEMPERATURE` |
| `BufferTank` | `CURRENT_BOTTOM_TEMPERATURE` | `BOTTOM_TEMPERATURE` |
| `BufferTank` | `STANDBY_TEMPERATURE` | `BACKUP_TEMPERATURE` |
| `BufferTank` | `OUTDOOR_TEMPERATURE_EXCESS_ENERGY_LIMIT` | `EXCESS_ENERGY_OUTDOOR_TEMPERATURE_LIMIT` |
| `BufferTank` | `EXCESS_ENERGY_MODE` | `EXCESS_ENERGY_STATE` |
| `BufferTank` | `HEAT_REQUEST` | `HEATING_REQUEST` |
| `BufferTank` | `COOL_REQUEST` | `COOLING_REQUEST` |
| `HotWaterTank` | `CURRENT_TEMPERATURE` | `TEMPERATURE` |
| `HotWaterTank` | `STANDBY_TEMPERATURE` | `BACKUP_TEMPERATURE` |
| `HotWaterTank` | `EXCESS_ENERGY_MODE` | `EXCESS_ENERGY_STATE` |
| `HotWaterTank` | `HEAT_REQUEST` | `HEATING_REQUEST` |
| `HotWaterTank` | `FRESH_WATER_FLOW` | `FRESH_WATER_FLOW_ACTIVE` |
| `HotWaterTank` | `FRESH_WATER_MODULE_TEMPERATURE` | `FRESH_WATER_TEMPERATURE` |
| `HotWaterTank` | `FRESH_WATER_MODULE_PUMP_SPEED` | removed |
| `HotWaterTank` | `CIRCULATION_PUMP_STATE` | `CIRCULATION_PUMP_ACTIVE` |
| `HeatPump` | `SUBSTATE` | `SUB_STATE` |
| `HeatPump` | `OPERATING_MODE` | removed |
| `HeatPump` | `COMPRESSOR_USE_NIGHT_SPEED` | `USE_COMPRESSOR_NIGHT_POWER_LIMIT` |
| `HeatPump` | `COMPRESSOR_NIGHT_SPEED` | `COMPRESSOR_NIGHT_POWER_LIMIT` |
| `HeatPump` | `SOURCE_PUMP_SPEED` | `SOURCE_ACTUATOR_SPEED` |
| `HeatPump` | `SOURCE_INPUT_TEMPERATURE` | `SOURCE_INLET_TEMPERATURE` |
| `HeatPump` | `SOURCE_OUTPUT_TEMPERATURE` | `SOURCE_OUTLET_TEMPERATURE` |
| `HeatPump` | `COMPRESSOR_INPUT_TEMPERATURE` | `COMPRESSOR_INLET_TEMPERATURE` |
| `HeatPump` | `COMPRESSOR_OUTPUT_TEMPERATURE` | `COMPRESSOR_OUTLET_TEMPERATURE` |
| `HeatPump` | `COMPRESSOR` | `COMPRESSOR_SPEED` |
| `HeatPump` | `CONDENSER_TEMPERATURE` | `CONDENSATION_TEMPERATURE` |
| `HeatPump` | `VAPORIZER_TEMPERATURE` | `EVAPORATION_TEMPERATURE` |
| `HeatPump` | `TARGET_OVERHEATING` | `TARGET_SUCTION_SUPERHEAT` |
| `HeatPump` | `CURRENT_OVERHEATING` | `SUCTION_SUPERHEAT` |
| `HeatPump` | `HEAT_REQUEST` | `REQUEST` |
| `HeatPump` | `HEATING_MASS_FLOW_RATE` | removed |
| `HeatPump` | `COOLING_MASS_FLOW_RATE` | removed |
| `HeatPump` | `HOT_WATER_MASS_FLOW_RATE` | removed |
| `HeatPump` | `HEATING_POWER` | `HEATING_THERMAL_POWER` |
| `HeatPump` | `HOT_WATER_POWER` | `DHW_THERMAL_POWER` |
| `HeatPump` | `RETURN_FLOW_TEMPERATURE` | `RETURN_TEMPERATURE` |
| `HeatPump` | `CONSUMING_EXCESS_ENERGY` | `EXCESS_ENERGY_ACTIVE` |
| `HeatPump` | `COMPRESSOR_POWER` | `ELECTRICAL_POWER` |
| `HeatPump` | `HEATING_ENERGY` | `HEATING_THERMAL_ENERGY` |
| `HeatPump` | `HEATING_ENERGY_CONSUMPTION` | `HEATING_ELECTRICAL_ENERGY` |
| `HeatPump` | `COOLING_ENERGY` | `COOLING_THERMAL_ENERGY` |
| `HeatPump` | `COOLING_ENERGY_CONSUMPTION` | `COOLING_ELECTRICAL_ENERGY` |
| `HeatPump` | `HOT_WATER_ENERGY` | `DHW_THERMAL_ENERGY` |
| `HeatPump` | `HOT_WATER_ENERGY_CONSUMPTION` | `DHW_ELECTRICAL_ENERGY` |
| `HeatPump` | `HOT_WATER_SPF` | `DHW_SPF` |
| `HeatPump` | `TOTAL_ENERGY_CONSUMPTION` | `TOTAL_ELECTRICAL_ENERGY` |
| `HeatPump` | `HEATING_EXCESS_ENERGY_CONSUMPTION` | `EXCESS_ENERGY_HEATING_CONSUMPTION` |
| `HeatPump` | `COOLING_EXCESS_ENERGY_CONSUMPTION` | `EXCESS_ENERGY_COOLING_CONSUMPTION` |
| `HeatPump` | `HOT_WATER_EXCESS_ENERGY_CONSUMPTION` | `EXCESS_ENERGY_DHW_CONSUMPTION` |
| `HeatPump` | `HAS_COMPRESSOR_FAILURE` | `COMPRESSOR_FAILURE` |
| `HeatPump` | `HAS_SOURCE_FAILURE` | `SOURCE_FAILURE` |
| `HeatPump` | `HAS_SOURCE_ACTUATOR_FAILURE` | `SOURCE_ACTUATOR_FAILURE` |
| `HeatPump` | `HAS_THREE_PHASE_FAILURE` | `THREE_PHASE_FAILURE` |
| `HeatPump` | `HAS_SOURCE_PRESSURE_FAILURE` | `SOURCE_PRESSURE_FAILURE` |
| `HeatPump` | `HAS_VFD_FAILURE` | `VFD_FAILURE` |
| `HeatPump` | `COOL_METER_TYPE` | removed |
| `HeatPump` | `HOT_WATER_METER_TYPE` | removed |
| `HeatCircuit` | `MODE` | `TYPE` |
| `HeatCircuit` | `FLOW_TEMPERATURE_SETPOINT` | `TARGET_FLOW_TEMPERATURE` |
| `HeatCircuit` | `MIXER_POSITION` | `MIXER_SETPOINT` |
| `HeatCircuit` | `PUMP_STATE` | `PUMP_ACTIVE` |
| `HeatCircuit` | `TARGET_TEMPERATURE` | `TARGET_ROOM_TEMPERATURE` |
| `HeatCircuit` | `EXCESS_ENERGY_MODE` | `EXCESS_ENERGY_STATE` |
| `HeatCircuit` | `HEAT_REQUEST` | `HEATING_REQUEST` |
| `HeatCircuit` | `COOL_REQUEST` | `COOLING_REQUEST` |
| `HeatCircuit` | `EXCESS_ENERGY_TARGET_TEMPERATURE` | `EXCESS_ENERGY_TARGET_ROOM_TEMPERATURE` |
| `HeatCircuit` | `EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS` | `EXCESS_ENERGY_TARGET_ROOM_TEMPERATURE_HYSTERESIS` |
| `HeatCircuit` | `EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE` | `EXCESS_ENERGY_TARGET_ROOM_COOLING_TEMPERATURE` |
| `HeatCircuit` | `EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE_HYSTERESIS` | `EXCESS_ENERGY_TARGET_ROOM_COOLING_TEMPERATURE_HYSTERESIS` |
| `HeatCircuit` | `SELECTED_TARGET_TEMPERATURE` | `SELECTED_TARGET_ROOM_TEMPERATURE` |
| `HeatCircuit` | `TARGET_TEMPERATURE_DAY` | `TARGET_ROOM_TEMPERATURE_NORMAL` |
| `HeatCircuit` | `TARGET_COOLING_TEMPERATURE_DAY` | `TARGET_ROOM_COOLING_TEMPERATURE_NORMAL` |
| `HeatCircuit` | `HEATING_LIMIT_DAY` | `HEATING_LIMIT_NORMAL` |
| `HeatCircuit` | `COOLING_LIMIT_DAY` | `COOLING_LIMIT_NORMAL` |
| `HeatCircuit` | `EXCESS_ENERGY_HEATING_LIMIT_DAY` | `EXCESS_ENERGY_HEATING_LIMIT_NORMAL` |
| `HeatCircuit` | `EXCESS_ENERGY_COOLING_LIMIT_DAY` | `EXCESS_ENERGY_COOLING_LIMIT_NORMAL` |
| `HeatCircuit` | `TARGET_TEMPERATURE_NIGHT` | `TARGET_ROOM_TEMPERATURE_REDUCED` |
| `HeatCircuit` | `TARGET_COOLING_TEMPERATURE_NIGHT` | `TARGET_ROOM_COOLING_TEMPERATURE_REDUCED` |
| `HeatCircuit` | `HEATING_LIMIT_NIGHT` | `HEATING_LIMIT_REDUCED` |
| `HeatCircuit` | `COOLING_LIMIT_NIGHT` | `COOLING_LIMIT_REDUCED` |
| `HeatCircuit` | `EXCESS_ENERGY_HEATING_LIMIT_NIGHT` | `EXCESS_ENERGY_HEATING_LIMIT_REDUCED` |
| `HeatCircuit` | `EXCESS_ENERGY_COOLING_LIMIT_NIGHT` | `EXCESS_ENERGY_COOLING_LIMIT_REDUCED` |
| `HeatCircuit` | `TARGET_TEMPERATURE_AWAY` | `TARGET_ROOM_TEMPERATURE_VACATION` |
| `HeatCircuit` | `TARGET_TEMPERATURE_OFFSET` | `ROOM_TEMPERATURE_OFFSET` |
| `HeatCircuit` | `AWAY_START_DATE` | `VACATION_START` |
| `HeatCircuit` | `AWAY_END_DATE` | `VACATION_END` |
| `HeatCircuit` | `USE_HEATING_CURVE` | `USE_CURVE_TABLE` |
| `HeatCircuit` | `HAS_VAR_SPEED_PUMP` | `HAS_VARIABLE_SPEED_PUMP` |
| `HeatCircuit` | `MIXER_RETURN_FLOW_TEMPERATURE` | `MIXER_RETURN_TEMPERATURE` |
| `HeatCircuit` | `HAS_RETURN_FLOW_TEMPERATURE` | `HAS_RETURN_TEMPERATURE` |
| `HeatCircuit` | `RETURN_FLOW_TEMPERATURE` | `RETURN_TEMPERATURE` |
| `SolarCircuit` | `SOURCE_TEMPERATURE` | `COLLECTOR_TEMPERATURE` |
| `SolarCircuit` | `PUMP_1` | `PUMP_1_SPEED` |
| `SolarCircuit` | `PUMP_2` | `PUMP_2_SPEED` |
| `SolarCircuit` | `CURRENT_TEMPERATURE` | `CONSUMER_TEMPERATURE` |
| `SolarCircuit` | `TARGET_TEMPERATURE` | `CONSUMER_TARGET_TEMPERATURE` |
| `SolarCircuit` | `HEAT_REQUEST` | `CONSUMER_HEATING_REQUEST` |
| `SolarCircuit` | `HEATING_ENERGY` | `TOTAL_THERMAL_ENERGY` |
| `SolarCircuit` | `DAILY_ENERGY` | `DAILY_THERMAL_ENERGY` |
| `SolarCircuit` | `ACTUAL_POWER` | `THERMAL_POWER` |
| `SolarCircuit` | `PRIORITY_1_BEFORE_2` | `CONSUMER_1_PRIORITY` |
| `ExternalHeatSource` | `MIN_RUNTIME_EXCESS_ENERGY` | `EXCESS_ENERGY_MIN_RUNTIME` |
| `ExternalHeatSource` | `HEAT_REQUEST` | `HEATING_REQUEST` |
| `ExternalHeatSource` | `CONSUMING_EXCESS_ENERGY` | `EXCESS_ENERGY_ACTIVE` |
| `PassiveCooling` | `MIXER_POSITION` | `MIXER_SETPOINT` |
| `Photovoltaics` | `DAILY_ENERGY` | `DAILY_EXCESS_ENERGY` |
| `Photovoltaics` | `TOTAL_ENERGY` | `TOTAL_EXCESS_ENERGY` |

## Enums

| 2.x | 3.0 |
|---|---|
| `BoolEnum` | `bool` |
| `BufferTankOperatingMode.HEAT_UP` | `BufferTankOperatingMode.MANUAL_CHARGE` |
| `HotWaterTankOperatingMode` | `DHWTankOperatingMode` |
| `HotWaterTankOperatingMode.HEAT_UP` | `DHWTankOperatingMode.MANUAL_CHARGE` |
| `BufferTankExcessEnergyMode`, `HotWaterTankExcessEnergyMode`, `HeatCircuitExcessEnergyMode` | `ExcessEnergyState` |
| `HeatPumpState.FLOW` | `HeatPumpState.PRE_RUN` |
| `HeatPumpState.AUTO_HEAT` | `HeatPumpState.AUTOMATIC` |
| `HeatPumpState.AUTO_COOL` | `HeatPumpState.COOLING` |
| `HeatPumpState.INFLOW` | `HeatPumpState.POST_RUN` |
| `HeatPumpSubState.DEFROST_PRE_FLOW` | `HeatPumpSubState.DEFROST_PRE_RUN` |
| `HeatPumpSubState.PREHEAT_FLOW` | `HeatPumpSubState.PRE_RUN_HEAT_UP` |
| `HeatPumpSubState.OPEN` | `HeatPumpSubState.OPENING` |
| `HeatPumpSubState.DEFROST_VENTING` | `HeatPumpSubState.DEFROST_FAN` |
| `HeatPumpSubState.RETURN_FLOW_OFF` | `HeatPumpSubState.RETURN_OFF` |
| `HeatPumpOperatingMode` | removed |
| `HeatCircuitMode` | `HeatingCircuitType` |
| `HeatCircuitOperatingMode` | `HeatingCircuitOperatingMode` |
| `HeatCircuitOperatingMode.DAY` | `HeatingCircuitOperatingMode.NORMAL` |
| `HeatCircuitOperatingMode.NIGHT` | `HeatingCircuitOperatingMode.REDUCED` |
| `HeatCircuitOperatingMode.HOLIDAY` | `HeatingCircuitOperatingMode.VACATION` |
| `HeatCircuitHeatRequest`, `HeatCircuitCoolRequest` | `HeatingCircuitRequest` |
| `HeatCircuitHeatRequest.ON` | `HeatingCircuitRequest.ACTIVE` |
| `HeatCircuitHeatRequest.FLOW_OFF` | `HeatingCircuitRequest.RETURN_OFF` |
| `HeatCircuitHeatRequest.TEMPORARY_OFF` | `HeatingCircuitRequest.TEMPERATURE_PRIORITY_OFF` |
| `HeatCircuitHeatRequest.INFLOW_OFF` | `HeatingCircuitRequest.FLOW_OFF` |
| `SolarCircuitPriority` | private |
| `BoolEnum` (`SolarCircuit.OPERATING_MODE`) | `SolarCircuitOperatingMode` |
| `SwitchValvePosition.OPEN` | `SwitchValvePosition.POSITION_1` |
| `SwitchValvePosition.CLOSED` | `SwitchValvePosition.POSITION_2` |
| `MixerSwitchValvePosition` | removed, `MIXER_SETPOINT` returns the raw setpoint (`-1..1`) |
| `SectionPrefix` | `DeviceType` |
| `SectionPrefix.HEAT_CIRCUIT` | `DeviceType.HEATING_CIRCUIT` |
| `SectionPrefix.HOT_WATER_TANK` | `DeviceType.DHW_TANK` |
| int (`ELECTRIC_ENERGY_METER_TYPE`) | `ElectricEnergyMeterType` |
| int (`HEAT_METER_TYPE`) | `HeatMeterType` |
