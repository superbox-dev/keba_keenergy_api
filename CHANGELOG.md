# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The 3.0.0 release is a typed low-level API with the technical terms as names. It breaks every 2.x import, see
the [migration guide](https://superbox-dev.github.io/keba_keenergy_api/migration) ([Issue #132][issue-132]).

### Added

- Added `KebaKeEnergyAPI.read()`, which returns a `Reading` per device with the typed `value`, the `raw_value`
  (as the Web HMI delivers it, e.g. `"25"` for `HeatPumpSubState.DRIP`, which has the values `13` and `25`),
  `device_number`, `consumer_number`, `lower_limit`, `upper_limit` and `message_id` ([Issue #132][issue-132])
- Added `write()`, `filter_supported()`, `get_device_counts()` (`DeviceCounts`), `get_system_info()`,
  `get_hmi_info()`, `get_device_info()`, `get_curve_tables()` (`CurveTable`) and
  `set_curve_table_points()` to `KebaKeEnergyAPI` ([Issue #132][issue-132])
- Added `get_week_timers()` and `set_week_timers()` for the week timers of the heating circuits (heating and cooling)
  and DHW tanks (`WeekTimerType`, `WeekTimer`, `DayTimer`, `TimeBlock` and `WeekDay`), the times are `timedelta`
  since midnight, so `24:00` is possible
- Added `EndpointDefinition.raw_unit`, `EndpointDefinition.display_unit`, `EndpointDefinition.display_factor`,
  `EndpointDefinition.display_precision`, `EndpointDefinition.message_id` and `DeviceType` (the device type of a
  section as `device_type`) ([Issue #132][issue-132])
- Added `read(..., message_ids=True)`, which reads the message ids with the values in the same request
  (`Reading.message_id` with `value` and `kind`). A message id the Web HMI doesn't know is left out, the value is
  still read ([Issue #132][issue-132])
- Added `read(..., limits=...)` to choose the endpoints whose limits are read (`all`, `none`, `read_only` or
  `writable`), as the limits make a request about twice as slow ([Issue #132][issue-132])
- Added the message ids of the components of pumps, the compressor, the mixers, the heat and energy meters, the
  superheat control, the switch valve of the passive cooling and the external heat source ([Issue #132][issue-132])
- Added `UnsupportedVariableError` (with the `variable` name) and `InvalidResponseError` ([Issue #132][issue-132])
- Added `ExcessEnergyState`, `HeatingCircuitRequest`, `HeatingCircuitType`, `ElectricalEnergyMeterType`, `HeatMeterType`
  and `SolarCircuitOperatingMode` ([Issue #132][issue-132])
- Added the heat pump endpoints `MODEL`, `TYPE` (`HeatPumpType`), `TARGET_TEMPERATURE`, `STATE_DURATION`,
  `STATE_REMAINING_TIME`, `SUPERHEAT_CONTROL_STATE` (`SuperheatControlState`), the operating times per mode
  (`HEATING_OPERATING_TIME`, `COOLING_OPERATING_TIME`, `DHW_OPERATING_TIME`), the defrost statistics (`DEFROST_CYCLES`,
  `FAILED_DEFROST_CYCLES`, `DEFROST_THERMAL_ENERGY`, `DEFROST_ELECTRICAL_ENERGY`, `DEFROST_OPERATING_TIME`,
  `EXCESS_ENERGY_DEFROST_CONSUMPTION`), the thermal excess energy in total and per mode (`EXCESS_ENERGY_THERMAL_ENERGY`,
  `EXCESS_ENERGY_HEATING_THERMAL_ENERGY`, `EXCESS_ENERGY_COOLING_THERMAL_ENERGY`, `EXCESS_ENERGY_DHW_THERMAL_ENERGY`,
  `EXCESS_ENERGY_DEFROST_THERMAL_ENERGY`), the option `HAS_REVERSE_CYCLE_DEFROST` and the failures
  `HIGH_PRESSURE_FAILURE`, `LOW_PRESSURE_FAILURE`, `PHASE_MONITOR_FAILURE` and `GAS_LEAK_FAILURE` ([Issue
  #133][issue-133])
- Added the meter values of the heat pump: power, accumulated and daily energy and mass flow of the heating, DHW,
  cooling and source meter (`HEATING_METER_*`, `DHW_METER_*`, `COOLING_METER_*`, `SOURCE_METER_*`) and the
  accumulated and daily energy of the electrical meter (`METER_ACCUMULATED_ELECTRICAL_ENERGY`,
  `METER_DAILY_ELECTRICAL_ENERGY`) ([Issue #133][issue-133])
- Added `HeatPump.SOURCE_VOLUME_FLOW`, the volume flow on the source side ([Issue #133][issue-133])
- Added the `Cascade` section (`DeviceType.CASCADE`) with the settings, power and COP of the cascade and its
  statistics, the `CASCADE_*` endpoints of the heat pump and the external heat source (state, power level,
  priorities, lock, forced activation, times) and `CascadeStrategy` and `CascadeState` ([Issue #133][issue-133])
- Added the sensors and outputs `HeatPump.CONDENSER_OUTLET_TEMPERATURE`, `OIL_TEMPERATURE`, `SOURCE_PRESSURE`,
  `OUTDOOR_UNIT_TEMPERATURE`, `COOLING_ACTIVE`, `ELECTRIC_DEFROST_ACTIVE`, `OIL_HEATER_ACTIVE`,
  `CONDENSATE_HEATER_ACTIVE`, `DHWTank.BOTTOM_TEMPERATURE`, the flow and return temperatures of the buffer tank and
  the passive cooling (`FLOW_TEMPERATURE`, `RETURN_TEMPERATURE`), the temperature and return temperature of the
  external heat source (`TEMPERATURE`, `RETURN_TEMPERATURE`) and `HeatingCircuit.FILTERED_OUTDOOR_TEMPERATURE` ([Issue
  #133][issue-133])
- Added `SolarCircuit.METER_MASS_FLOW` and the solar circuit statistics `THERMAL_ENERGY` and `OPERATING_TIME`
  ([Issue #133][issue-133])
- Added the performance factors `HEATING_PF`, `COOLING_PF`, `DHW_PF` and `TOTAL_PF` of the heat pump and the
  cascade, `HeatPump.TOTAL_OPERATING_TIME`, `HeatPump.MOP_ACTIVE` and the estimated compressor power
  (`COMPRESSOR_ESTIMATED_ELECTRICAL_POWER`, `COMPRESSOR_ESTIMATED_REFRIGERATING_CAPACITY`) ([Issue #133][issue-133])
- Added `KebaKeEnergyAPI.get_alarms()` and `get_alarm_count()`, which read the pending alarms of the control unit
  (`Alarm`, `AlarmPriority`) ([Issue #135][issue-135])
- Added `KebaKeEnergyAPI.is_remote_maintenance_active()`, `is_remote_maintenance_connected()`,
  `is_remote_maintenance_server_reachable()` and `set_remote_maintenance_active()` for the remote maintenance and
  `is_modbus_active()` and `set_modbus_active()` for the Modbus TCP server of the control unit ([Issue
  #138][issue-138])
- Added `KebaKeEnergyAPI.get_curve_table_names()`, which reads only the names of the curve tables, and
  `get_curve_tables(names)`, which reads only the points of the requested curve tables ([Issue #144][issue-144])

### Changed

- Changed the minimum Python version to 3.14.2 ([Issue #132][issue-132])
- Changed the modules: `constants` became `endpoints`, `enums` (values), `models` and `constants`
  (`API_DEFAULT_TIMEOUT`, `MIN_CURVE_TABLE_POINTS`, `MAX_CURVE_TABLE_POINTS`), `api` became `client` and
  `error` became `exceptions` ([Issue #132][issue-132])
- Changed `KebaKeEnergyAPI()`: `username` and `password` are keyword-only, `verify_ssl` replaced
  `skip_ssl_verification` ([Issue #132][issue-132])
- Changed the values: `read()` returns `bool`, `float`, `int`, `str` or enum members instead of lowercase strings,
  without rounding or scaling, e.g. ratios stay `0..1`, the CPU usage stays per mille and the mixer setpoint is
  returned as it is ([Issue #132][issue-132])
- Changed `filter_supported()` to drop an endpoint if the Web HMI doesn't know its variable of one of the installed
  devices, as `read()` would fail with it ([Issue #132][issue-132])
- Changed the session: a passed session is used as it is, otherwise the client opens one on the first request and
  closes it with `close()`, no session per request anymore ([Issue #132][issue-132])
- Changed `write()` to raise an `APIError` for a read-only endpoint or a value of the wrong type instead of
  ignoring it ([Issue #132][issue-132])
- Changed `InvalidJsonError` to `InvalidResponseError` ([Issue #132][issue-132])
- Renamed the device types, the endpoints, the enums and their members to the technical terms (e.g. `HeatCircuit` to
  `HeatingCircuit`, `HotWaterTank` to `DHWTank`) and replaced the methods of the section clients, the
  [migration guide](https://superbox-dev.github.io/keba_keenergy_api/migration) has the tables (old name → new name)
  ([Issue #132][issue-132])

### Removed

- Removed the section clients (`client.heat_pump`, …) with all `get_*`, `set_*`, `has_*` and `get_number_of_*`
  methods, `read_data()`, `write_data()` and `filter_request()` ([Issue #132][issue-132])
- Removed `human_readable`, `extra_attributes` and `key_prefix`, the heating curve points are no longer part of the
  read response ([Issue #132][issue-132])
- Removed `Position`, `EndpointPath`, `PAYLOAD_PREFIX`, `ACT_VALUE_SUFFIX`, `MESSAGE_ID_SUFFIX`, `BoolEnum`,
  `HeatPumpOperatingMode` and `MixerSwitchValvePosition` ([Issue #132][issue-132])

[issue-132]: https://github.com/superbox-dev/keba_keenergy_api/issues/132
[issue-133]: https://github.com/superbox-dev/keba_keenergy_api/issues/133
[issue-135]: https://github.com/superbox-dev/keba_keenergy_api/issues/135
[issue-138]: https://github.com/superbox-dev/keba_keenergy_api/issues/138
[issue-144]: https://github.com/superbox-dev/keba_keenergy_api/issues/144

<!--start-->

## [2.14.0] - 2026-10-28

### Added

- Added `HeatPumpState.SOURCE_FLUSH` (`9`) and `ExternalHeatSourceOperatingMode` (`OFF`, `ON`, `FLUE`)
  ([Issue #131][issue-131])
- Added `ExternalHeatSource.HAS_EMISSIONS` with `get_has_emissions` and `set_has_emissions` of the external heat
  source
- Added `MessageIdKind` (`OK`, `DEACTIVATED`, `ERROR`) with `MessageIdKind.from_message_id()` to get the kind of a
  message id from `read_message_ids()` like the Web HMI ([Issue #136][issue-136])
- Added `System.FLASH_ERASE_COUNTER` with `get_flash_erase_counter` to read the flash erase counter of the
  controller, which also counts writes from the Web HMI and the display ([Issue #137][issue-137])

### Changed

- Documented the meaning of the `HeatPumpState`, `HeatCircuitHeatRequest`, `HeatCircuitCoolRequest`,
  `SwitchValvePosition` and `MixerSwitchValvePosition` values with misleading names ([Issue #131][issue-131])

### Fixed

- Fixed reading the heat pump state `9` (source flush), which raised an `APIError` ([Issue #131][issue-131])
- Fixed reading and setting the external heat source operating mode `2` (flue), which raised an `APIError`.
  `ExternalHeatSource.OPERATING_MODE` now uses `ExternalHeatSourceOperatingMode` instead of `BoolEnum`, `off` and
  `on` stay the same ([Issue #131][issue-131])

[issue-131]: https://github.com/superbox-dev/keba_keenergy_api/issues/131
[issue-136]: https://github.com/superbox-dev/keba_keenergy_api/issues/136
[issue-137]: https://github.com/superbox-dev/keba_keenergy_api/issues/137

## [2.13.0] - 2026-10-24

### Added

- Added `read_message_ids()` to read the message ids (`state.msgId`) of sensors with one request.
  A message id other than `0` means that the sensor is not in use, e.g. not connected ([Issue #67][issue-67])
- Added `has_message_id` and `message_id_path` to `Endpoint` for all 31 confirmed `values.actValue` sensors
- Added the optional `position` argument to `has_mixer()` of the heating circuit and `has_fresh_water_module()`
  of the hot water tank
- Added `async with` support and `close()` to `KebaKeEnergyAPI`. Without a passed session, all requests share
  one session instead of opening a new connection per request. A passed session is left open
- Added `APITimeoutError`, raised when a request times out. It inherits from `APIError` and `TimeoutError`
- Added a constants page to the documentation with all endpoints (path, type, writable, values), the value enums
  and the other public constants of `keba_keenergy_api.constants`
- Added a preview image to the documentation for links shared on social media and removed the search page
  from the documentation sitemap
- Added an errors section to the usage page of the documentation

### Changed

- Dropped support for Python 3.10 (end of life). Python 3.11 is now the minimum
- Changed `SectionPrefix` to a `StrEnum`
- Read the heating curve points without attributes (`attr="0"`) for a smaller response
- Renamed `SolarCircuitPriority1Before2StringEndpoint.helper()` to `extra_writes()`
- Simplified the internal endpoint code (no changes to the public API)
- Converted all docstrings to the NumPy style
- Added the `Apache-2.0` license expression and the `Typing :: Typed` / `Framework :: AsyncIO` classifiers
  to the package metadata
- `write_data()` and the setters no longer send a request if there is nothing to write
- `read_data()`, `read_message_ids()` and `filter_request()` without a `position` read the installed devices
  only on the first call and reuse them afterwards. Create a new `KebaKeEnergyAPI` to read them again
- `filter_request()` checks all variables with one request (plus one per unknown variable) instead of one
  request per section and device, e.g. 2 instead of 226 requests (0.8 s instead of 28 s). It raises an
  `APIError` if the Web HMI rejects the request without naming a requested variable
- `read_data()` with extra attributes and `get_heating_curve_points()` with a heating curve name only read the
  points of the heating curves in use or requested, instead of all heating curves
- `get_available_heating_curves()` reads the heating curve names without attributes (`attr="0"`), as only the
  names are used
- Moved the documentation from MkDocs on `api.superbox.one` to Docusaurus on GitHub Pages
  (<https://superbox-dev.github.io/keba_keenergy_api/>)
- Shortened the `README.md` to a quick start and moved the detailed examples and write warnings to the
  [Usage](https://superbox-dev.github.io/keba_keenergy_api/usage) page
- Applied the request timeout of `API_DEFAULT_TIMEOUT` (10 seconds) also to the requests with a passed session,
  which used the timeout of the session before (5 minutes by default in `aiohttp`)
- Showed the documentation only in the dark theme with the colors of contributors.home-assistant.io, the brand logo
  of the integration on the project card, a link to the website of the integration in the menu and a wider right
  column on smaller screens
- Focused the search of the documentation with `/` instead of `Ctrl`/`Cmd` + `K`, styled the search and the cards of
  the category pages like contributors.home-assistant.io and made the header translucent

### Fixed

- Fixed `IndexError` in single getters with a `position` greater than 1
- Fixed `InvalidJsonError` not being raised for invalid JSON responses
- Fixed timeouts not being raised as `APIError` (now `APITimeoutError`, also for the `aiohttp` timeouts
  `ServerTimeoutError`, `ConnectionTimeoutError` and `SocketTimeoutError`)
- Fixed `UnboundLocalError` for HTTP status codes between 301 and 399, e.g. a redirect of a reverse proxy.
  Every HTTP status other than 2xx now raises an `APIError`
- Fixed `KeyError` instead of `APIError` in single getters with a `position` lower than 1
- Fixed `write_data()` writing a literal `%s` path for a single value of a device section
- Fixed `write_data()` raising a `TypeError` instead of `APIError` for more than one value of a system-wide
  section, and a `TypeError` for a single value of `SolarCircuit.PRIORITY_1_BEFORE_2`
- Fixed `KeyError` in `read_data()` with extra attributes if the heating curve is not in the line table pool
- Fixed `IndexError` in `get_heating_curve_points()` if the control unit reports more than 16 points
- Fixed `KeyError` in `get_info()`, `get_hmi_info()` and `get_device_info()` if the response has no `ret`
- Fixed the documented unit of the photovoltaics `get_daily_energy()` and `get_total_energy()` and of the heat pump
  `get_heating_energy()`, `get_cooling_energy()`, `get_hot_water_energy()` and `get_total_thermal_energy()`
  (J instead of kWh)
- Fixed the documented unit of the pump and compressor speeds (a fraction from 0 to 1 instead of percent),
  including `set_compressor_night_speed()` and the solar circuit `get_pump_1_speed()` and `get_pump_2_speed()`
- Fixed the docstrings of `get_away_end_date()` and `set_away_end_date()` of the heating circuit, which described
  the start date
- Fixed an unclosed `ClientSession` per request if the shared session was already closed, e.g. an endpoint client
  used after `async with`

[issue-67]: https://github.com/superbox-dev/keba_keenergy/issues/67

## [2.12.2] - 2026-07-18

### Fixed

- Fixed the aiohttp deprecation warning "BasicAuth is deprecated and will be removed in aiohttp 4.0"
  by sending the `Authorization` header with `aiohttp.encode_basic_auth()`

## [2.12.1] - 2026-06-24

### Security

- Bumped aiohttp in `uv.lock` from `3.13.5` to `3.14.1` ([PR #118][pr-118], [PR #119][pr-119])

[pr-118]: https://github.com/superbox-dev/keba_keenergy_api/pull/118
[pr-119]: https://github.com/superbox-dev/keba_keenergy_api/pull/119

## [2.12.0] - 2026-05-19

### Added

- Added endpoint `has_var_speed_pump()` to the heating circuit
- Added endpoint `get_excess_energy_target_temperature()` to the heating circuit
- Added endpoint `set_excess_energy_target_temperature()` to the heating circuit
- Added endpoint `get_excess_energy_target_temperature_hysteresis()` to the heating circuit
- Added endpoint `set_excess_energy_target_temperature_hysteresis()` to the heating circuit
- Added endpoint `get_excess_energy_target_cooling_temperature()` to the heating circuit
- Added endpoint `set_excess_energy_target_cooling_temperature()` to the heating circuit
- Added endpoint `get_excess_energy_target_cooling_temperature_hysteresis()` to the heating circuit
- Added endpoint `set_excess_energy_target_cooling_temperature_hysteresis()` to the heating circuit
- Added endpoint `get_excess_energy_heating_limit_day()` to the heating circuit
- Added endpoint `set_excess_energy_heating_limit_day()` to the heating circuit
- Added endpoint `get_excess_energy_cooling_limit_day()` to the heating circuit
- Added endpoint `set_excess_energy_cooling_limit_day()` to the heating circuit
- Added endpoint `get_excess_energy_heating_limit_night()` to the heating circuit
- Added endpoint `set_excess_energy_heating_limit_night()` to the heating circuit
- Added endpoint `get_excess_energy_cooling_limit_night()` to the heating circuit
- Added endpoint `set_excess_energy_cooling_limit_night()` to the heating circuit
- Added endpoint `get_pump_state()` to the heating circuit
- Added endpoint `get_mixer_position()` to the heating circuit
- Added endpoint `get_excess_energy_mode()` to the heating circuit
- Added endpoint `get_use_excess_energy()` to the heating circuit
- Added endpoint `set_use_excess_energy()` to the heating circuit
- Added endpoint `get_excess_energy_operating_time()` to the heat pump
- Added endpoint `get_excess_energy_max_runtime()` to the heat pump
- Added endpoint `get_excess_energy_activation_counter()` to the heat pump
- Added endpoint `get_excess_energy_consumption()` to the heat pump
- Added endpoint `get_heating_excess_energy_consumption()` to the heat pump
- Added endpoint `get_cooling_excess_energy_consumption()` to the heat pump
- Added endpoint `get_hot_water_excess_energy_consumption()` to the heat pump
- Added endpoint `get_consuming_excess_energy()` to the heat pump
- Added endpoint `get_excess_energy_target_temperature()` to the buffer tank
- Added endpoint `set_excess_energy_target_temperature()` to the buffer tank
- Added endpoint `get_excess_energy_target_temperature_hysteresis()` to the buffer tank
- Added endpoint `set_excess_energy_target_temperature_hysteresis()` to the buffer tank
- Added endpoint `get_outdoor_temperature_excess_energy_limit()` to the buffer tank
- Added endpoint `set_outdoor_temperature_excess_energy_limit()` to the buffer tank
- Added endpoint `get_excess_energy_mode()` to the buffer tank
- Added endpoint `get_use_excess_energy()` to the buffer tank
- Added endpoint `set_use_excess_energy()` to the buffer tank
- Added endpoint `get_excess_energy_target_temperature()` to the hot water tank
- Added endpoint `set_excess_energy_target_temperature()` to the hot water tank
- Added endpoint `get_excess_energy_target_temperature_hysteresis()` to the hot water tank
- Added endpoint `set_excess_energy_target_temperature_hysteresis()` to the hot water tank
- Added endpoint `get_excess_energy_mode()` to the hot water tank
- Added endpoint `get_use_excess_energy()` to the hot water tank
- Added endpoint `set_use_excess_energy()` to the hot water tank
- Added endpoint `get_use_excess_energy()` to the external heat source
- Added endpoint `set_use_excess_energy()` to the external heat source
- Added endpoint `get_excess_energy_operating_time()` to the external heat source
- Added endpoint `get_excess_energy_max_runtime()` to the external heat source
- Added endpoint `get_excess_energy_activation_counter()` to the external heat source
- Added endpoint `get_consuming_excess_energy()` to the external heat source
- Added endpoint `get_min_runtime_excess_energy()` to the external heat source
- Added endpoint `set_min_runtime_excess_energy()` to the external heat source
- Added endpoint `get_excess_energy_active()` to the photovoltaics
- Added endpoint `get_mixer_position()` to the passive cooling
- Added the meter type constants `HeatPump.ELECTRIC_ENERGY_METER_TYPE`, `HeatPump.HEAT_METER_TYPE`,
  `HeatPump.COOL_METER_TYPE` and `HeatPump.HOT_WATER_METER_TYPE`

### Changed

- **Breaking:** Renamed `Photovoltaic` to `Photovoltaics` and `SectionPrefix.PHOTOVOLTAIC` to
  `SectionPrefix.PHOTOVOLTAICS`, so `read_data()` returns the photovoltaics values under `photovoltaics`
- **Breaking:** Replaced `EndpointProperties` with `FloatEndpoint`, `IntegerEndpoint` and `StringEndpoint`, and
  renamed `SolarCircuitPriority1Before2EndpointProperties` to `SolarCircuitPriority1Before2StringEndpoint`

### Fixed

- Fixed `has_pump()` of the heating circuit reading `hasVarSpeedPump` instead of `hasPump`
- Fixed `ValueError` instead of `APIError` if a value can't be converted to the type of the endpoint

## [2.11.0] - 2026-04-13

### Added

- Added the passive cooling section (`passive_cooling`)
- Added endpoint `get_mode()` to the heating circuit
- Added endpoint `get_cooling_curve()` to the heating circuit
- Added endpoint `set_cooling_curve()` to the heating circuit
- Added endpoint `get_cooling_curve_slope()` to the heating circuit
- Added endpoint `set_cooling_curve_slope()` to the heating circuit
- Added endpoint `get_cooling_curve_offset()` to the heating circuit
- Added endpoint `set_cooling_curve_offset()` to the heating circuit
- Added endpoint `get_target_cooling_temperature_day()` to the heating circuit
- Added endpoint `set_target_cooling_temperature_day()` to the heating circuit
- Added endpoint `set_heating_limit_day()` to the heating circuit
- Added endpoint `get_cooling_limit_day()` to the heating circuit
- Added endpoint `set_cooling_limit_day()` to the heating circuit
- Added endpoint `get_target_cooling_temperature_night()` to the heating circuit
- Added endpoint `set_target_cooling_temperature_night()` to the heating circuit
- Added endpoint `set_heating_limit_night()` to the heating circuit
- Added endpoint `get_cooling_limit_night()` to the heating circuit
- Added endpoint `set_cooling_limit_night()` to the heating circuit
- Added endpoint `has_mixer()` to the heating circuit
- Added endpoint `has_return_flow_temperature()` to the heating circuit
- Added endpoint `has_pump()` to the heating circuit
- Added endpoint `has_active_cooling()` to the heat pump
- Added endpoint `has_outdoor_temperature()` to the system
- Added endpoint `has_fresh_water_module()` to the hot water tank
- Added endpoint `get_temperature()` to the passive cooling
- Added endpoint `get_switch_valve_position()` to the passive cooling
- Added endpoint `get_circulation_pump_speed()` to the passive cooling
- Added endpoint `get_mixer_target_temperature()` to the passive cooling
- Added endpoint `get_mixer_flow_temperature()` to the passive cooling

### Changed

- **Breaking:** Renamed the hot water tank endpoint `get_hot_water_flow()` to `get_fresh_water_flow()`
- **Breaking:** Renamed the constants `HeatCircuit.FLOW_TEMPERATURE` to `HeatCircuit.MIXER_FLOW_TEMPERATURE`,
  `HeatPump.CIRCULATION_PUMP` to `HeatPump.CIRCULATION_PUMP_SPEED` and `HotWaterTank.HOT_WATER_FLOW`
  to `HotWaterTank.FRESH_WATER_FLOW`

## [2.10.2] - 2026-04-03

### Security

- Bumped aiohttp in `uv.lock` from `3.13.3` to `3.13.4` ([CVE-2026-34513][cve-2026-34513], [PR #107][pr-107])

[cve-2026-34513]: https://github.com/advisories/GHSA-hcc4-c3v8-rx92
[pr-107]: https://github.com/superbox-dev/keba_keenergy_api/pull/107

## [2.10.1] - 2026-02-26

### Fixed

- Fixed the value type of `HeatCircuit.PUMP_SPEED`

## [2.10.0] - 2026-02-26

### Added

- Added endpoint `get_pump_speed()` to the heating circuit

## [2.9.1] - 2026-02-20

### Added

- Added endpoint `get_available_heating_curves()` to the heating circuit

### Changed

- **Breaking:** Removed the `HeatCircuitHeatingCurve` enum. The heating curve names are now read from the control unit

### Fixed

- Fixed all endpoints that used the static heating curve name mapping

## [2.9.0] - 2026-02-17

### Added

- Added endpoint `get_target_overheating()` to the heat pump ([Issue #100][issue-100])
- Added endpoint `get_current_overheating()` to the heat pump ([Issue #100][issue-100])
- Added endpoint `get_expansion_valve_position()` to the heat pump ([Issue #100][issue-100])
- Added endpoint `get_circulation_return_temperature()` to the hot water tank ([Issue #97][issue-97])
- Added endpoint `get_circulation_pump_state()` to the hot water tank ([Issue #97][issue-97])
- Added endpoint `get_heating_curve_offset()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `set_heating_curve_offset()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `get_heating_curve_slope()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `set_heating_curve_slope()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `get_use_heating_curve()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `set_use_heating_curve()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `get_heating_curve()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `set_heating_curve()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `get_heating_curve_points()` to the heating circuit ([Issue #97][issue-97])
- Added endpoint `set_heating_curve_points()` to the heating circuit ([Issue #97][issue-97])
- Added the heating curve points as extra attributes to the heating curve ([Issue #97][issue-97])

### Changed

- Removed `BaseEnum.from_value()`

[issue-97]: https://github.com/superbox-dev/keba_keenergy_api/issues/97
[issue-100]: https://github.com/superbox-dev/keba_keenergy_api/issues/100

## [2.8.1] - 2026-01-28

### Changed

- Added a note to the endpoint documentation: writing values should remain within normal limits,
  as is the case with typical use of the Web HMI. **Permanent and very frequent writing of values reduces the lifetime
  of the built-in flash memory.**

## [2.8.0] - 2026-01-24

### Added

- Added endpoint `get_away_start_date()` to the heating circuit
- Added endpoint `set_away_start_date()` to the heating circuit
- Added endpoint `get_away_end_date()` to the heating circuit
- Added endpoint `set_away_end_date()` to the heating circuit
- Added endpoint `get_timezone()` to the system

## [2.7.2] - 2026-01-23

### Added

- Added endpoint `get_selected_target_temperature()` to the heating circuit

### Fixed

- Reverted `get_target_temperature()` of the heating circuit to the behaviour before 2.7.1.
  The selected target temperature is now available with `get_selected_target_temperature()`

## [2.7.1] - 2026-01-23

### Fixed

- Changed `get_target_temperature()` of the heating circuit to return the selected target temperature
  without the offset (`values.selectedSetTemp`)

## [2.7.0] - 2026-01-17

### Added

- Added support for Python 3.14
- Added the switch valve section (`switch_valve`) with endpoint `get_position()`
- Added endpoint `get_number_of_switch_valves()` to the system
- Added endpoint `has_compressor_failure()` to the heat pump
- Added endpoint `has_source_failure()` to the heat pump
- Added endpoint `has_source_actuator_failure()` to the heat pump
- Added endpoint `has_three_phase_failure()` to the heat pump
- Added endpoint `has_source_pressure_failure()` to the heat pump
- Added endpoint `has_vfd_failure()` to the heat pump
- Added endpoint `get_fresh_water_module_pump_speed()` to the hot water tank
- Added endpoint `get_mixer_return_flow_temperature()` to the heating circuit
- Added `filter_request()` to get only the endpoints that are supported by the Web HMI
- Added the documentation at <https://api.superbox.one>

### Changed

- **Breaking:** Renamed the heating circuit endpoint `get_flow_temperature()` to `get_mixer_flow_temperature()`
- **Breaking:** Removed the deprecated heat pump endpoints `get_circulation_pump()` and `get_compressor()`,
  use `get_circulation_pump_speed()` and `get_compressor_speed()` instead
- **Breaking:** Replaced the on/off enums (e.g. `HeatPumpHeatRequest`, `HotWaterTankHotWaterFlow`,
  `SystemHasPhotovoltaics`) with `BoolEnum`
- **Breaking:** Removed the unused heat pump meter constants, e.g. `HeatPump.DAILY_HEATING_ENERGY`

## [2.6.0] - 2026-01-11

### Added

- Added endpoint `get_priority_1_before_2()` to the solar circuit
- Added endpoint `set_priority_1_before_2()` to the solar circuit

## [2.5.2] - 2026-01-09

### Added

- Added endpoint `get_substate()` to the heat pump
- Added endpoint `get_source_pump_speed()` to the heat pump
- Added endpoint `get_condenser_temperature()` to the heat pump
- Added endpoint `get_vaporizer_temperature()` to the heat pump

### Fixed

- Changed the basic auth encoding from `latin-1` to `utf-8`

## [2.5.1] - 2026-01-06

### Fixed

- Fixed the buffer tank operating mode: renamed `BufferTankOperatingMode.AUTO` to `BufferTankOperatingMode.ON`

## [2.5.0] - 2026-01-05

### Added

- Added the buffer tank section (`buffer_tank`)
- Added endpoint `get_name()` to the buffer tank
- Added endpoint `get_current_top_temperature()` to the buffer tank
- Added endpoint `get_current_bottom_temperature()` to the buffer tank
- Added endpoint `get_operating_mode()` to the buffer tank
- Added endpoint `set_operating_mode()` to the buffer tank
- Added endpoint `get_standby_temperature()` to the buffer tank
- Added endpoint `set_standby_temperature()` to the buffer tank
- Added endpoint `get_target_temperature()` to the buffer tank
- Added endpoint `get_heat_request()` to the buffer tank
- Added endpoint `get_cool_request()` to the buffer tank
- Added endpoint `get_number_of_buffer_tanks()` to the system
- Added endpoint `get_name()` to the hot water tank

### Changed

- **Breaking:** Removed the unused heating circuit endpoints `get_external_cool_request()` and
  `get_external_heat_request()`

## [2.4.0] - 2026-01-03

### Added

- Added the solar circuit section (`solar_circuit`)
- Added endpoint `get_name()` to the solar circuit
- Added endpoint `get_operating_mode()` to the solar circuit
- Added endpoint `set_operating_mode()` to the solar circuit
- Added endpoint `get_source_temperature()` to the solar circuit
- Added endpoint `get_pump_1_speed()` to the solar circuit
- Added endpoint `get_pump_2_speed()` to the solar circuit
- Added endpoint `get_current_temperature_1()` to the solar circuit
- Added endpoint `get_current_temperature_2()` to the solar circuit
- Added endpoint `get_target_temperature_1()` to the solar circuit
- Added endpoint `set_target_temperature_1()` to the solar circuit
- Added endpoint `get_target_temperature_2()` to the solar circuit
- Added endpoint `set_target_temperature_2()` to the solar circuit
- Added endpoint `get_heat_request_1()` to the solar circuit
- Added endpoint `get_heat_request_2()` to the solar circuit
- Added endpoint `get_heating_energy()` to the solar circuit
- Added endpoint `get_daily_energy()` to the solar circuit
- Added endpoint `get_actual_power()` to the solar circuit
- Added endpoint `get_circulation_pump_speed()` to the heat pump
- Added endpoint `get_compressor_speed()` to the heat pump

### Deprecated

- Deprecated the heat pump endpoint `get_circulation_pump()`, use `get_circulation_pump_speed()` instead
- Deprecated the heat pump endpoint `get_compressor()`, use `get_compressor_speed()` instead

## [2.3.1] - 2025-10-18

### Fixed

- Fixed API error when reading an endpoint with zero positions:
  `Reading variable: APPL.CtrlAppl.sParam.extHeatSource[%s].param.operatingMode failed (-1)`

## [2.3.0] - 2025-10-16

### Added

- Added endpoint `get_hmi_info()` to the system
- Added endpoint `get_cpu_usage()` to the system
- Added endpoint `get_webview_cpu_usage()` to the system
- Added endpoint `get_webserver_cpu_usage()` to the system
- Added endpoint `get_control_cpu_usage()` to the system
- Added endpoint `get_ram_usage()` to the system
- Added endpoint `get_free_ram()` to the system

## [2.2.0] - 2025-10-13

### Added

- Added endpoint `get_heat_request()` to the external heat source
- Added endpoint `get_operating_time()` to the external heat source
- Added endpoint `get_max_runtime()` to the external heat source
- Added endpoint `get_activation_counter()` to the external heat source
- Added endpoint `get_operating_time()` to the heat pump
- Added endpoint `get_max_runtime()` to the heat pump
- Added endpoint `get_activation_counter()` to the heat pump

## [2.1.0] - 2025-10-11

### Added

- Added the external heat source section (`external_heat_source`) and the photovoltaics section (`photovoltaics`)
- Added endpoint `get_excess_power()` to the photovoltaics
- Added endpoint `get_daily_energy()` to the photovoltaics
- Added endpoint `get_total_energy()` to the photovoltaics
- Added endpoint `get_operating_mode()` to the external heat source
- Added endpoint `set_operating_mode()` to the external heat source
- Added endpoint `get_target_temperature()` to the external heat source
- Added endpoint `has_photovoltaics()` to the system
- Added endpoint `get_number_of_external_heat_sources()` to the system
- Added endpoint `get_cool_request()` to the heating circuit
- Added endpoint `get_flow_temperature()` to the heating circuit
- Added endpoint `get_return_flow_temperature()` to the heating circuit
- Added support for basic authentication with `username` and `password` (required for newer KeEnergy.WebHmi versions)
- Added `AuthenticationError`, raised for HTTP status `401`
- Added the HTTP status code to the `APIError` exception

## [2.0.0] - 2025-09-30

### Added

- Added endpoint `has_passive_cooling()` to the heat pump
- Added endpoint `get_compressor_use_night_speed()` to the heat pump
- Added endpoint `set_compressor_use_night_speed()` to the heat pump
- Added endpoint `get_compressor_night_speed()` to the heat pump
- Added endpoint `set_compressor_night_speed()` to the heat pump
- Added endpoint `get_max_compressor_night_speed()` to the heat pump
- Added endpoint `get_min_compressor_night_speed()` to the heat pump
- Added endpoint `get_flow_temperature_setpoint()` to the heating circuit
- Added endpoint `get_hot_water_flow()` to the hot water tank, to see if the fresh water module is active
- Added endpoint `get_fresh_water_module_temperature()` to the hot water tank
- Added the heating circuit heat request states `FLOW_OFF`, `ROOM_OFF`, `INFLOW_OFF`
- Added the heating circuit operating mode `ROOM_CONTROL`
- Added the heat pump states `PUMP_DOWN`, `SHUTDOWN` and `ERROR`

### Changed

- **Breaking:** Renamed the hot water tank endpoints:
  - `get_temperature()` to `get_current_temperature()`
  - `get_lower_limit_temperature()` to `get_min_target_temperature()`
  - `get_upper_limit_temperature()` to `get_max_target_temperature()`
  - `get_min_temperature()` / `set_min_temperature()` to `get_standby_temperature()` / `set_standby_temperature()`
  - `get_max_temperature()` / `set_max_temperature()` to `get_target_temperature()` / `set_target_temperature()`
- **Breaking:** Renamed the heat pump endpoints:
  - `get_inflow_temperature()` to `get_flow_temperature()`
  - `get_reflux_temperature()` to `get_return_flow_temperature()`
  - `get_electrical_power()` to `get_compressor_power()`
  - `get_heating_electrical_energy()` to `get_heating_energy_consumption()`
  - `get_cooling_electrical_energy()` to `get_cooling_energy_consumption()`
  - `get_domestic_hot_water_energy()` to `get_hot_water_energy()`
  - `get_domestic_hot_water_electrical_energy()` to `get_hot_water_energy_consumption()`
  - `get_domestic_hot_water_spf()` to `get_hot_water_spf()`
  - `get_total_energy()` to `get_total_thermal_energy()`
  - `get_total_electrical_energy()` to `get_total_energy_consumption()`
  - `get_spf()` to `get_total_spf()`
- **Breaking:** Renamed the heating circuit endpoints:
  - `get_temperature()` to `get_target_temperature()`
  - `get_day_temperature()` / `set_day_temperature()` to `get_target_temperature_day()` / `set_target_temperature_day()`
  - `get_night_temperature()` / `set_night_temperature()` to `get_target_temperature_night()` /
    `set_target_temperature_night()`
  - `get_holiday_temperature()` / `set_holiday_temperature()` to `get_target_temperature_away()` /
    `set_target_temperature_away()`
  - `get_temperature_offset()` / `set_temperature_offset()` to `get_target_temperature_offset()` /
    `set_target_temperature_offset()`
  - `get_day_temperature_threshold()` to `get_heating_limit_day()`
  - `get_night_temperature_threshold()` to `get_heating_limit_night()`
- **Breaking:** Renamed the endpoint constants accordingly, e.g. `HotWaterTank.TEMPERATURE` to
  `HotWaterTank.CURRENT_TEMPERATURE`
- **Breaking:** Renamed `HeatCircuitOperatingMode.EXTERN` to `HeatCircuitOperatingMode.EXTERNAL` and
  `HeatCircuitHeatRequest.OUTDOOR_TEMPERATURE_OFF` to `HeatCircuitHeatRequest.OUTDOOR_OFF`
- **Breaking:** Changed the values of the on/off enums (e.g. `HeatPumpHeatRequest`) from `"true"` / `"false"`
  to `1` / `0`

### Fixed

- Added the missing human-readable value `room_off` for the heating circuit heat request state `4`

## [1.15.0] - 2025-09-14

### Added

- Added endpoint `get_electrical_power()` to the heat pump
- Added endpoint `get_heating_power()` to the heat pump
- Added endpoint `get_hot_water_power()` to the heat pump
- Added endpoint `get_cop()` to the heat pump
- Added endpoint `get_heating_energy()` to the heat pump
- Added endpoint `get_heating_electrical_energy()` to the heat pump
- Added endpoint `get_heating_spf()` to the heat pump
- Added endpoint `get_cooling_energy()` to the heat pump
- Added endpoint `get_cooling_electrical_energy()` to the heat pump
- Added endpoint `get_cooling_spf()` to the heat pump
- Added endpoint `get_domestic_hot_water_energy()` to the heat pump
- Added endpoint `get_domestic_hot_water_electrical_energy()` to the heat pump
- Added endpoint `get_domestic_hot_water_spf()` to the heat pump
- Added endpoint `get_total_energy()` to the heat pump
- Added endpoint `get_total_electrical_energy()` to the heat pump
- Added endpoint `get_spf()` to the heat pump

## [1.14.0] - 2025-08-27

### Added

- Added endpoint `has_room_temperature()` to the heating circuit
- Added endpoint `has_room_humidity()` to the heating circuit

## [1.13.0] - 2025-08-26

### Added

- Added endpoint `get_room_temperature()` to the heating circuit
- Added endpoint `get_room_humidity()` to the heating circuit
- Added endpoint `get_dew_point()` to the heating circuit

## [1.12.10] - 2025-08-19

### Added

- Added `keba_keenergy_api/py.typed` to support static type checking, e.g. with mypy

## [1.12.9] - 2024-12-21

### Added

- Added support for Python 3.13 (required for Home Assistant 2024.12)

## [1.12.8] - 2024-12-21

### Changed

- Allowed all aiohttp versions `3.*`

## [1.12.7] - 2024-08-24

### Changed

- Bumped aiohttp to `~=3.10.0b1`

## [1.12.6] - 2024-03-27

### Added

- Added support for Python 3.12

### Fixed

- Added the missing heating circuit heat request state `OUTDOOR_TEMPERATURE_OFF`

## [1.12.4] - 2024-01-31

### Changed

- Bumped aiohttp to `~=3.9.3`

## [1.12.3] - 2023-12-08

### Changed

- Bumped aiohttp to `3.9.1`

## [1.12.2] - 2023-11-19

### Changed

- **Breaking:** Renamed `HeatCircuitOperatingMode.AWAY` to `HeatCircuitOperatingMode.HOLIDAY`

## [1.12.1] - 2023-11-19

### Changed

- **Breaking:** Renamed the heating circuit endpoints `get_offset_temperature()` / `set_offset_temperature()` to
  `get_temperature_offset()` / `set_temperature_offset()`

## [1.12.0] - 2023-11-18

### Added

- Added endpoint `get_operating_mode()` to the system
- Added endpoint `set_operating_mode()` to the system
- Added endpoint `get_operating_mode()` to the heat pump
- Added endpoint `set_operating_mode()` to the heat pump
- Added endpoint `get_external_cool_request()` to the heating circuit
- Added endpoint `get_external_heat_request()` to the heating circuit
- Added the heat pump states `AUTO_COOL` and `DEFROST`

### Changed

- **Breaking:** Merged the `device` and `options` sections into the new `system` section:
  - `device.get_device_info()` to `system.get_device_info()`
  - `device.get_system_info()` to `system.get_info()`
  - `options.get_number_of_*()` to `system.get_number_of_*()`
  - `get_outdoor_temperature()` of the client to `system.get_outdoor_temperature()`
  - removed `device.get_name()`, `device.get_serial_number()`, `device.get_revision_number()` and
    `device.get_variant_number()`, use `system.get_device_info()` instead
- **Breaking:** Replaced `read_values()` and `read_values_grouped_by_section()` with `read_data()`,
  which returns the values grouped by section
- **Breaking:** Renamed `write_values()` to `write_data()`
- **Breaking:** Renamed the heat pump endpoint `get_status()` to `get_state()` and `HeatPumpStatus` to `HeatPumpState`,
  with `AUTO` renamed to `AUTO_HEAT`
- **Breaking:** Renamed `SystemPrefix` to `SectionPrefix` and the section enum `Options` / `Outdoor` to `System`
- Converted the attribute keys to lower case

## [1.11.1] - 2023-10-25

### Fixed

- Fixed the response keys of `read_values_grouped_by_section()`

## [1.11.0] - 2023-10-25

### Added

- Added endpoint `get_heat_request()` to the heat pump
- Added endpoint `get_heat_request()` to the heating circuit
- Added endpoint `get_heat_request()` to the hot water tank

## [1.10.1] - 2023-10-24

### Changed

- Removed the trailing underscore from the `SystemPrefix` values

## [1.10.0] - 2023-10-23

### Added

- Added the heat pump state `INFLOW`
- Added endpoint `set_holiday_temperature()` to the heating circuit

## [1.9.0] - 2023-10-22

### Added

- Added the heating circuit operating modes `AWAY` and `PARTY`

## [1.8.1] - 2023-10-22

### Added

- Added `APIError` exception when a value can't be converted to a human-readable value

### Changed

- Allowed setting the operating mode in lower and upper case

## [1.8.0] - 2023-10-20

### Added

- Added `read_values_grouped_by_section()`
- Added `extra_attributes` to `read_values()` to add the `attributes` to the response

## [1.7.0] - 2023-10-19

### Added

- Added endpoint `get_lower_limit_temperature()` to the hot water tank
- Added endpoint `get_upper_limit_temperature()` to the hot water tank

## [1.6.2] - 2023-10-18

### Changed

- Changed the sections of `KebaKeEnergyAPI` (`device`, `options`, `hot_water_tank`, `heat_pump`, `heat_circuit`)
  to properties for better mocking with pytest

## [1.6.1] - 2023-10-17

### Fixed

- `InvalidJsonError` now inherits from `APIError`

## [1.6.0] - 2023-10-14

### Added

- Added endpoint `get_name()` to the heat pump
- Added endpoint `get_name()` to the heating circuit
- Added `human_readable` argument to `read_values()` to get a human-readable name instead of a number,
  e.g. for `hot_water_tank.get_operating_mode()`

## [1.5.0] - 2023-10-13

### Added

- Added `get_system_info()` to read all system information

## [1.4.3] - 2023-10-13

### Fixed

- Fixed error when mixing endpoints with and without position

## [1.4.2] - 2023-10-13

### Added

- Added `device_url` to the client to get the device URL

## [1.4.1] - 2023-10-11

### Changed

- Downgraded aiohttp from `3.8.6` to `3.8.5` for Home Assistant compatibility

## [1.4.0] - 2023-10-11

### Added

- Added `get_device_info()` to read all device information, e.g. the serial number, as `dict`

### Changed

- Bumped aiohttp from `3.8.5` to `3.8.6`

## [1.3.0] - 2023-10-10

### Added

- Added `get_number_of_hot_water_tanks()` to read the number of hot water tanks
- Added `get_number_of_heat_pumps()` to read the number of heat pumps
- Added `get_number_of_heating_circuits()` to read the number of heating circuits
- Added automatic position numbers for `read_values()` depending on the hardware

### Changed

- **Breaking:** Removed the `position` argument from `write_values()`, the request now takes a tuple with
  one value per position

## [1.2.0] - 2023-10-09

### Added

- Added `read_values()` to read multiple values with one HTTP request
- Added `write_values()` to write multiple values with one HTTP request

## [1.1.0] - 2023-10-08

### Added

- Added device information endpoints `get_name()`, `get_serial_number()`, `get_revision_number()` and
  `get_variant_number()`
- Added SSL support for aiohttp

## [1.0.0] - 2023-10-07

### Added

- Initial release

[Unreleased]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.14.0...HEAD
[2.14.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.13.0...v2.14.0
[2.13.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.12.2...v2.13.0
[2.12.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.12.1...v2.12.2
[2.12.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.12.0...v2.12.1
[2.12.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.11.0...v2.12.0
[2.11.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.10.2...v2.11.0
[2.10.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.10.1...v2.10.2
[2.10.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.10.0...v2.10.1
[2.10.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.9.1...v2.10.0
[2.9.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.9.0...v2.9.1
[2.9.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.8.1...v2.9.0
[2.8.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.8.0...v2.8.1
[2.8.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.7.2...v2.8.0
[2.7.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.7.1...v2.7.2
[2.7.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.7.0...v2.7.1
[2.7.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.6.0...v2.7.0
[2.6.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.5.2...v2.6.0
[2.5.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.5.1...v2.5.2
[2.5.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.5.0...v2.5.1
[2.5.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.4.0...v2.5.0
[2.4.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.3.1...v2.4.0
[2.3.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.15.0...v2.0.0
[1.15.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.14.0...v1.15.0
[1.14.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.13.0...v1.14.0
[1.13.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.10...v1.13.0
[1.12.10]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.9...v1.12.10
[1.12.9]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.8...v1.12.9
[1.12.8]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.7...v1.12.8
[1.12.7]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.6...v1.12.7
[1.12.6]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.4...v1.12.6
[1.12.4]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.3...v1.12.4
[1.12.3]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.2...v1.12.3
[1.12.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.1...v1.12.2
[1.12.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.12.0...v1.12.1
[1.12.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.11.1...v1.12.0
[1.11.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.11.0...v1.11.1
[1.11.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.10.1...v1.11.0
[1.10.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.10.0...v1.10.1
[1.10.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.9.0...v1.10.0
[1.9.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.8.1...v1.9.0
[1.8.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.6.2...v1.7.0
[1.6.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.4.3...v1.5.0
[1.4.3]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.4.2...v1.4.3
[1.4.2]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/superbox-dev/keba_keenergy_api/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/superbox-dev/keba_keenergy_api/releases/tag/v1.0.0

<!--end-->
