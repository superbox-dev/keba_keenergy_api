# KEBA KeEnergy API

<!--start-home-->
A Python wrapper for the KEBA KeEnergy API used by the Web HMI.

![coverage-badge](https://raw.githubusercontent.com/superbox-dev/keba_keenergy_api/main/coverage-badge.svg)
[![Version](https://img.shields.io/pypi/pyversions/keba-keenergy-api.svg)](https://pypi.python.org/pypi/keba-keenergy-api)
[![CI](https://github.com/superbox-dev/KEBA-KeEnergy-API/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/superbox-dev/keba_keenergy_api/actions/workflows/ci.yml)

<!--end-home-->

## Donation

<!--start-donation-->

I put a lot of time into this project. If you like it, you can support me with a donation.

[![KoFi](https://raw.githubusercontent.com/superbox-dev/.github/refs/heads/main/profile/superbox-kofi.jpg)](https://ko-fi.com/F2F0KXO6D)

<!--end-donation-->

<!--start-home-->

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
from keba_keenergy_api.constants import HeatCircuitOperatingMode

async def main():
    client = KebaKeEnergyAPI(
        host="ap4400.local",
        username="test",
        password="test",
        ssl=True,
        skip_ssl_verification=True
    )

    # Get current outdoor temperature
    outdoor_temperature = await client.system.get_outdoor_temperature()

    # Get heat circuit temperature from heat circuit 2
    heat_circuit_temperature = await client.heat_circuit.get_target_temperature(
        position=2
    )

    # Read multiple values
    data = await client.read_data(
        request=[
            HeatCircuit.TARGET_TEMPERATURE,
            HeatCircuit.TARGET_TEMPERATURE_DAY
        ],
        extra_attributes=True
    )

    # Enable "day" mode for heat circuit 2
    await client.heat_circuit.set_operating_mode(
        mode=HeatCircuitOperatingMode.DAY.value,
        position=2
    )

    # Write multiple values
    await client.write_data(
        request={
            # Write heat circuit on position 1 and 3
            HeatCircuit.TARGET_TEMPERATURE_DAY: (20, None, 5),
            # Write night temperature on position 1
            HeatCircuit.TARGET_TEMPERATURE_NIGHT: (16,),
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

async def main():
    async with ClientSession() as session:
        client = KebaKeEnergyAPI(
            host="ap4400.local",
            username="test",
            password="test",
            ssl=True,
            skip_ssl_verification=True,
            session=session
        )
        ...

asyncio.run(main())
```

### ⚠️ Write warnings

This is a low-level API that allows writing values outside the safe operating range.
Improper use can damage heating systems and hardware. Always check the `attributes`,
as these may contain minimum and maximum values.

*Use at your own risk!*

**Example:**

The upper limit from the hot water tank temperature is 52 °C. Do not write larger values under any circumstances,
even if it would be possible.

```json
{
    "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
    "attributes": {
        "dynUpperLimit": 1,
        "formatId": "fmtTemp",
        "longText": "Temp. nom.",
        "lowerLimit": "0",
        "unitId": "Temp",
        "upperLimit": "52"
    },
    "value": "50"
}
```

**And one last warning:**

> **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
> Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.
> **Be carefully!**

<!--end-home-->

## Documentation

Read the full API documentation on [api.superbox.one](https://api.superbox.one).

## Changelog

The changelog lives in the [CHANGELOG.md](CHANGELOG.md) document.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

<!--start-contributing-->

## Get Involved

**The KEBA KeEnergy API** is an open-source project and contributions are welcome. You can:

* Report [issues](https://github.com/superbox-dev/keba_keenergy_api/issues/new/choose) or request new features
* Improve documentation
* Contribute code
* Support the project by starring it on GitHub ⭐

<!--end-contributing-->

I'm happy about your contributions to the project!
You can get started by reading the [CONTRIBUTING.md](CONTRIBUTING.md).
