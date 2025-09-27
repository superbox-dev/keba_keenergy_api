# KEBA KeEnergy API

A Python wrapper for the KEBA KeEnergy API.

![coverage-badge](https://raw.githubusercontent.com/superbox-dev/keba_keenergy_api/main/coverage-badge.svg)
[![CI](https://github.com/superbox-dev/KEBA-KeEnergy-API/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/superbox-dev/keba_keenergy_api/actions/workflows/ci.yml)
[![Version](https://img.shields.io/pypi/pyversions/keba-keenergy-api.svg)](https://pypi.python.org/pypi/keba-keenergy-api)

[![license-url](https://img.shields.io/pypi/l/keba-keenergy-api.svg)](https://github.com/superbox-dev/keba_keenergy_api/blob/main/LICENSE)
![Typing: strict](https://img.shields.io/badge/typing-strict-green.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-black)
![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)

## Getting started

```bash
pip install keba-keenergy-api
```

## Usage

```python
import asyncio
from typing import Any

from keba_keenergy_api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatCircuit


async def main() -> None:
    client = KebaKeEnergyAPI(host="YOUR-IP-OR-HOSTNAME", ssl=True)

    # Get current outdoor temperature
    outdoor_temperature: float = await client.get_outdoor_temperature()

    # Get heat circuit temperature from heat circuit 2
    heat_circuit_temperature: float = await client.heat_circuit.get_target_temperature(position=2)

    # Read multiple values
    data: dict[str, tuple[float | int | str]] = await client.read_data(
        request=[
            HeatCircuit.TARGET_TEMPERATURE,
            HeatCircuit.TARGET_TEMPERATURE_DAY,
        ],
    )

    # Enable "day" mode for heat circuit 2
    await client.heat_circuit.set_operating_mode(mode="day", position=2)

    # Write multiple values
    await client.write_data(
        request={
            HeatCircuit.TARGET_TEMPERATURE_DAY: (20, None, 5),  # Write heat circuit on position 1 and 3 
            HeatCircuit.TARGET_TEMPERATURE_NIGHT: (16,),  # Write night temperature on position 1
        },
    )


asyncio.run(main())
```

By default, the library creates a new connection to `KEBA KeEnergy API` with each coroutine. If you are calling a large
number of coroutines, an `aiohttp ClientSession()` can be used for connection pooling:

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI

from aiohttp import ClientSession

async def main() -> None:
    async with ClientSession() as session:
        client = KebaKeEnergyAPI(host="YOUR-IP-OR-HOSTNAME", session=session, ssl=True)
        ...

asyncio.run(main())
```

### API endpoints

| Endpoint                                        | Description                                  |
|-------------------------------------------------|----------------------------------------------|
| `.read_data(request, position, human_readable)` | Get multiple values with one http request.   |
| `.write_data(request)`                          | Write multiple values with one http request. |

#### System

| Endpoint                                           | Response       | Description                                                                                                        |
|----------------------------------------------------|----------------|--------------------------------------------------------------------------------------------------------------------|
| `.get_info()`                                      | `str`          | Get system information.                                                                                            |
| `.get_device_info()`                               | `str`          | Get device information.                                                                                            |
| `.get_outdoor_temperature()`                       | `float`        | Get outdoor temperature.                                                                                           |
| `.get_operating_mode(position, human_readable)`    | `int` or `str` | Get operating mode as integer (0 is `STANDBY`, 1 is `SUMMER`, 2 is `AUTO_HEAT`, 3 is `AUTO_COOL` and 4 is `AUTO`). |
| `.set_operating_mode(0, position, human_readable)` | `int` or `str` | Set operating mode.                                                                                                |

#### Hot water tank

| Endpoint                                           | Request/Response | Description                                                                           |
|----------------------------------------------------|------------------|---------------------------------------------------------------------------------------|
| `.get_current_temperature(position)`               | `float`          | Get current temperature.                                                              |
| `.get_operating_mode(position, human_readable)`    | `int` or `str`   | Get operating mode as integer (0 is `OFF`, 1 is `AUTO`, 2 is `DAY` and 3 is `NIGHT`). |
| `.set_operating_mode(0, position, human_readable)` | `int` or `str`   | Set operating mode.                                                                   |
| `.get_min_target_temperature(position)`            | `int`            | Get minimum possible target temperature.                                              |
| `.get_max_target_temperature(position)`            | `int`            | Get maximum possible target temperature.                                              |
| `.get_standby_temperature(position)`               | `float`          | Get standby temperature.                                                              |
| `.set_standby_temperature(20, position)`           | `float`          | Set standby temperature.                                                              |
| `.get_target_temperature(position)`                | `float`          | Get target temperature.                                                               |
| `.set_target_temperature(22, position)`            | `float`          | Set target temperature.                                                               |
| `.get_heat_request(position)`                      | `int` or `str`   | Get heat request.                                                                     |
| `.get_hot_water_flow(position)`                    | `int` or `str`   | Get hot water flow.                                                                   |
| `.get_fresh_water_module_temperature(position)`    | `float`          | Get fresh water module temperature.                                                   |

#### Heat pump

| Endpoint                                                    | Response       | Description                                                                  |
|-------------------------------------------------------------|----------------|------------------------------------------------------------------------------|
| `.get_name(position)`                                       | `str`          | Get head pump model name.                                                    |
| `.get_state(position, human_readable)`                      | `int` or `str` | Get heat pump state as integer (0 is `STANDBY`, 1 is `FLOW` and 2 is `AUTO`). |
| `.get_operating_mode(position, human_readable)`             | `int` or `str` | Get operating mode as integer (0 is `OFF`, 1 is `ON`, 2 is `BACKUP`).        |
| `.set_operating_mode(0, position, human_readable)`          | `int` or `str` | Set operating mode.                                                          |
| `.get_compressor_use_night_speed(position, human_readable)` | `int` or `str` | Get compressor use night speed (0 is `OFF`, 1 is `ON`).                      |
| `.set_compressor_use_night_speed(0, position)`              | `int` or `str` | Set compressor use night speed.                                              |
| `.get_compressor_night_speed(position)`                     | `float`        | Get compressor night speed.                                                  |
| `.set_compressor_night_speed(0.5, position)`                | `float`        | Set compressor night speed.                                                  |
| `.get_max_compressor_night_speed(position)`                 | `float`        | Get maximum compressor night speed.                                          |
| `.get_min_compressor_night_speed(position)`                 | `float`        | Get minimum compressor night speed.                                          |
| `.get_circulation_pump(position)`                           | `float`        | Get circulation pump in percent.                                             |
| `.get_flow_temperature(position)`                           | `float`        | Get flow temperature.                                                        |
| `.get_return_flow_temperature(position)`                    | `float`        | Get return flow temperature.                                                 |
| `.get_source_input_temperature(position)`                   | `float`        | Get source input temperature.                                                |
| `.get_source_output_temperature(position)`                  | `float`        | Get source output temperature.                                               |
| `.get_compressor_input_temperature(position)`               | `float`        | Get compressor input temperature.                                            |
| `.get_compressor_output_temperature(position)`              | `float`        | Get compressor output temperature.                                           |
| `.get_compressor(position)`                                 | `float`        | Get compressor in percent.                                                   |
| `.get_high_pressure(position)`                              | `float`        | Get high pressure.                                                           |
| `.get_low_pressure(position)`                               | `float`        | Get low pressure.                                                            |
| `.get_heat_request(position)`                               | `int` or `str` | Get heat request.                                                            |
| `.get_compressor_power(position)`                           | `float`        | Get compressor power.                                                        |
| `.get_heating_power(position)`                              | `float`        | Get heating power.                                                           |
| `.get_hot_water_power(position)`                            | `float`        | Get hot water power.                                                         |
| `.get_cop(position)`                                        | `float`        | Get coefficient of performance.                                              |
| `.get_heating_energy(position)`                             | `float`        | Get heating energy.                                                          |
| `.get_heating_energy_consumption(position)`                 | `float`        | Get heating energy consumption.                                              |
| `.get_heating_spf(position)`                                | `float`        | Get heating seasonal performance factor.                                     |
| `.get_cooling_energy(position)`                             | `float`        | Get cooling energy.                                                          |
| `.get_cooling_energy_consumption(position)`                 | `float`        | Get cooling energy consumption.                                              |
| `.get_cooling_spf(position)`                                | `float`        | Get cooling seasonal performance factor.                                     |
| `.get_hot_water_energy(position)`                           | `float`        | Get hot water energy.                                                        |
| `.get_hot_water_energy_consumption(position)`               | `float`        | Get hot water electrical energy.                                             |
| `.get_hot_water_spf(position)`                              | `float`        | Get hot water seasonal performance factor.                                   |
| `.get_total_thermal_energy(position)`                       | `float`        | Get total thermal energy.                                                    |
| `.get_total_energy_consumption(position)`                   | `float`        | Get total energy consumption.                                                |
| `.get_total_spf(position)`                                  | `float`        | Get total seasonal performance factor.                                       |
| `.has_passive_cooling(position)`                            | `int` or `str` | Has passive cooling.                                                         |

#### Heat circuit

| Endpoint                                        | Request/Response | Description                                         |
|-------------------------------------------------|------------------|-----------------------------------------------------|
| `.get_name(position)`                           | `str`            | Get heat circuit name.                              |
| `.has_room_temperature(position)`               | `int` or `str`   | Has room temperature.                               |
| `.get_room_temperature(position)`               | `float`          | Get room temperature.                               |
| `.has_room_humidity(position)`                  | `int` or `str`   | Has room humidity.                                  |
| `.get_room_humidity(position)`                  | `float`          | Get room humidity.                                  |
| `.get_dew_point(position)`                      | `float`          | Get dew point.                                      |
| `.get_flow_temperature_setpoint(position)`      | `float`          | Get flow temperature setpoint.                      |
| `.get_target_temperature(position)`             | `float`          | Get target temperature.                             |
| `.get_target_temperature_day(position)`         | `float`          | Get taget temperature for the day.                  |
| `.set_target_temperature_day(20, position)`     | `float`          | Set taget temperature for the day.                  |
| `.get_heating_limit_day(position)`              | `float`          | Get the heating limit for the day.                  |
| `.get_target_temperature_night(position)`       | `float`          | Get target temperature for the night.               |
| `.set_target_temperature_night(16, position)`   | `float`          | Set target temperature for the night.               |
| `.get_heating_limit_night(position)`            | `float`          | Get the heating limit for the night.                |
| `.get_target_temperature_away(position)`        | `float`          | Get target temperature when away.                   |
| `.set_target_temperature_away(14, position)`    | `float`          | Set target temperature when away.                   |
| `.get_target_temperature_offset(position)`      | `float`          | Get target temperature offset.                      |
| `.set_target_temperature_offset(2, position)`   | `float`          | Set target temperature offset.                      |
| `.get_operating_mode(position, human_readable)` | `int` or `str`   | Get operating mode (0 is `OFF` and 3 is `HEAT_UP`). |
| `.set_operating_mode(3, position)`              | `int` or `str`   | Set operating mode.                                 |
| `.get_heat_request(position)`                   | `int` or `str`   | Get heat request.                                   |
| `.get_external_cool_request(position)`          | `int` or `str`   | Get external cool request.                          |
| `.get_external_heat_request(position)`          | `int` or `str`   | Get external heat request.                          |

## Changelog

The changelog lives in the [CHANGELOG.md](CHANGELOG.md) document. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Contributing

We're happy about your contributions to the project!

You can get started by reading the [CONTRIBUTING.md](CONTRIBUTING.md).

## Donation

We put a lot of time into this project. If you like it, you can support us with a donation.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F2F0KXO6D)
