---
sidebar_position: 5
---

# Usage

## Read and write data

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI
from keba_keenergy_api.enums import HeatingCircuitOperatingMode
from keba_keenergy_api.sections import HeatingCircuit
from keba_keenergy_api.sections import System


async def main():
    async with KebaKeEnergyAPI(
        host="ap4400.local", username="test", password="test", ssl=True, verify_ssl=False
    ) as client:
        # Read multiple values with one request
        readings = await client.read(
            [System.OUTDOOR_TEMPERATURE, HeatingCircuit.OPERATING_MODE, HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL]
        )

        outdoor_temperature = readings[System.OUTDOOR_TEMPERATURE][0]
        print(outdoor_temperature.value, outdoor_temperature.unit)  # 10.808357 °C

        # One reading per heating circuit, the position starts at 1
        for reading in readings[HeatingCircuit.OPERATING_MODE]:
            print(reading.position, reading.value)  # 1 HeatingCircuitOperatingMode.AUTO

        # Write multiple values with one request, one value per device, None skips a device
        await client.write(
            {
                # Normal room temperature of heating circuit 1 and 3
                HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL: [20, None, 21.5],
                # Operating mode of heating circuit 1
                HeatingCircuit.OPERATING_MODE: [HeatingCircuitOperatingMode.NORMAL],
            }
        )


asyncio.run(main())
```

The sections are the members of the enums in `keba_keenergy_api.sections`, one enum per device type, see
[Sections](/sections). The installed devices are read once with `get_device_counts()` and reused, sections of
devices that are not installed return an empty list.

Each `Reading` has the value converted to the type of the endpoint (`bool`, `float`, `int`, `str` or an enum member
of `keba_keenergy_api.enums`), the `position` (and `consumer` for the two consumers of a solar
circuit), the `lower_limit` and `upper_limit` of the Web HMI and the `unit`.

Reading the limits makes the request of the Web HMI about twice as slow. `limits` chooses the endpoints whose limits
are read, the others have `None`:

| `limits`          | Limits are read for                                   |
|-------------------|-------------------------------------------------------|
| `"all"` (default) | all endpoints                                         |
| `"writable"`      | writable endpoints only, enough to check a write      |
| `"read_only"`     | read-only endpoints only                              |
| `"none"`          | no endpoint, the fastest read                         |

```python
readings = await client.read([DHWTank.TARGET_TEMPERATURE, DHWTank.TEMPERATURE], limits="writable")
```

Values are not rounded, scaled or interpreted: ratios stay `0..1` (e.g. pump speeds), the CPU usage stays per mille,
the energy of the meters (heat pump, photovoltaics, solar circuit) stays in joule, mass flows in kg/s and volume
flows in m³/s. Temperature differences (hystereses, offsets, superheat) have the unit `K`. Converting the values is
up to the caller.

Older Web HMI versions don't know every variable. `filter_supported()` returns the sections the controller supports
(all variables of the installed devices are known), `read()` raises an `UnsupportedVariableError` for an unknown
variable.

## Session

Without a session, the client opens one on the first request and closes it with `close()` or at the end of
`async with`.

You can also pass your own `aiohttp ClientSession()`, e.g. to share it with other code. The client leaves it open.
Every request times out after 10 seconds (`API_DEFAULT_TIMEOUT`), also with a passed session:

```python
import asyncio

from aiohttp import ClientSession

from keba_keenergy_api import KebaKeEnergyAPI


async def main():
    async with ClientSession() as session:
        client = KebaKeEnergyAPI(host="ap4400.local", username="test", password="test", session=session)
        ...


asyncio.run(main())
```

## Write warnings

This is a low-level API that allows writing values outside the safe operating range.
Improper use can damage heating systems and hardware. Always check `lower_limit` and `upper_limit` of the reading
before writing a value.

*Use at your own risk!*

**Example:**

The upper limit of the DHW tank temperature is 52 °C. Do not write larger values under any circumstances,
even if it would be possible.

```python
readings = await client.read([DHWTank.TARGET_TEMPERATURE])
readings[DHWTank.TARGET_TEMPERATURE][0].upper_limit  # 52.0
```

:::warning[Attention]

Writing values should remain within normal limits, as is the case with typical use of the Web HMI.
Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory. **Be careful!**

:::

## Message ids

Many sensors and components have a message id (`state.msgId`), the section has an `Endpoint.message_id`.
`read(..., message_ids=True)` reads them with the values in the same request and sets `Reading.message_id`
with the raw `value` and the `kind`, the same way the Web HMI handles them:

| Message id      | `MessageIdKind` | Meaning                                          |
|-----------------|-----------------|--------------------------------------------------|
| `0`             | `OK`            | The value is valid                               |
| `10`            | `DEACTIVATED`   | The component is not configured                  |
| any other value | `ERROR`         | The component exists, but its value is not valid |

```python
from keba_keenergy_api.sections import HeatingCircuit

readings = await client.read([HeatingCircuit.ROOM_TEMPERATURE], message_ids=True)

for reading in readings[HeatingCircuit.ROOM_TEMPERATURE]:
    print(reading.position, reading.message_id)  # 1 MessageId(value=10, kind=<MessageIdKind.DEACTIVATED: ...>)
```

If the Web HMI doesn't know a message id, `read()` sends the request again without it and leaves it out from then on.
The value is read as usual, its `message_id` is `None`.

## Curve tables

A heating circuit uses either its curve slope and offset or a curve table (`USE_CURVE_TABLE`). The curve tables are
stored in a pool and selected by name with `HEATING_CURVE` and `COOLING_CURVE`, the same table can be a heating or a
cooling curve. `get_curve_tables()` returns them by name (e.g. `HC1`) with their points, `set_curve_table_points()`
writes the 7 to 16 points of a table.

## Alarms

`get_alarms()` returns the pending alarms, the same list as on the display and in the Web HMI. The texts are in the
requested `language` (default `en`), names configured on the control unit stay as they are. The control unit removes an
alarm as soon as its cause is gone. `get_alarm_count()` is a cheaper request, e.g. to read the alarms only when there
are any.

```python
from zoneinfo import ZoneInfo

if await client.get_alarm_count():
    timezone = ZoneInfo(await client.get_timezone())

    for alarm in await client.get_alarms(language="de"):
        print(alarm.priority, alarm.short_text, alarm.timestamp.replace(tzinfo=timezone))
```

`timestamp` is the local time of the control unit without a timezone, `get_timezone()` returns it. `priority` is an
`AlarmPriority` (`EMERGENCY`, `ERROR`, `WARNING`, `INFO`), an unknown priority is an `INFO` like in the Web HMI.
`acknowledgeable` shows whether the alarm must be acknowledged on the control unit, the library doesn't acknowledge
alarms.

## Remote maintenance

The control unit can be reached by KEBA or the installer via remote maintenance. Each method sends one request.

```python
if not await client.is_remote_maintenance_active():
    await client.set_remote_maintenance_active(active=True)

await client.is_remote_maintenance_connected()  # True during a connection to the remote maintenance server.
```

`is_remote_maintenance_server_reachable()` lets the control unit check the remote maintenance server, which takes a
few seconds. Don't use it in a regular poll.

:::warning[Attention]

`set_remote_maintenance_active()` changes the settings of the control unit, like the Web HMI does. Don't switch it
permanently or very frequently, see [write warnings](#write-warnings).

:::

## Errors

All errors are subclasses of `APIError` (`keba_keenergy_api.exceptions`):

| Exception                  | Raised when                                                                                         |
|----------------------------|-----------------------------------------------------------------------------------------------------|
| `AuthenticationError`      | The credentials were rejected (HTTP 401)                                                            |
| `UnsupportedVariableError` | The Web HMI doesn't know a variable, `variable` holds its name                                      |
| `InvalidResponseError`     | The response is not valid JSON, a value can't be converted or an alarm has an invalid timestamp     |
| `APITimeoutError`          | A request timed out, it is also a `TimeoutError`                                                    |
| `APIError`                 | Any other HTTP or connection error, an invalid or read-only value for `write()` or an unknown curve |

`status` holds the HTTP status, if any.
