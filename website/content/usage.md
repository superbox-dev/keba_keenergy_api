---
sidebar_position: 5
---

# Usage

## Read and write data

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI
from keba_keenergy_api.enums import HeatingCircuitOperatingMode
from keba_keenergy_api.endpoints import HeatingCircuit
from keba_keenergy_api.endpoints import System


async def main():
    async with KebaKeEnergyAPI(
        host="ap4400.local", username="test", password="test", ssl=True, verify_ssl=False
    ) as client:
        # Read multiple values with one request
        readings = await client.read(
            [System.OUTDOOR_TEMPERATURE, HeatingCircuit.OPERATING_MODE, HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL]
        )

        outdoor_temperature = readings[System.OUTDOOR_TEMPERATURE][0]
        print(outdoor_temperature.value, System.OUTDOOR_TEMPERATURE.value.raw_unit)  # 10.808357 °C

        # One reading per heating circuit, the device number starts at 1
        for reading in readings[HeatingCircuit.OPERATING_MODE]:
            print(reading.device_number, reading.value)  # 1 HeatingCircuitOperatingMode.AUTO

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

The endpoints are the members of the enums in `keba_keenergy_api.endpoints`, one enum per device type, see
[Endpoints](/endpoints). The installed devices are read once with `get_device_counts()` and reused, endpoints of
devices that are not installed return an empty list.

Each `Reading` has:

- `value`: the value converted to the type of the endpoint (`bool`, `float`, `int`, `str` or an enum member of
  `keba_keenergy_api.enums`)
- `raw_value`: the value exactly as the Web HMI delivers it, as a string (e.g. `"25"` for `HeatPumpSubState.DRIP`,
  which stands for `13` and `25`)
- `device_number`: the number of the device, starting at 1
- `consumer_number`: the number of the consumer, only for the two consumers of a solar circuit
- `lower_limit` and `upper_limit`: the limits of the Web HMI
- `message_id`: the message id, see [Message ids](#message-ids)

Reading the limits makes the request of the Web HMI about twice as slow. `limits` chooses the endpoints whose limits
are read, the others have `None`:

| `limits`          | Limits are read for                                   |
|-------------------|-------------------------------------------------------|
| `"all"` (default) | all endpoints                                         |
| `"writable"`      | writable endpoints only, enough to check a write      |
| `"read_only"`     | read-only endpoints only                              |
| `"none"`          | no endpoint, the fastest read                         |

```python
readings = await client.read([DHWTank.TARGET_TEMPERATURE, DHWTank.TOP_TEMPERATURE], limits="writable")
```

The `value` is never rounded, scaled or interpreted, see [Units and display](#units-and-display).

Older Web HMI versions don't know every variable. `filter_supported()` returns the endpoints the controller supports
(all variables of the installed devices are known), `read()` raises an `UnsupportedVariableError` for an unknown
variable.

## Units and display

The `value` is the value of the Web HMI, only converted to the type of the endpoint:

- It is never rounded, scaled or interpreted.
- Ratios stay `0..1` (e.g. pump speeds) and the CPU usage stays per mille.
- The energy of the meters (heat pump, photovoltaics, solar circuit) stays in joule.
- Mass flows stay in kg/s and volume flows in m³/s.
- Temperature differences (hystereses, offsets, superheat) have the unit `K`.
- Converting the values is up to the caller.

How the Web HMI shows a value is static data of the endpoint:

- `endpoint.value` is its `EndpointDefinition`, a `Reading` doesn't repeat it.
- It is not read from the controller, so `read()` stays one request.
- The conversion comes from the `unitId` of the variable (`display = raw * multiplier / divisor`).
- The decimal places come from the `formatId` of the variable (`postComma`).

The fields of the `EndpointDefinition`:

| Field               | Meaning                                                                                  |
|---------------------|------------------------------------------------------------------------------------------|
| `raw_unit`          | Unit of the `value` as the Web HMI delivers it, `None` for ratios (`0..1`) and no unit   |
| `display_unit`      | Unit the Web HMI shows, `raw_unit` if the value is shown unchanged                       |
| `display_factor`    | `value * display_factor` is the value the Web HMI shows, `1.0` if it is shown unchanged  |
| `display_precision` | Decimal places the Web HMI shows for `value * display_factor`, `None` without a format   |

The conversions of the Web HMI:

| `raw_unit` | `display_unit` | `display_factor` |
|------------|----------------|------------------|
| ratio      | `%`            | `100`            |
| `‰`        | `%`            | `0.1`            |
| `W`        | `kW`           | `1/1000`         |
| `J`        | `kWh`          | `1/3600000`      |
| `s`        | `h`            | `1/3600`         |
| `s`        | `min`          | `1/60`           |
| `m³/s`     | `L/h`          | `3600000`        |
| `kg/s`     | `kg/h`         | `3600`           |

- All other numbers are shown in the unit they are delivered in (e.g. `°C`, `K`, `bar`, `kWh` of the statistics).
- The [Endpoints](/endpoints) page lists these values for every endpoint.

```python
definition = HeatPump.CIRCULATION_PUMP_SPEED.value
reading = readings[HeatPump.CIRCULATION_PUMP_SPEED][0]

# The pump speed is delivered as ratio 0.54009795, the Web HMI shows 54 %.
print(reading.value, definition.raw_unit)  # 0.54009795 None
print(round(reading.value * definition.display_factor, definition.display_precision), definition.display_unit)  # 54.0 %
```

Good to know:

- The `display_precision` refers to the **display unit**, not to the raw value. A power delivered in `W` is shown in
  `kW` with 2 decimal places.
- `lower_limit` and `upper_limit` are in the `raw_unit` like the `value`, multiply them by `display_factor` for the
  display unit.
- `bool`, enums and `str` have no `display_precision`. A few numbers (e.g. seasonal performance factors) are delivered
  by the Web HMI without a number format and also have none.
- The vacation start and end of the heating circuit are Unix timestamps, they have no display data.

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

Many sensors and components have a message id (`state.msgId`), the endpoint has an `EndpointDefinition.message_id`.
`read(..., message_ids=True)` reads them with the values in the same request and sets `Reading.message_id`
with the raw `value` and the `kind`, the same way the Web HMI handles them:

| Message id      | `MessageIdKind` | Meaning                                          |
|-----------------|-----------------|--------------------------------------------------|
| `0`             | `OK`            | The value is valid                               |
| `10`            | `DEACTIVATED`   | The component is not configured                  |
| any other value | `ERROR`         | The component exists, but its value is not valid |

```python
from keba_keenergy_api.endpoints import HeatingCircuit

readings = await client.read([HeatingCircuit.ROOM_TEMPERATURE], message_ids=True)

for reading in readings[HeatingCircuit.ROOM_TEMPERATURE]:
    print(reading.device_number, reading.message_id)  # 1 MessageId(value=10, kind=<MessageIdKind.DEACTIVATED: ...>)
```

If the Web HMI doesn't know a message id, `read()` sends the request again without it and leaves it out from then on.
The value is read as usual, its `message_id` is `None`.

## Curve tables

A heating circuit uses either its curve slope and offset or a curve table (`USE_CURVE_TABLE`). The curve tables are
stored in a pool and selected by name with `HEATING_CURVE` and `COOLING_CURVE`, the same table can be a heating or a
cooling curve.

- `get_curve_table_names()` returns only the names of the tables (e.g. `HC1`), one small request
- `get_curve_tables()` returns the tables by name with their points, `get_curve_tables(["HC1"])` only the requested
  ones (an unknown name raises an `APIError`)
- `set_curve_table_points()` writes the 1 to 16 points of a table

```python
names = await client.get_curve_table_names()
curves = await client.get_curve_tables(["HC1"])
```

## Week timers

The week timers set the times with normal operation (day), outside of them the operation is reduced (night). Each
device has 7 days with 3 blocks, each with a start and a stop.

- `WeekTimerType.HEATING_CIRCUIT_HEATING` and `HEATING_CIRCUIT_COOLING`: the timers of the heating circuits
- `WeekTimerType.DHW_TANK`: the timer of the DHW tanks (the buffer tanks have none)
- `get_week_timers()` reads the timers of the given device numbers with one request (the first device is 1, like
  `Reading.device_number`), `set_week_timers()` writes the timers of the devices given by number with one request
- `set_week_timers()` only writes the given days and blocks: a `WeekTimer` can have any days and a day 1 to 3
  blocks, written from the first one, the following blocks of the day keep their value
- the numbers are always given, the number of installed devices is not read (see `get_device_counts()`), a device that
  is not installed raises an `UnsupportedVariableError`
- the days are in the order of the Web HMI (`WeekDay.SUNDAY` first), start and stop are `int` seconds since
  midnight (`21600` is `06:00`) and the stop can be `24:00` (`86400`), an unused block has the same start and stop (`0`)

```python
timers = await client.get_week_timers(WeekTimerType.HEATING_CIRCUIT_HEATING, [1, 2])
block = timers[1].days[WeekDay.MONDAY].blocks[0]

await client.set_week_timers(WeekTimerType.HEATING_CIRCUIT_HEATING, {2: timers[1]})
```

## Vacation period

The vacation period of a heating circuit is the pair `HeatingCircuit.VACATION_START` and `VACATION_END`, normal
endpoints for `read()` and `write()`. The values are Unix timestamps in seconds (UTC). The Web HMI sets the start to
`00:00:00` and the end to `23:59:59` of the local day, the time zone is returned by `get_timezone()`. The limits that
`read(..., limits=...)` returns for them (`0` to `86400`) don't match these values.

```python
await client.write(
    {
        HeatingCircuit.VACATION_START: [1793314800, 1793314800],
        HeatingCircuit.VACATION_END: [1793401199, 1793401199],
    }
)
```

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

## Remote maintenance and Modbus TCP

The control unit can be reached by KEBA or the installer via remote maintenance and offers a Modbus TCP server. Each
method sends one request.

```python
if not await client.is_remote_maintenance_active():
    await client.set_remote_maintenance_active(active=True)

await client.is_remote_maintenance_connected()  # True during a connection to the remote maintenance server.

await client.set_modbus_active(active=True)
```

`is_remote_maintenance_server_reachable()` lets the control unit check the remote maintenance server, which takes a
few seconds. Don't use it in a regular poll. After `set_modbus_active(active=True)`, `is_modbus_active()` still returns
`False` for a few seconds, disabling takes effect immediately.

:::warning[Attention]

`set_remote_maintenance_active()` and `set_modbus_active()` change the settings of the control unit, like the Web HMI
does. Don't disable the Modbus TCP server while another Modbus client depends on it. Don't switch them permanently or
very frequently, see [write warnings](#write-warnings).

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
