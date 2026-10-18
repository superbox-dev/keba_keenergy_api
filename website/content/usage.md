---
sidebar_position: 5
---

# Usage

## Read and write values

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatCircuitOperatingMode


async def main():
    client = KebaKeEnergyAPI(
        host="ap4400.local", username="test", password="test", ssl=True, skip_ssl_verification=True
    )

    # Get current outdoor temperature
    outdoor_temperature = await client.system.get_outdoor_temperature()

    # Get heat circuit temperature from heat circuit 2
    heat_circuit_temperature = await client.heat_circuit.get_target_temperature(position=2)

    # Read multiple values
    data = await client.read_data(
        request=[HeatCircuit.TARGET_TEMPERATURE, HeatCircuit.TARGET_TEMPERATURE_DAY], extra_attributes=True
    )

    # Enable "day" mode for heat circuit 2
    await client.heat_circuit.set_operating_mode(mode=HeatCircuitOperatingMode.DAY.value, position=2)

    # Write multiple values
    await client.write_data(
        request={
            # Write the day temperature of heat circuit 1 and 3
            HeatCircuit.TARGET_TEMPERATURE_DAY: (20, None, 21),
            # Write night temperature on position 1
            HeatCircuit.TARGET_TEMPERATURE_NIGHT: (16,),
        },
    )


asyncio.run(main())
```

## Share one connection

By default, the library creates a new connection to `KEBA KeEnergy API` with each coroutine. If you are calling a large
number of coroutines, use the client with `async with`, so that all requests share one connection:

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI


async def main():
    async with KebaKeEnergyAPI(
        host="ap4400.local", username="test", password="test", ssl=True, skip_ssl_verification=True
    ) as client:
        ...


asyncio.run(main())
```

You can also pass your own `aiohttp ClientSession()`, e.g. to share it with other code. The client leaves it open:

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI

from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        client = KebaKeEnergyAPI(
            host="ap4400.local", username="test", password="test", ssl=True, skip_ssl_verification=True, session=session
        )
        ...


asyncio.run(main())
```

## Write warnings

This is a low-level API that allows writing values outside the safe operating range.
Improper use can damage heating systems and hardware. Always check the `attributes`,
as these may contain minimum and maximum values.

*Use at your own risk!*

**Example:**

The upper limit of the hot water tank temperature is 52 °C. Do not write larger values under any circumstances,
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

:::warning[Attention]

Writing values should remain within normal limits, as is the case with typical use of the Web HMI.
Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory. **Be careful!**

:::
