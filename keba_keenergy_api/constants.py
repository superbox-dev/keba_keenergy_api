# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Constants of the KEBA KeEnergy API."""

import re
from typing import TYPE_CHECKING
from typing import Final

if TYPE_CHECKING:
    from collections.abc import Mapping

API_DEFAULT_TIMEOUT: Final = 10

MIN_CURVE_TABLE_POINTS: Final = 1
MAX_CURVE_TABLE_POINTS: Final = 16

# Prefix of all variables of the control application.
_PAYLOAD_PREFIX: Final = "APPL.CtrlAppl"
_MESSAGE_ID_SUFFIX: Final = "state.msgId"

# Units of the endpoints.
_BAR: Final = "bar"
_CELSIUS: Final = "°C"
_CUBIC_METER_PER_SECOND: Final = "m³/s"
_JOULE: Final = "J"
# Temperature differences, e.g. hystereses and offsets.
_KELVIN: Final = "K"
_KILOBYTE: Final = "kB"
_KILOGRAM_PER_SECOND: Final = "kg/s"
_KILOWATT_HOUR: Final = "kWh"
_PER_MILLE: Final = "‰"
_PERCENT: Final = "%"
_SECOND: Final = "s"
_WATT: Final = "W"

# Message ids (``state.msgId``) with a special meaning in the Web HMI.
_OK_MESSAGE_ID: Final = 0
_DEACTIVATED_MESSAGE_ID: Final = 10

# Endpoints of the Web HMI.
_READ_WRITE_VARS: Final = "/var/readWriteVars"
_WRITE_VARS: Final = f"{_READ_WRITE_VARS}?action=set"
_SYSTEM_INSTALLED: Final = "/swupdate?action=getSystemInstalled"
_HMI_INSTALLED: Final = "/swupdate?action=getHmiInstalled"
_DEVICE_INFO: Final = "/deviceControl?action=getDeviceInfo"
_REMOTE_MAINTENANCE_ACTIVE: Final = "/deviceControl?action=isRemoteMActive"
_REMOTE_MAINTENANCE_CONNECTED: Final = "/deviceControl?action=isRemoteMConnectionAlive"
_REMOTE_MAINTENANCE_SERVER_REACHABLE: Final = "/deviceControl?action=isRemoteMServerReachable"
_ACTIVATE_REMOTE_MAINTENANCE: Final = "/deviceControl?action=activateRemoteM"
_MODBUS_ACTIVE: Final = "/deviceControl?action=isModbusActive"
_ACTIVATE_MODBUS: Final = "/deviceControl?action=activateModbus"
_TIME_ZONE: Final = "/dateTime?action=getTimeZone"
_ALARM_COUNT: Final = "/alarm?action=getCount"
_ALARMS: Final = "/alarm?action=getAll"

# The Web HMI rejects a read request with an unknown variable as a whole and names the first one.
_READ_ERROR_PATTERN: Final = re.compile(r"Reading variable: (\S+) failed")

# Raw boolean values of the Web HMI and the value written for them.
_BOOL_VALUES: Final[Mapping[str, bool]] = {"true": True, "false": False, "1": True, "0": False}
_WRITE_TRUE: Final = "1"
_WRITE_FALSE: Final = "0"

# Sections with the number of installed devices, read by get_device_counts().
_DEVICE_COUNT_SECTIONS: Final[Mapping[str, str]] = {
    "buffer_tank": "_NUMBER_OF_BUFFER_TANKS",
    "dhw_tank": "_NUMBER_OF_DHW_TANKS",
    "external_heat_source": "_NUMBER_OF_EXTERNAL_HEAT_SOURCES",
    "heat_pump": "_NUMBER_OF_HEAT_PUMPS",
    "heating_circuit": "_NUMBER_OF_HEATING_CIRCUITS",
    "solar_circuit": "_NUMBER_OF_SOLAR_CIRCUITS",
    "switch_valve": "_NUMBER_OF_SWITCH_VALVES",
}

# Priorities of the first consumer of a solar circuit, written together with CONSUMER_1_PRIORITY.
_CONSUMER_PRIORITY_LOW: Final = 14
_CONSUMER_PRIORITY_HIGH: Final = 15

# The heating and cooling curves are stored in a pool of line tables.
_LINE_TABLE: Final = f"{_PAYLOAD_PREFIX}.sParam.linTabPool[%s]"
_LINE_TABLE_POOL_SIZE: Final = 30
_CURVE_TABLE_NAME_PREFIX: Final = "HC"
# The Web HMI writes this value to the version counter to save a line table.
_SAVE_LINE_TABLE: Final = "192"
