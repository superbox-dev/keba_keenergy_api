# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-09-30

### Added

- Added endpoint `has_passive_cooling()` to detect if the heat pump support passive cooling
- Added endpoint `get_compressor_use_night_speed()` to get the compressor night speed state
- Added endpoint `set_compressor_use_night_speed()` to get the compressor night speed
- Added endpoint `set_compressor_use_night_speed()` to get the compressor night speed
- Added endpoint `get_compressor_night_speed()` to get the compressor night speed
- Added endpoint `set_compressor_night_speed()` to set the compressor night speed
- Added endpoint `get_max_compressor_night_speed()` to get the maximum compressor night speed
- Added endpoint `get_min_compressor_night_speed()` to get the minimum compressor night speed
- Added endpoint `get_flow_temperature_setpoint()` to get the calculated flow temperature setpoint
- Added endpoint `get_hot_water_flow()` to see if the fresh water module is activated and hot water flow
- Added endpoint `get_fresh_water_module_temperature()` to get the temperature from the fresh water module
- Added missing humanreadable values for `HeatCircuitHeatRequest()`, `HeatCircuitOperatingMode()`, and `HeatPumpState()`

### Changed

- Changed many endpoint function names have been given more technically accurate names (breaking changes)

### Fixed

- Added missing humanreadable value `room_off` for heat circuit heat request status `4`

## [1.15.0] - 2025-09-14

### Added

- Endpoints to read the energy management data from the API

## [1.14.0] - 2025-08-27

### Added

- `has_room_temperature()` and `has_room_hummidity()` endpoint for heat circuits

## [1.13.0] - 2025-08-26

### Added

- Room temperature, room humidity and dew point to heat circuit endpoint

## [1.12.10] - 2025-08-19

### Added

- [py.typed](keba_keenergy_api/py.typed) to support static type checking e.g. with mypy

## [1.12.9] - 2024-12-21

### Added

- Support for Python 3.13 (required for the Home Assistant 2024.12)

## [1.12.8] - 2024-12-21

### Changed

- Allow all aiohttp versions with 3.*

## [1.12.7] - 2024-08-24

### Changed

- Bump aiohttp to 3.10.0b1

## [1.12.6] - 2024-03-27

### Fixed

- Missing heat request state `OUTDOOR_TEMPERATURE_OFF`

## [1.12.5] - 2024-02-25

### Changed

- Support Python 3.12

## [1.12.4] - 2024-01-30

### Changed

- Bump aiohttp to 3.9.4

## [1.12.3] - 2023-12-08

### Changed

- Bump aiohttp to 3.9.1
- Bump aioresponses to 0.7.6

## [1.12.2] - 2023-11-19

### Changed

- Rename `HeatCircuitOperatingMode.AWAY` to `HeatCircuitOperatingMode.HOLIDAY`

## [1.12.1] - 2023-11-19

### Changed

- Rename endpoint `get_offset_temperture()` to `get_temperture_offset()`

## [1.12.0] - 2023-11-18

### Added

- `system.get_operation_mode()` endpoint
- `system.set_operation_mode()` endpoint
- `heat_pump.get_operation_mode()` endpoint
- `heat_pump.set_operation_mode()` endpoint
- `heat_circuit.get_external_cool_request()` endpoint
- `heat_circuit.get_external_heat_request()` endpoint

### Changed

- Convert attributes keys to lower case
- Merge options and devices endpoint to system endpoint
- Rename `read_values()` to `read_data()`
- Rename `write_values()` to `write_data()`
- Rename `heat_pump.get_status()` to `heat_pump.get_state()`

## [1.11.1] - 2023-10-25

### Fixed

- Response keys from `read_values_grouped_by_section()`

## [1.11.0] - 2023-10-25

### Added

- `heat_pump.get_heat_request()` endpoint
- `heat_circuit.get_heat_request()` endpoint
- `hot_water_tank.get_heat_request()` endpoint

## [1.10.1] - 2023-10-24

### Changed

- Refactor `SystemPrefix` enum variables

## [1.10.0] - 2023-10-23

### Added

- Heat pump state "inflow"
- `heat_circuit.set_holiday_temperature()` endpoint

## [1.9.0] - 2023-10-23

### Added

- **AWAY** and **PARTY** to heat circuit operating mode

## [1.8.1] - 2023-10-22

### Added

- `APIError()` exception when can't convert value to human readable value

### Changed

- Allow set operating mode in lower and uppercase

## [1.8.0] - 2023-10-20

### Added

- `read_values_grouped_by_section()` endpoint
- `attributes` to `read_values()` response

## [1.7.0] - 2023-10-19

### Added

- `hot_water_tank.get_lower_limit_temperature()` endpoint
- `hot_water_tank.get_upper_limit_temperature()` endpoint

## [1.6.2] - 2023-10-18

### Fixed

- Refactor `KebaKeEnergyAPI()` class for better mocking with pytest

## [1.6.1] - 2023-10-17

### Fixed

- `InvalidJsonError` Class no inherit from `APIError` Class

### Added

## [1.6.0] - 2023-10-14

- `heat_pump.get_name()` to read the **heat pump** name
- `heat_circuit.get_name()` to read the **heat circuit** name
- `human_readable` attribute to `read_values()` to get a human-readable name and not a number as response e.g.
  for `hot_water_tank.get_operating_mode()`

## [1.5.0] - 2023-10-13

### Added

- `get_system_info()` to read all system information

## [1.4.3] - 2023-10-13

### Fixed

- Error when mixing endpoints with and without position

## [1.4.2] - 2023-10-13

### Added

- Get the device url with `client.device_url`

## [1.4.1] - 2023-10-11

### Changed

- Downgrade aiohttp to version 3.8.5 (for home assistant compatibility)

## [1.4.0] - 2023-10-11

### Added

- `get_device_info()` to read all device information e.g. serial number as `dict`

## [1.3.0] - 2023-10-10

### Added

- `get_number_of_hot_water_tanks()` to read number of hot water tanks
- `get_number_of_heat_pumps()` to read number of heat pumps
- `get_number_of_heating_circuits()` to read number of heating circuits
- Automatic set of position numbers for `read_values()` dependent on hardware

## [1.2.0] - 2023-10-09

### Added

- `read_values()` to read multiple values with one http request
- `write_values()` to write multiple values with one http request

## [1.1.0] - 2023-10-08

### Added

- Device information endpoint for e.g. serial number
- SSL support for aiohttp

## [1.0.0] - 2023-10-07

Initial release
