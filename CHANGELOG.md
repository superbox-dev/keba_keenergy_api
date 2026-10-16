# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `read_message_ids()` to read the message ids (`state.msgId`) of sensors with one request.
  A message id other than `0` means that the sensor is not in use, e.g. not connected ([Issue #67][issue-67])
- Added `has_message_id` and `message_id_path` to `Endpoint` for all 31 confirmed `values.actValue` sensors
- Added the optional `position` argument to `has_mixer()` of the heating circuit and `has_fresh_water_module()`
  of the hot water tank
- Added `APITimeoutError`, raised when a request times out. It inherits from `APIError` and `TimeoutError`

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

### Fixed

- Fixed `IndexError` in single getters with a `position` greater than 1
- Fixed `InvalidJsonError` not being raised for invalid JSON responses
- Fixed timeouts not being raised as `APIError` (now `APITimeoutError`)
- Fixed `UnboundLocalError` for HTTP status codes between 301 and 399, e.g. a redirect of a reverse proxy.
  Every HTTP status other than 2xx now raises an `APIError`
- Fixed `KeyError` instead of `APIError` in single getters with a `position` lower than 1
- Fixed `write_data()` writing a literal `%s` path for a single value of a device section
- Fixed `write_data()` raising a `TypeError` instead of `APIError` for more than one value of a system-wide
  section, and a `TypeError` for a single value of `SolarCircuit.PRIORITY_1_BEFORE_2`
- Fixed `KeyError` in `read_data()` with extra attributes if the heating curve is not in the line table pool
- Fixed `IndexError` in `get_heating_curve_points()` if the control unit reports more than 16 points
- Fixed `KeyError` in `get_info()`, `get_hmi_info()` and `get_device_info()` if the response has no `ret`

<!--start-->

## [2.12.2] - 2026-07-18

### Fixed

- Fixed deprecation warning: "BasicAuth is deprecated and will be removed in aiohttp 4.0"

## [2.12.1] - 2026-06-24

### Security

- Bumped aiohttp from `3.13.5` to `3.14.0`

## [2.12.0] - 2026-05-08

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

## [2.11.0] - 2026-04-13

### Added

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

## [2.10.2] - 2026-04-03

### Security

- Bumped aiohttp from `3.13.3` to `3.13.4` ([CVE-2026-34513][cve-2026-34513])

## [2.10.1] - 2026-02-26

### Fixed

- Fixed the value type of `HeatCircuit.PUMP_SPEED`

## [2.10.0] - 2026-02-26

### Added

- Added endpoint `get_pump_speed()` to the heating circuit

## [2.9.1] - 2026-02-20

### Added

- Added endpoint `get_available_heating_curves()` to the heating circuit

### Fixed

- Fixed all endpoints that used a static heating curve name mapping

## [2.9.0] - 2026-02-17

### Added

- Added endpoint `get_target_overheating()` to the heat pump ([Issue #100][issue-100])
- Added endpoint `get_current_overheating()` to the heat pump ([Issue #100][issue-100])
- Added endpoint `get_expansion_valve_position()` to the heat pump ([Issue #100][issue-100])
- Added endpoint `get_circulation_return_temperature()` to the hot water tank ([Issue #100][issue-100])
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

## [2.8.1] - 2026-01-28

### Changed

- Added important information to the endpoint documentation: writing values should remain within normal limits,
  as is the case with typical use of the Web HMI. **Permanent and very frequent writing of values reduces the lifetime
  of the built-in flash memory.**

## [2.8.0] - 2026-01-24

### Added

- Added endpoints `get_away_start_date()`, `set_away_start_date()`, `get_away_end_date()` and `set_away_end_date()`
  to the heating circuit
- Added endpoint `get_timezone()` to the system

## [2.7.2] - 2026-01-23

### Added

- Added endpoint `get_selected_target_temperature()` to the heating circuit

### Fixed

- Reverted `get_target_temperature()` of the heating circuit to the original behavior

## [2.7.1] - 2026-01-23

### Fixed

- Fixed the target temperature value: the endpoint returns the raw target temperature without the offset

## [2.7.0] - 2026-01-17

### Added

- Added support for Python 3.14
- Added endpoints for switch valves
- Added endpoint `has_compressor_failure()` to the heat pump
- Added endpoint `has_source_failure()` to the heat pump
- Added endpoint `has_source_actuator_failure()` to the heat pump
- Added endpoint `has_three_phase_failure()` to the heat pump
- Added endpoint `has_source_pressure_failure()` to the heat pump
- Added endpoint `has_vfd_failure()` to the heat pump
- Added endpoint `get_fresh_water_module_pump_speed()` to the hot water tank
- Added endpoint `get_mixer_return_flow_temperature()` to the heating circuit
- Added `filter_request()` to get only the endpoints that are supported by the Web HMI

### Changed

- **Breaking:** Renamed the heating circuit endpoint `get_flow_temperature()` to `get_mixer_flow_temperature()`

## [2.6.0] - 2026-01-11

### Added

- Added endpoints `get_priority_1_before_2()` and `set_priority_1_before_2()` to the solar circuit

## [2.5.2] - 2026-01-09

### Added

- Added endpoint `get_substate()` to the heat pump
- Added endpoint `get_source_pump_speed()` to the heat pump
- Added endpoint `get_condenser_temperature()` to the heat pump
- Added endpoint `get_vaporizer_temperature()` to the heat pump

### Fixed

- Changed the basic auth encoding from "latin-1" to "utf-8"

## [2.5.1] - 2026-01-06

### Fixed

- Fixed invalid buffer tank operating mode

## [2.5.0] - 2026-01-05

### Added

- Added endpoints for buffer tanks

## [2.4.0] - 2026-01-03

### Added

- Added endpoints for solar circuits

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
- Added support for authentication (required for newer KeEnergy.WebHmi versions)
- Added the HTTP status code to the `APIError` exception

## [2.0.0] - 2025-09-30

### Added

- Added endpoint `has_passive_cooling()` to detect if the heat pump supports passive cooling
- Added endpoint `get_compressor_use_night_speed()` to get the compressor night speed state
- Added endpoint `set_compressor_use_night_speed()` to set the compressor night speed state
- Added endpoint `get_compressor_night_speed()` to get the compressor night speed
- Added endpoint `set_compressor_night_speed()` to set the compressor night speed
- Added endpoint `get_max_compressor_night_speed()` to get the maximum compressor night speed
- Added endpoint `get_min_compressor_night_speed()` to get the minimum compressor night speed
- Added endpoint `get_flow_temperature_setpoint()` to get the calculated flow temperature setpoint
- Added endpoint `get_hot_water_flow()` to see if the fresh water module is activated and hot water flows
- Added endpoint `get_fresh_water_module_temperature()` to get the temperature of the fresh water module
- Added missing human-readable values for `HeatCircuitHeatRequest`, `HeatCircuitOperatingMode` and `HeatPumpState`

### Changed

- **Breaking:** Renamed many endpoint functions to more technically accurate names

### Fixed

- Added missing human-readable value `room_off` for the heating circuit heat request state `4`

## [1.15.0] - 2025-09-14

### Added

- Added endpoints to read the energy management data

## [1.14.0] - 2025-08-27

### Added

- Added endpoints `has_room_temperature()` and `has_room_humidity()` to the heating circuit

## [1.13.0] - 2025-08-26

### Added

- Added room temperature, room humidity and dew point to the heating circuit

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

- Bumped aiohttp to `3.10.0b1`

## [1.12.6] - 2024-03-27

### Fixed

- Added missing heat request state `OUTDOOR_TEMPERATURE_OFF`

## 1.12.5 - 2024-02-25

### Added

- Added support for Python 3.12

## [1.12.4] - 2024-01-30

### Changed

- Bumped aiohttp to `3.9.4`

## [1.12.3] - 2023-12-08

### Changed

- Bumped aiohttp to `3.9.1`
- Bumped aioresponses to `0.7.6`

## [1.12.2] - 2023-11-19

### Changed

- **Breaking:** Renamed `HeatCircuitOperatingMode.AWAY` to `HeatCircuitOperatingMode.HOLIDAY`

## [1.12.1] - 2023-11-19

### Changed

- **Breaking:** Renamed endpoint `get_offset_temperture()` to `get_temperture_offset()`

## [1.12.0] - 2023-11-18

### Added

- Added endpoint `system.get_operation_mode()`
- Added endpoint `system.set_operation_mode()`
- Added endpoint `heat_pump.get_operation_mode()`
- Added endpoint `heat_pump.set_operation_mode()`
- Added endpoint `heat_circuit.get_external_cool_request()`
- Added endpoint `heat_circuit.get_external_heat_request()`

### Changed

- Converted the attribute keys to lower case
- Merged the options and devices endpoints into the system endpoint
- **Breaking:** Renamed `read_values()` to `read_data()`
- **Breaking:** Renamed `write_values()` to `write_data()`
- **Breaking:** Renamed `heat_pump.get_status()` to `heat_pump.get_state()`

## [1.11.1] - 2023-10-25

### Fixed

- Fixed the response keys of `read_values_grouped_by_section()`

## [1.11.0] - 2023-10-25

### Added

- Added endpoint `heat_pump.get_heat_request()`
- Added endpoint `heat_circuit.get_heat_request()`
- Added endpoint `hot_water_tank.get_heat_request()`

## [1.10.1] - 2023-10-24

### Changed

- Refactored the `SystemPrefix` enum variables

## [1.10.0] - 2023-10-23

### Added

- Added heat pump state "inflow"
- Added endpoint `heat_circuit.set_holiday_temperature()`

## [1.9.0] - 2023-10-23

### Added

- Added **AWAY** and **PARTY** to the heating circuit operating mode

## [1.8.1] - 2023-10-22

### Added

- Added `APIError` exception when a value can't be converted to a human-readable value

### Changed

- Allowed setting the operating mode in lower and upper case

## [1.8.0] - 2023-10-20

### Added

- Added endpoint `read_values_grouped_by_section()`
- Added `attributes` to the `read_values()` response

## [1.7.0] - 2023-10-19

### Added

- Added endpoint `hot_water_tank.get_lower_limit_temperature()`
- Added endpoint `hot_water_tank.get_upper_limit_temperature()`

## [1.6.2] - 2023-10-18

### Changed

- Refactored the `KebaKeEnergyAPI` class for better mocking with pytest

## [1.6.1] - 2023-10-17

### Fixed

- `InvalidJsonError` now inherits from `APIError`

## [1.6.0] - 2023-10-14

### Added

- Added `heat_pump.get_name()` to read the heat pump name
- Added `heat_circuit.get_name()` to read the heating circuit name
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

- Added `client.device_url` to get the device URL

## [1.4.1] - 2023-10-11

### Changed

- Downgraded aiohttp to `3.8.5` for Home Assistant compatibility

## [1.4.0] - 2023-10-11

### Added

- Added `get_device_info()` to read all device information, e.g. the serial number, as `dict`

## [1.3.0] - 2023-10-10

### Added

- Added `get_number_of_hot_water_tanks()` to read the number of hot water tanks
- Added `get_number_of_heat_pumps()` to read the number of heat pumps
- Added `get_number_of_heating_circuits()` to read the number of heating circuits
- Added automatic position numbers for `read_values()` depending on the hardware

## [1.2.0] - 2023-10-09

### Added

- Added `read_values()` to read multiple values with one HTTP request
- Added `write_values()` to write multiple values with one HTTP request

## [1.1.0] - 2023-10-08

### Added

- Added device information endpoint, e.g. for the serial number
- Added SSL support for aiohttp

## [1.0.0] - 2023-10-07

### Added

- Initial release

[unreleased]: https://github.com/superbox-dev/keba_keenergy_api/compare/v2.12.2...HEAD
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
[issue-67]: https://github.com/superbox-dev/keba_keenergy/issues/67
[issue-97]: https://github.com/superbox-dev/keba_keenergy_api/issues/97
[issue-100]: https://github.com/superbox-dev/keba_keenergy_api/issues/100
[cve-2026-34513]: https://github.com/advisories/GHSA-hcc4-c3v8-rx92

<!--end-->
