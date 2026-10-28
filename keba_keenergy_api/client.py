# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Asynchronous client for the KEBA KeEnergy Web HMI API."""

import json
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from http import HTTPStatus
from itertools import batched
from typing import TYPE_CHECKING
from typing import Any
from typing import Self
from typing import TypedDict
from typing import get_args
from urllib.parse import urlencode

from aiohttp import ClientError
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import ContentTypeError
from aiohttp import encode_basic_auth

from keba_keenergy_api.constants import _ACTIVATE_REMOTE_MAINTENANCE
from keba_keenergy_api.constants import _ALARM_COUNT
from keba_keenergy_api.constants import _ALARMS
from keba_keenergy_api.constants import _BOOL_VALUES
from keba_keenergy_api.constants import _CONSUMER_PRIORITY_HIGH
from keba_keenergy_api.constants import _CONSUMER_PRIORITY_LOW
from keba_keenergy_api.constants import _CURVE_TABLE_NAME_PREFIX
from keba_keenergy_api.constants import _DEVICE_COUNT_SECTIONS
from keba_keenergy_api.constants import _DEVICE_INFO
from keba_keenergy_api.constants import _HMI_INSTALLED
from keba_keenergy_api.constants import _LINE_TABLE
from keba_keenergy_api.constants import _LINE_TABLE_POOL_SIZE
from keba_keenergy_api.constants import _READ_ERROR_PATTERN
from keba_keenergy_api.constants import _READ_WRITE_VARS
from keba_keenergy_api.constants import _REMOTE_MAINTENANCE_ACTIVE
from keba_keenergy_api.constants import _REMOTE_MAINTENANCE_CONNECTED
from keba_keenergy_api.constants import _REMOTE_MAINTENANCE_SERVER_REACHABLE
from keba_keenergy_api.constants import _SAVE_LINE_TABLE
from keba_keenergy_api.constants import _SYSTEM_INSTALLED
from keba_keenergy_api.constants import _TIME_ZONE
from keba_keenergy_api.constants import _WRITE_FALSE
from keba_keenergy_api.constants import _WRITE_TRUE
from keba_keenergy_api.constants import _WRITE_VARS
from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.constants import MAX_CURVE_TABLE_POINTS
from keba_keenergy_api.constants import MIN_CURVE_TABLE_POINTS
from keba_keenergy_api.enums import AlarmPriority
from keba_keenergy_api.enums import MessageIdKind
from keba_keenergy_api.exceptions import APIError
from keba_keenergy_api.exceptions import APITimeoutError
from keba_keenergy_api.exceptions import AuthenticationError
from keba_keenergy_api.exceptions import InvalidResponseError
from keba_keenergy_api.exceptions import UnsupportedVariableError
from keba_keenergy_api.models import Alarm
from keba_keenergy_api.models import CurvePoint
from keba_keenergy_api.models import CurveTable
from keba_keenergy_api.models import DeviceCounts
from keba_keenergy_api.models import DeviceInfo
from keba_keenergy_api.models import HmiInfo
from keba_keenergy_api.models import Limits
from keba_keenergy_api.models import MessageId
from keba_keenergy_api.models import Reading
from keba_keenergy_api.models import Readings
from keba_keenergy_api.models import SystemInfo
from keba_keenergy_api.models import Value
from keba_keenergy_api.models import WriteValue
from keba_keenergy_api.sections import Section
from keba_keenergy_api.sections import SolarCircuit
from keba_keenergy_api.sections import System

if TYPE_CHECKING:
    import re
    from collections.abc import Iterable
    from collections.abc import Iterator
    from collections.abc import Mapping
    from collections.abc import Sequence
    from types import TracebackType


class _ReadPayload(TypedDict):
    """Payload for reading a variable."""

    name: str
    attr: str


class _WritePayload(TypedDict):
    """Payload for writing a variable."""

    name: str
    value: str


class _ActivatePayload(TypedDict):
    """Payload for enabling or disabling a service of the control unit."""

    activate: bool


@dataclass(frozen=True, kw_only=True)
class _Variable:
    """Variable name of one value of a section, with its 1-based position and consumer."""

    name: str
    position: int
    consumer: int | None


type _Payload = _ActivatePayload | list[_ReadPayload] | list[_WritePayload]
type _Response = list[dict[str, Any]]


class KebaKeEnergyAPI:
    """Asynchronous client for the KEBA KeEnergy Web HMI API.

    A caller may pass an existing :class:`aiohttp.ClientSession`, which is used as it is and not closed by the
    client. Without a session, the client opens one on the first request and closes it with :meth:`close`
    (or at the end of ``async with``).

    The installed devices are read once and reused, as they don't change while the control unit is running.
    """

    def __init__(
        self,
        host: str,
        *,
        username: str | None = None,
        password: str | None = None,
        ssl: bool = False,
        verify_ssl: bool = True,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize the API client.

        Parameters
        ----------
        host
            The hostname or IP address, e.g. ``ap4400.local``.
        username
            Username for HTTP Basic authentication.
        password
            Password for HTTP Basic authentication.
        ssl
            Use HTTPS.
        verify_ssl
            Verify the TLS certificate, ``False`` e.g. for self-signed certificates.
        session
            Optional session, used as it is and not closed by the client.

        Examples
        --------
        >>> client = KebaKeEnergyAPI(
        ...     host="ap4400.local",
        ...     username="test",
        ...     password="test",
        ...     ssl=True,
        ...     verify_ssl=False,
        ... )

        """
        self._host: str = host
        self._ssl: bool = ssl
        self._verify_ssl: bool = verify_ssl
        self._auth: str | None = encode_basic_auth(username, password) if username and password else None
        self._session: ClientSession | None = session
        self._own_session: ClientSession | None = None
        self._device_counts: DeviceCounts | None = None
        # Message id variables the Web HMI rejected, they are no longer read.
        self._unsupported_message_ids: set[str] = set()

    async def __aenter__(self) -> Self:
        """Return the client, the session it opens is closed at the end of ``async with``.

        Returns
        -------
        KebaKeEnergyAPI
            The client itself.

        Examples
        --------
        >>> async with KebaKeEnergyAPI(host="ap4400.local") as client:
        ...     await client.read([System.OUTDOOR_TEMPERATURE])

        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the session opened by the client.

        Parameters
        ----------
        exc_type
            Type of the raised exception, if any.
        exc_value
            The raised exception, if any.
        traceback
            Traceback of the raised exception, if any.

        """
        await self.close()

    @property
    def device_url(self) -> str:
        """Return the base URL of the control unit, e.g. ``https://ap4400.local``."""
        return f"{'https' if self._ssl else 'http'}://{self._host}"

    async def close(self) -> None:
        """Close the session opened by the client.

        A session passed to the client is left open, as its owner closes it.
        """
        if self._own_session is not None:
            await self._own_session.close()
            self._own_session = None

    async def get_device_counts(self) -> DeviceCounts:
        """Return the number of installed devices per device type.

        They are read from the control unit on the first call only.

        Returns
        -------
        DeviceCounts
            The number of installed devices, e.g. heat pumps and heating circuits.

        """
        if self._device_counts is None:
            response: _Response = await self._post(
                _READ_WRITE_VARS,
                [
                    _ReadPayload(name=System[section].value.variable, attr="0")
                    for section in _DEVICE_COUNT_SECTIONS.values()
                ],
            )

            counts: dict[str, int] = {
                key: int(item["value"]) for key, item in zip(_DEVICE_COUNT_SECTIONS, response, strict=True)
            }
            self._device_counts = DeviceCounts(**counts)

        return self._device_counts

    async def _post(self, endpoint: str, payload: _Payload | None = None, /) -> _Response:
        """Send a POST request to the Web HMI and return the JSON response as a list.

        Raises
        ------
        AuthenticationError
            The credentials were rejected (HTTP 401).
        UnsupportedVariableError
            The Web HMI doesn't know a requested variable.
        InvalidResponseError
            The response is not valid JSON.
        APITimeoutError
            The request timed out.
        APIError
            The Web HMI (or a reverse proxy) returned a status other than 2xx, the connection failed or the passed
            session is closed.

        """
        session: ClientSession = self._get_session()

        if session.closed:
            message: str = "The session is closed"
            raise APIError(message)

        headers: dict[str, str] = {} if self._auth is None else {"Authorization": self._auth}

        try:
            async with session.post(
                f"{self.device_url}{endpoint}",
                headers=headers,
                ssl=self._ssl and self._verify_ssl,
                data=None if payload is None else json.dumps(payload),
                # Also for a passed session, which has no timeout of its own.
                timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT),
            ) as resp:
                if resp.status == HTTPStatus.UNAUTHORIZED:
                    raise AuthenticationError(status=HTTPStatus.UNAUTHORIZED)

                # Everything else than 2xx is an error, e.g. also a redirect or a 502 of a reverse proxy.
                if not HTTPStatus.OK <= resp.status < HTTPStatus.MULTIPLE_CHOICES:
                    raise self._get_status_error(HTTPStatus(resp.status), await resp.text())

                response: _Response | dict[str, Any] = await resp.json()
        except (json.JSONDecodeError, ContentTypeError) as error:
            message = f"Invalid JSON response! {error}"
            raise InvalidResponseError(message) from error
        # Before ClientError, as the aiohttp timeouts (e.g. ConnectionTimeoutError) are also a ClientError.
        except TimeoutError as error:
            message = f"Request timed out! {error}".rstrip()
            raise APITimeoutError(message) from error
        except ClientError as error:
            raise APIError(str(error)) from error

        return [response] if isinstance(response, dict) else response

    def _get_session(self) -> ClientSession:
        """Return the passed session, otherwise the session opened by the client."""
        if self._session is not None:
            return self._session

        if self._own_session is None or self._own_session.closed:
            self._own_session = ClientSession(timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT))

        return self._own_session

    def _get_status_error(self, status: HTTPStatus, text: str, /) -> APIError:
        """Return the error of a response with a status other than 2xx.

        The Web HMI answers an error with HTTP 500 and a developer message, an unknown variable is an
        ``UnsupportedVariableError``.
        """
        if status is not HTTPStatus.INTERNAL_SERVER_ERROR:
            return APIError(text, status=status)

        message: str = self._get_developer_message(text)
        match: re.Match[str] | None = _READ_ERROR_PATTERN.search(message)

        if match is not None:
            return UnsupportedVariableError(message, variable=match.group(1), status=status)

        return APIError(message, status=status)

    @staticmethod
    def _get_developer_message(text: str, /) -> str:
        """Return the developer message of a Web HMI error response, otherwise the response text."""
        try:
            error_response: object = json.loads(text)
        except ValueError:
            return text

        if isinstance(error_response, dict) and "developerMessage" in error_response:
            return str(error_response["developerMessage"])

        return text

    async def get_system_info(self) -> SystemInfo:
        """Return the installed system software.

        Returns
        -------
        SystemInfo
            Name and version of the system software.

        """
        response: _Response = await self._post(_SYSTEM_INSTALLED)
        info: SystemInfo = SystemInfo(name=str(response[0]["name"]))

        if "version" in response[0]:
            info["version"] = str(response[0]["version"])

        return info

    async def get_hmi_info(self) -> HmiInfo:
        """Return the installed Web HMI software.

        Returns
        -------
        HmiInfo
            Name of the Web HMI software, e.g. ``KeEnergy.WebHmi_2.2.0.0``.

        """
        response: _Response = await self._post(_HMI_INSTALLED)
        return HmiInfo(name=str(response[0]["name"]))

    async def get_device_info(self) -> DeviceInfo:
        """Return the information about the control unit.

        Returns
        -------
        DeviceInfo
            Name, order, revision, serial and variant number of the control unit.

        """
        response: _Response = await self._post(_DEVICE_INFO)
        item: dict[str, Any] = response[0]

        return DeviceInfo(
            name=str(item["name"]),
            orderNo=int(item["orderNo"]),
            revNo=int(item["revNo"]),
            serNo=int(item["serNo"]),
            variantNo=int(item["variantNo"]),
        )

    async def get_timezone(self) -> str:
        """Return the timezone of the control unit.

        Returns
        -------
        str
            Name of the timezone, e.g. ``Europe/Vienna``.

        """
        response: _Response = await self._post(_TIME_ZONE)
        return str(response[0]["timezone"])

    async def is_remote_maintenance_active(self) -> bool:
        """Return whether remote maintenance is enabled in the settings of the control unit.

        Returns
        -------
        bool
            ``True`` if remote maintenance is enabled.

        """
        response: _Response = await self._post(_REMOTE_MAINTENANCE_ACTIVE)
        return bool(response[0]["active"])

    async def is_remote_maintenance_connected(self) -> bool:
        """Return whether the control unit is connected to the remote maintenance server.

        Returns
        -------
        bool
            ``True`` if the connection is alive.

        """
        response: _Response = await self._post(_REMOTE_MAINTENANCE_CONNECTED)
        return bool(response[0]["connected"])

    async def is_remote_maintenance_server_reachable(self) -> bool:
        """Return whether the control unit reaches the remote maintenance server.

        The control unit checks the server for this request, which takes a few seconds. Don't use it in a regular
        poll.

        Returns
        -------
        bool
            ``True`` if the server is reachable.

        """
        response: _Response = await self._post(_REMOTE_MAINTENANCE_SERVER_REACHABLE)
        return bool(response[0]["reachable"])

    async def set_remote_maintenance_active(self, *, active: bool) -> None:
        """Enable or disable remote maintenance, like the Web HMI does.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        active
            ``True`` to enable remote maintenance, ``False`` to disable it.

        Examples
        --------
        >>> await client.set_remote_maintenance_active(active=True)

        """
        await self._post(_ACTIVATE_REMOTE_MAINTENANCE, _ActivatePayload(activate=active))

    async def read(
        self,
        sections: Iterable[Section],
        *,
        counts: DeviceCounts | None = None,
        limits: Limits = "all",
        message_ids: bool = False,
    ) -> Readings:
        """Read the values of the sections with one request.

        Values are only converted to the type of the endpoint (``bool``, ``float``, ``int``, ``str`` or an enum
        member), not rounded or scaled.

        Parameters
        ----------
        sections
            The sections to read, e.g. ``[HeatPump.STATE, HeatingCircuit.ROOM_TEMPERATURE]``.
        counts
            The installed devices, read with :meth:`get_device_counts` if not given.
        limits
            The endpoints whose limits (``Reading.lower_limit`` and ``upper_limit``) are read: ``all``, ``none``,
            only the ``read_only`` or only the ``writable`` ones. Limits make the request of the Web HMI about twice
            as slow, the others have ``None``.
        message_ids
            Also read the message id (``state.msgId``) of the sections that have one (``Endpoint.message_id``)
            with the same request, see ``Reading.message_id``. A message id the Web HMI doesn't know costs one more
            request, it is left out from then on and its readings have no message id.

        Returns
        -------
        Readings
            One list per section with one reading per device (and consumer), in the requested order.
            Sections of devices that are not installed have an empty list.

        Raises
        ------
        APIError
            ``limits`` is not a valid value.
        UnsupportedVariableError
            The Web HMI doesn't know a variable, see :meth:`filter_supported`.
        InvalidResponseError
            A value can't be converted to the type of its endpoint.

        Examples
        --------
        >>> readings = await client.read([HeatPump.STATE, HeatingCircuit.ROOM_TEMPERATURE], message_ids=True)
        >>> readings[HeatPump.STATE][0].value
        <HeatPumpState.AUTOMATIC: 2>
        >>> readings[HeatingCircuit.ROOM_TEMPERATURE][0].message_id
        MessageId(value=10, kind=<MessageIdKind.DEACTIVATED: 'deactivated'>)

        """
        allowed_limits: tuple[str, ...] = get_args(Limits.__value__)

        # Checked up front, also if no variable is read (e.g. no device of the sections is installed).
        if limits not in allowed_limits:
            message: str = (
                f"Invalid limits {limits!r}! Allowed values are "
                f"{', '.join(map(repr, allowed_limits[:-1]))} and {allowed_limits[-1]!r}"
            )
            raise APIError(message)

        requested: list[Section] = list(dict.fromkeys(sections))
        _counts: DeviceCounts = counts or await self.get_device_counts()

        variables: list[tuple[Section, _Variable, str | None]] = [
            (section, variable, message_id_name)
            for section in requested
            for variable, message_id_name in self._iter_variables_with_message_ids(
                section, _counts, message_ids=message_ids
            )
        ]
        variables, response = await self._read_values(variables, limits)
        items: Iterator[dict[str, Any]] = iter(response)
        readings: Readings = {section: [] for section in requested}

        for section, variable, message_id_name in variables:
            item: dict[str, Any] = next(items)
            message_id: MessageId | None = None if message_id_name is None else self._to_message_id(next(items))
            readings[section].append(self._to_reading(section, variable, item, message_id))

        return readings

    def _iter_variables_with_message_ids(
        self,
        section: Section,
        counts: DeviceCounts,
        /,
        *,
        message_ids: bool,
    ) -> Iterator[tuple[_Variable, str | None]]:
        """Yield the variables of a section with the name of their message id.

        The name is ``None`` without message id or if the Web HMI rejected the message id before.
        """
        template: str | None = section.value.message_id_variable if message_ids else None
        variables: Iterator[_Variable] = self._iter_variables(section, counts, section.value.variable)

        if template is None:
            yield from ((variable, None) for variable in variables)
        else:
            yield from (
                (variable, None if message_id.name in self._unsupported_message_ids else message_id.name)
                for variable, message_id in zip(variables, self._iter_variables(section, counts, template), strict=True)
            )

    async def _read_values(
        self,
        variables: list[tuple[Section, _Variable, str | None]],
        limits: Limits,
        /,
    ) -> tuple[list[tuple[Section, _Variable, str | None]], _Response]:
        """Read the values and their message ids with one request.

        A message id the Web HMI rejects is left out and the request is sent again, an unknown value is raised.

        Returns
        -------
        tuple[list[tuple[Section, _Variable, str | None]], _Response]
            The variables without the rejected message ids and the response, in the order of the variables.

        """
        payload: list[_ReadPayload] = []

        for section, variable, message_id_name in variables:
            payload.append(_ReadPayload(name=variable.name, attr="1" if self._has_limits(section, limits) else "0"))

            if message_id_name is not None:
                payload.append(_ReadPayload(name=message_id_name, attr="0"))

        try:
            return variables, await self._read_payload(payload)
        except UnsupportedVariableError as error:
            if all(message_id_name != error.variable for _, _, message_id_name in variables):
                raise

            rejected: str = error.variable

        self._unsupported_message_ids.add(rejected)

        return await self._read_values(
            [
                (section, variable, None if message_id_name == rejected else message_id_name)
                for section, variable, message_id_name in variables
            ],
            limits,
        )

    @staticmethod
    def _has_limits(section: Section, limits: Limits, /) -> bool:
        """Return whether the limits of a section are read, ``limits`` is already checked by :meth:`read`."""
        match limits:
            case "all":
                return True
            case "none":
                return False
            case "read_only":
                return not section.value.writable

        return section.value.writable

    @staticmethod
    def _iter_variables(section: Section, counts: DeviceCounts, template: str, /) -> Iterator[_Variable]:
        """Yield the variables of a section for the installed devices, in the order of the payload."""
        if not section.value.has_device_index:
            yield _Variable(name=template, position=1, consumer=None)
            return

        quantity: int = section.value.quantity
        count: int = getattr(counts, section.device_type.value)

        for index in range(count):
            if quantity == 1:
                yield _Variable(name=template % index, position=index + 1, consumer=None)
            else:
                # Sections with a quantity > 1 (e.g. two consumers per solar circuit) use a sub index.
                yield from (
                    _Variable(
                        name=template % (index * quantity + sub_index), position=index + 1, consumer=sub_index + 1
                    )
                    for sub_index in range(quantity)
                )

    async def _read_payload(self, payload: list[_ReadPayload], /) -> _Response:
        """Read the variables of the payload with one request, no request for an empty payload."""
        if not payload:
            return []

        return await self._post(_READ_WRITE_VARS, payload)

    def _to_reading(
        self,
        section: Section,
        variable: _Variable,
        item: dict[str, Any],
        message_id: MessageId | None,
        /,
    ) -> Reading:
        """Return the reading of a response item."""
        attributes: dict[str, Any] = item.get("attributes", {})

        return Reading(
            value=self._convert_value(section, item),
            position=variable.position,
            consumer=variable.consumer,
            lower_limit=self._to_limit(attributes.get("lowerLimit")),
            upper_limit=self._to_limit(attributes.get("upperLimit")),
            unit=section.value.unit,
            message_id=message_id,
        )

    @staticmethod
    def _to_message_id(item: dict[str, Any], /) -> MessageId:
        """Return the message id of a response item."""
        value: int = int(item["value"])
        return MessageId(value=value, kind=MessageIdKind.from_message_id(value))

    @staticmethod
    def _convert_value(section: Section, item: dict[str, Any], /) -> Value:
        """Return the value converted to the type of the endpoint.

        Raises
        ------
        InvalidResponseError
            The value can't be converted.

        """
        value_type: type = section.value.value_type
        text: str = str(item["value"])

        try:
            if value_type is bool:
                return _BOOL_VALUES[text.lower()]

            if issubclass(value_type, Enum):
                return value_type(int(text))

            return value_type(text)
        except (KeyError, ValueError) as error:
            message: str = f"Can't convert {text!r} of {section} to {value_type.__name__}"
            raise InvalidResponseError(message) from error

    @staticmethod
    def _to_limit(limit: str | None, /) -> float | None:
        """Return a limit of the Web HMI as float, ``None`` if there is none."""
        if limit is None:
            return None

        try:
            return float(limit)
        except ValueError:
            return None

    async def write(self, values: Mapping[Section, Sequence[WriteValue | None]]) -> None:
        """Write values with one request.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        values
            One sequence per section with one value per device, the first item is position 1 and ``None`` skips a
            device. Sections with more than one value per device (``quantity``) take one value per consumer
            (device 1 consumer 1, device 1 consumer 2, device 2 consumer 1, ...). System-wide sections take
            one value.

        Raises
        ------
        APIError
            A section is read-only, the value doesn't match the type of the endpoint or more than one value is given
            for a system-wide section.

        Examples
        --------
        >>> await client.write(
        ...     {
        ...         HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL: [20, None, 21.5],
        ...         HeatingCircuit.OPERATING_MODE: [HeatingCircuitOperatingMode.AUTO],
        ...     }
        ... )

        """
        payload: list[_WritePayload] = [
            item
            for section, section_values in values.items()
            for item in self._get_write_payload(section, section_values)
        ]

        if payload:
            await self._post(_WRITE_VARS, payload)

    def _get_write_payload(self, section: Section, values: Sequence[WriteValue | None], /) -> list[_WritePayload]:
        """Return the write payload of one section, including the extra writes it needs.

        Raises
        ------
        APIError
            The section is read-only, a value is invalid or more than one value is given for a system-wide section.

        """
        message: str

        if not section.value.writable:
            message = f"{section} is read-only"
            raise APIError(message)

        if isinstance(values, str):
            message = f"{section} needs a sequence of values, not a string"
            raise APIError(message)

        if not section.value.has_device_index and len(values) > 1:
            message = f"{section} is system wide, only one value can be written"
            raise APIError(message)

        template: str = section.value.variable
        payload: list[_WritePayload] = [
            _WritePayload(
                name=template % index if section.value.has_device_index else template,
                value=self._to_write_value(section, value),
            )
            for index, value in enumerate(values)
            if value is not None
        ]

        if section is SolarCircuit.CONSUMER_1_PRIORITY:
            payload += self._get_write_payload(
                SolarCircuit["_CONSUMER_PRIORITY"], self._get_consumer_priorities(values)
            )

        return payload

    @staticmethod
    def _to_write_value(section: Section, value: WriteValue, /) -> str:
        """Return a value as written to the Web HMI.

        Raises
        ------
        APIError
            The value doesn't match the type of the endpoint.

        """
        value_type: type = section.value.value_type

        if isinstance(value, bool):
            if value_type is bool:
                return _WRITE_TRUE if value else _WRITE_FALSE
        elif isinstance(value, Enum):
            # Members with more than one value (e.g. some heat pump substates) can't be written.
            if isinstance(value, value_type) and isinstance(value.value, int):
                return str(value.value)
        elif isinstance(value, int):
            if value_type in {float, int}:
                return str(value)
        elif isinstance(value, float):
            if value_type is float:
                return str(value)
        elif value_type is str:
            return value

        message: str = f"Invalid value {value!r} for {section}, expected {value_type.__name__}"
        raise APIError(message)

    @staticmethod
    def _get_consumer_priorities(values: Sequence[WriteValue | None], /) -> list[WriteValue | None]:
        """Return the priorities of the consumers for a write of ``SolarCircuit.CONSUMER_1_PRIORITY``.

        The switch in the Web HMI also writes the priority of the first consumer of each solar circuit:
        14 (low) if consumer 1 has priority, 15 (high) if not. The second consumer is not written.
        """
        priorities: list[WriteValue | None] = []

        for value in values:
            priority: int | None = None

            if value is not None:
                priority = _CONSUMER_PRIORITY_LOW if value else _CONSUMER_PRIORITY_HIGH

            priorities += [priority, None]

        return priorities

    async def filter_supported(
        self,
        sections: Iterable[Section],
        *,
        counts: DeviceCounts | None = None,
    ) -> list[Section]:
        """Return the sections that are supported by the Web HMI software version.

        All variables are read with one request. The Web HMI rejects a request with an unknown variable as a whole,
        so each unknown variable costs one more request. A section is supported if the Web HMI knows its variables
        of all installed devices. Sections of devices that are not installed are skipped.

        Parameters
        ----------
        sections
            The sections to check, e.g. ``[HeatPump.COP, HeatPump.HEATING_SPF]``.
        counts
            The installed devices, read with :meth:`get_device_counts` if not given.

        Returns
        -------
        list[Section]
            The supported sections, in the requested order and each once.

        Raises
        ------
        APIError
            The request failed for another reason than an unknown variable.

        """
        _counts: DeviceCounts = counts or await self.get_device_counts()

        names: dict[Section, list[str]] = {
            section: [variable.name for variable in self._iter_variables(section, _counts, section.value.variable)]
            for section in sections
        }
        # A variable that is requested more than once is checked once.
        remaining: list[str] = list(dict.fromkeys(name for section_names in names.values() for name in section_names))
        unsupported: set[str] = set()

        while remaining:
            try:
                await self._read_payload([_ReadPayload(name=name, attr="0") for name in remaining])
            except UnsupportedVariableError as error:
                if error.variable not in remaining:
                    raise

                unsupported.add(error.variable)
                remaining.remove(error.variable)
            else:
                break

        return [
            section
            for section, section_names in names.items()
            if section_names and unsupported.isdisjoint(section_names)
        ]

    async def get_curve_tables(self) -> dict[str, CurveTable]:
        """Return the curve tables of the line table pool, used as heating or cooling curves.

        Returns
        -------
        dict[str, CurveTable]
            The curves by name, e.g. ``HC1``.

        """
        indexes: dict[str, int] = await self._get_curve_table_indexes()

        names: list[str] = [
            name
            for index in indexes.values()
            for name in (
                f"{_LINE_TABLE % index}.noOfPoints",
                *(
                    f"{_LINE_TABLE % index}.points[{point_index}].{axis}"
                    for point_index in range(MAX_CURVE_TABLE_POINTS)
                    for axis in ("x", "y")
                ),
            )
        ]
        response: _Response = await self._read_payload([_ReadPayload(name=name, attr="0") for name in names])

        curves: dict[str, CurveTable] = {}

        for name, items in zip(indexes, batched(response, 1 + 2 * MAX_CURVE_TABLE_POINTS, strict=True), strict=True):
            number_of_points: int = min(int(items[0]["value"]), MAX_CURVE_TABLE_POINTS)
            curves[name] = CurveTable(
                name=name,
                points=tuple(
                    CurvePoint(outdoor=float(items[1 + 2 * i]["value"]), flow=float(items[2 + 2 * i]["value"]))
                    for i in range(number_of_points)
                ),
            )

        return curves

    async def _get_curve_table_indexes(self) -> dict[str, int]:
        """Return the index in the line table pool of each curve table by name."""
        response: _Response = await self._read_payload(
            [_ReadPayload(name=f"{_LINE_TABLE % index}.name", attr="0") for index in range(_LINE_TABLE_POOL_SIZE)]
        )

        return {
            str(item["value"]): index
            for index, item in enumerate(response)
            if str(item["value"]).startswith(_CURVE_TABLE_NAME_PREFIX)
        }

    async def set_curve_table_points(self, name: str, points: Sequence[CurvePoint]) -> None:
        """Write the points of a curve table.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        name
            Name of the curve, e.g. ``HC1``.
        points
            The points of the curve, ``MIN_CURVE_TABLE_POINTS`` to ``MAX_CURVE_TABLE_POINTS``.

        Raises
        ------
        APIError
            The curve doesn't exist or the number of points is invalid.

        Examples
        --------
        >>> await client.set_curve_table_points(
        ...     "HC1",
        ...     [CurvePoint(outdoor=-20, flow=55), ..., CurvePoint(outdoor=20, flow=25)],
        ... )

        """
        message: str

        if not MIN_CURVE_TABLE_POINTS <= len(points) <= MAX_CURVE_TABLE_POINTS:
            message = (
                f"A curve table needs {MIN_CURVE_TABLE_POINTS} to {MAX_CURVE_TABLE_POINTS} points, not {len(points)}"
            )
            raise APIError(message)

        indexes: dict[str, int] = await self._get_curve_table_indexes()

        try:
            line_table: str = _LINE_TABLE % indexes[name]
        except KeyError as error:
            message = f"Invalid curve table {name!r}! Allowed values are {list(indexes)}"
            raise APIError(message) from error

        payload: list[_WritePayload] = [_WritePayload(name=f"{line_table}.noOfPoints", value=str(len(points)))]

        # Unused points are reset, like the Web HMI does.
        for point_index in range(MAX_CURVE_TABLE_POINTS):
            point: CurvePoint = points[point_index] if point_index < len(points) else CurvePoint(outdoor=0, flow=0)
            payload += [
                _WritePayload(name=f"{line_table}.points[{point_index}].x", value=str(point.outdoor)),
                _WritePayload(name=f"{line_table}.points[{point_index}].y", value=str(point.flow)),
            ]

        payload.append(_WritePayload(name=f"{line_table}.verCnt", value=_SAVE_LINE_TABLE))

        await self._post(_WRITE_VARS, payload)

    async def get_alarm_count(self) -> int:
        """Return the number of pending alarms.

        The request is cheaper than :meth:`get_alarms`, e.g. to read the alarms only when there are any.

        Returns
        -------
        int
            The number of pending alarms.

        """
        response: _Response = await self._post(_ALARM_COUNT)
        return int(response[0]["value"])

    async def get_alarms(self, *, language: str = "en") -> list[Alarm]:
        """Return the pending alarms, the same list as on the display and in the Web HMI.

        An alarm is removed by the control unit as soon as its cause is gone.

        Parameters
        ----------
        language
            Language code of the alarm texts, e.g. ``en`` or ``de``.

        Returns
        -------
        list[Alarm]
            The pending alarms.

        Raises
        ------
        InvalidResponseError
            The timestamp of an alarm is not a valid date.

        Examples
        --------
        >>> alarms = await client.get_alarms(language="de")
        >>> timezone = ZoneInfo(await client.get_timezone())
        >>> [alarm.timestamp.replace(tzinfo=timezone) for alarm in alarms]

        """
        response: _Response = await self._post(f"{_ALARMS}&{urlencode({'languageCode': language})}")
        return [self._to_alarm(item) for item in response[0]["alarms"]]

    @staticmethod
    def _to_alarm(item: dict[str, Any], /) -> Alarm:
        """Return the alarm of a response item.

        Raises
        ------
        InvalidResponseError
            The timestamp is not a valid date.

        """
        timestamp: dict[str, int] = item["timeStamp"]

        try:
            # Without a timezone, as the Web HMI delivers the local time of the control unit.
            raised: datetime = datetime.combine(
                date(timestamp["year"], timestamp["month"], timestamp["day"]),
                time(
                    timestamp["hours"],
                    timestamp["minutes"],
                    timestamp["seconds"],
                    timestamp.get("milliseconds", 0) * 1000,
                ),
            )
        except ValueError as error:
            message: str = f"Invalid timestamp of alarm {item['alarmNr']}: {timestamp}"
            raise InvalidResponseError(message) from error

        return Alarm(
            number=int(item["alarmNr"]),
            component=int(item["compNr"]),
            instance=int(item["instanceNr"]),
            priority=AlarmPriority(int(item["prio"])),
            acknowledgeable=bool(item["quittable"]),
            short_text=str(item["shortText"]),
            long_text=str(item["longText"]),
            timestamp=raised,
        )
