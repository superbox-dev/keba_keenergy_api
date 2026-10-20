# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""KEBA KeEnergy API endpoint definitions."""

import json
import re
from collections.abc import Callable
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from re import Pattern
from typing import Any
from typing import Final
from typing import NamedTuple
from typing import TypeAlias
from typing import TypedDict
from typing import TypeVar

from aiohttp import ClientError
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import ContentTypeError

from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.constants import MAX_HEATING_CURVE_POINTS
from keba_keenergy_api.constants import MIN_HEATING_CURVE_POINTS
from keba_keenergy_api.constants import BoolEnum
from keba_keenergy_api.constants import BufferTank
from keba_keenergy_api.constants import BufferTankOperatingMode
from keba_keenergy_api.constants import Endpoint
from keba_keenergy_api.constants import EndpointPath
from keba_keenergy_api.constants import ExternalHeatSource
from keba_keenergy_api.constants import FloatEndpoint
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HeatPumpOperatingMode
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.constants import LineTablePool
from keba_keenergy_api.constants import PassiveCooling
from keba_keenergy_api.constants import Photovoltaics
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import SwitchValve
from keba_keenergy_api.constants import System
from keba_keenergy_api.constants import SystemOperatingMode
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import APITimeoutError
from keba_keenergy_api.error import AuthenticationError
from keba_keenergy_api.error import InvalidJsonError

_T = TypeVar("_T")

# Attributes returned by the Web HMI that are not useful for API consumers.
_IGNORED_ATTRIBUTES: Final[frozenset[str]] = frozenset(
    {"unitId", "longText", "formatId", "dynLowerLimit", "dynUpperLimit"}
)
# Number of heating curve slots in the line table pool that are scanned for heating curves.
_HEATING_CURVE_POOL_SIZE: Final[int] = 30


class ReadPayload(TypedDict):
    """Payload for reading an API endpoint."""

    name: str
    attr: str


class WritePayload(TypedDict):
    """Payload for writing an API endpoint."""

    name: str
    value: str


class ReadChildrenPayload(TypedDict):
    """Payload for reading child API endpoints."""

    parent: str
    filter: str


@dataclass
class Position:
    """Number of installed devices per device type, as configured in the control unit."""

    heat_pump: int
    heat_circuit: int
    solar_circuit: int
    buffer_tank: int
    hot_water_tank: int
    external_heat_source: int
    switch_valve: int

    @property
    def passive_cooling(self) -> int:
        """Return the number of passive cooling units (one per heat pump)."""
        return self.heat_pump


class HeatingCurvePoint(NamedTuple):
    """Point on a heating curve."""

    outdoor: float
    flow: float


class Value(TypedDict, total=False):
    """Converted API value with its (cleaned) attributes, e.g. limits and ``raw_value``."""

    value: Any
    attributes: dict[str, Any]


ValueList: TypeAlias = list[Value] | list[list[Value]]
ValueResponse: TypeAlias = dict[str, Value | ValueList]
Payload: TypeAlias = list[ReadPayload | WritePayload]
Response: TypeAlias = list[dict[str, Any]]

HeatingCurvePoints = tuple[HeatingCurvePoint, ...]
HeatingCurves: TypeAlias = dict[str, HeatingCurvePoints]


class BaseEndpoints:
    """Base class for all endpoint classes.

    Holds the connection settings and the shared logic to build request payloads, send them to the
    Web HMI and convert the responses.
    """

    KEY_PATTERN: Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

    def __init__(
        self,
        base_url: str,
        *,
        auth: str | None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize the endpoints.

        Parameters
        ----------
        base_url
            Base URL of the control unit, e.g. ``https://ap4400.local``.
        auth
            Value of the ``Authorization`` header, or ``None`` without authentication.
        ssl
            Whether HTTPS is used.
        skip_ssl_verification
            Disable TLS certificate verification.
        session
            Optional shared session. Without a session, a new one is created and closed per request.

        """
        self._base_url: str = base_url
        self._auth: str | None = auth
        self._ssl: bool = ssl
        self._skip_ssl_verification: bool = skip_ssl_verification
        self._session: ClientSession | None = session

    async def _post(self, payload: str | None = None, endpoint: str | None = None) -> Response:
        """Send a POST request to the Web HMI and return the JSON response as a list.

        Parameters
        ----------
        payload
            JSON encoded request body.
        endpoint
            Endpoint path, e.g. ``/var/readWriteVars``.

        Returns
        -------
        Response
            The response items. A single JSON object is wrapped in a list.

        Raises
        ------
        AuthenticationError
            The credentials were rejected (HTTP 401).
        InvalidJsonError
            The response is not valid JSON.
        APITimeoutError
            The request timed out (also a ``TimeoutError``).
        APIError
            The Web HMI (or a reverse proxy) returned a status other than 2xx, the connection failed
            or the request timed out.

        """
        session: ClientSession = (
            self._session
            if self._session and not self._session.closed
            else ClientSession(timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT))
        )

        try:
            url: str = f"{self._base_url}{endpoint or ''}"
            headers: dict[str, str] = {}

            if self._auth is not None:
                headers["Authorization"] = self._auth

            async with session.post(
                url,
                headers=headers,
                ssl=False if self._skip_ssl_verification else self._ssl,
                data=payload,
            ) as resp:
                if resp.status == HTTPStatus.UNAUTHORIZED:
                    raise AuthenticationError(status=HTTPStatus.UNAUTHORIZED)

                # Everything else than 2xx is an error, e.g. also a redirect or a 502 of a reverse proxy.
                if not HTTPStatus.OK <= resp.status < HTTPStatus.MULTIPLE_CHOICES:
                    error_message: str = await resp.text()

                    if resp.status == HTTPStatus.INTERNAL_SERVER_ERROR:
                        error_message = self._get_developer_message(error_message)

                    raise APIError(error_message, status=HTTPStatus(resp.status))

                response: list[dict[str, Any]] = await resp.json()

                if isinstance(response, dict):
                    response = [response]

                return response
        except (json.JSONDecodeError, ContentTypeError) as error:
            message: str = f"Invalid JSON response! {error}"
            raise InvalidJsonError(message) from error
        # Before ClientError, as the aiohttp timeouts (e.g. ConnectionTimeoutError) are also a ClientError.
        except TimeoutError as error:
            message = f"Request timed out! {error}".rstrip()
            raise APITimeoutError(message) from error
        except ClientError as error:
            raise APIError(str(error)) from error
        finally:
            # Close the session opened for this request, also if the shared session was already closed.
            if session is not self._session:
                await session.close()

    @staticmethod
    def _get_developer_message(text: str, /) -> str:
        """Return the developer message of a Web HMI error response (HTTP 500), otherwise the response text."""
        try:
            error_response: Any = json.loads(text)
        except ValueError:
            return text

        if isinstance(error_response, dict) and "developerMessage" in error_response:
            return str(error_response["developerMessage"])

        return text

    def _get_real_key(self, key: Section, /, *, key_prefix: bool = True) -> str:
        """Return the response key of a section, e.g. ``heat_pump_state`` or ``state``."""
        class_name: str = key.__class__.__name__
        _real_key: str = key.name.lower()

        if key_prefix is True:
            _real_key = f"{self.KEY_PATTERN.sub('_', class_name).lower()}_{_real_key}"

        return _real_key

    @staticmethod
    def _normalize_request(
        request: Section | list[Section],
        position: int | Position | list[int],
        /,
    ) -> tuple[list[Section], Position | list[int]]:
        """Return the request and the position as lists (a ``Position`` is kept as it is)."""
        return (
            request if isinstance(request, list) else [request],
            [position] if isinstance(position, int) else position,
        )

    def _get_device_indexes(self, section: Section, position: Position | list[int]) -> list[int | None]:
        """Return the zero-based device indexes to request for a section.

        ``None`` means the section has no device index (system wide). Devices that are not installed are left out.
        """
        if isinstance(section, Photovoltaics | System):
            return [None]

        if isinstance(position, Position):
            position_key: str = f"{self.KEY_PATTERN.sub('_', section.__class__.__name__).lower()}"
            return list(range(getattr(position, position_key, None) or 0))

        return [p - 1 for p in position if p != 0] if position else [None]

    def _iter_variable_names(
        self,
        section: Section,
        position: Position | list[int],
        template: str | None = None,
    ) -> Iterator[str]:
        """Yield the variable names of a section, in the order of the read payload.

        Parameters
        ----------
        section
            The section to resolve.
        position
            Installed device position(s).
        template
            Variable name template, defaults to the section path. Used e.g. for the message id path.

        """
        template = template or section.value.value
        quantity: int = section.value.quantity

        for idx in self._get_device_indexes(section=section, position=position):
            if idx is None:
                yield template
            elif quantity == 1:
                yield template % idx
            else:
                # Sections with a quantity > 1 (e.g. two consumers per solar circuit) use a sub index.
                yield from (template % sub_idx for sub_idx in range(idx * quantity, (idx + 1) * quantity))

    def _generate_read_payload(
        self,
        request: list[Section],
        position: Position | list[int],
        *,
        extra_attributes: bool = False,
    ) -> Payload:
        """Build the payload to read all requested sections with one request."""
        attr: str = str(int(extra_attributes is True))

        return [
            ReadPayload(name=name, attr=attr)
            for section in request
            for name in self._iter_variable_names(section, position)
        ]

    def _generate_message_id_requests(
        self,
        request: list[Section],
        position: Position | list[int],
    ) -> list[tuple[Section, str]]:
        """Return one (section, path) pair per message id variable, in the order of the read payload."""
        return [
            (section, name)
            for section in request
            if (path := section.value.message_id_path)
            for name in self._iter_variable_names(section, position, template=path)
        ]

    async def _read_message_ids(self, paths: list[str]) -> list[int]:
        """Read the given message id variables with one request."""
        if not paths:
            return []

        response: Response = await self._post(
            payload=json.dumps([ReadPayload(name=path, attr="0") for path in paths]),
            endpoint=EndpointPath.READ_WRITE_VARS,
        )

        return [int(item["value"]) for item in response]

    @staticmethod
    def _convert_raw_value(section: Section, item: dict[str, Any]) -> float | int | str:
        """Convert a single response item to the endpoint type (without the human-readable mapping)."""
        try:
            value: float | int | str = section.value.value_type(item["value"])
        except ValueError as error:
            message: str = f'Can\'t convert value to type "{section.value.value_type.__name__}"! {item}'
            raise APIError(message) from error

        value = section.value.normalize(value)

        if isinstance(section.value, FloatEndpoint) and isinstance(value, float):
            value = round(value, section.value.decimals)

        if value in ["true", "false"]:
            value = 1 if value == "true" else 0

        return value

    @staticmethod
    def _to_human_readable(section: Section, value: float | str, item: dict[str, Any]) -> float | int | str:
        """Map a raw value to its human-readable name, if the endpoint defines one."""
        if not section.value.human_readable:
            return value

        try:
            return str(section.value.human_readable(value).name.lower())
        except ValueError as error:
            message: str = f"Can't convert value to human readable value! {item}"
            raise APIError(message) from error

    @classmethod
    def _clean_attributes(cls, item: dict[str, Any]) -> dict[str, Any]:
        """Return the attributes of a response item with snake_case keys, without ignored keys."""
        attributes: dict[str, Any] = item.get("attributes", {})

        return {
            cls.KEY_PATTERN.sub("_", key).lower(): value
            for key, value in attributes.items()
            if key not in _IGNORED_ATTRIBUTES
        }

    def _get_response_data(
        self,
        response: Response,
        /,
        request: list[Section],
        position: Position | list[int],
        *,
        key_prefix: bool = True,
        human_readable: bool = True,
    ) -> dict[str, ValueList]:
        """Map a read response back to the requested sections.

        The response items are consumed in the same order as the read payload was built.
        Sections with a quantity > 1 return a nested list per device.
        """
        items: Iterator[dict[str, Any]] = iter(response)
        _response_without_quantity: dict[str, list[Value]] = {}
        _response_with_quantity: dict[str, list[list[Value]]] = {}

        for section in request:
            response_key: str = self._get_real_key(section, key_prefix=key_prefix)

            for _ in self._get_device_indexes(section=section, position=position):
                response_group: list[Value] = []

                for _ in range(section.value.quantity):
                    item: dict[str, Any] = next(items)
                    raw_value: float | int | str = self._convert_raw_value(section, item)
                    value: float | int | str = (
                        self._to_human_readable(section, raw_value, item) if human_readable else raw_value
                    )
                    attributes: dict[str, Any] = self._clean_attributes(item)

                    if value != raw_value:
                        attributes = attributes | {"raw_value": raw_value}

                    response_group.append({"value": value, "attributes": attributes})

                if section.value.quantity == 1:
                    _response_without_quantity.setdefault(response_key, []).append(response_group[0])
                else:
                    _response_with_quantity.setdefault(response_key, []).append(response_group)

        return {**_response_without_quantity, **_response_with_quantity}

    async def _read_data(
        self,
        request: Section | list[Section],
        position: int | Position | list[int] = 1,
        *,
        key_prefix: bool = True,
        human_readable: bool = True,
        extra_attributes: bool = False,
    ) -> dict[str, ValueList]:
        """Read the requested sections with one request and return the converted values."""
        request, position = self._normalize_request(request, position)

        payload: Payload = self._generate_read_payload(
            request=request,
            position=position,
            extra_attributes=extra_attributes,
        )

        response: Response = await self._post(
            payload=json.dumps(payload),
            endpoint=EndpointPath.READ_WRITE_VARS,
        )

        return self._get_response_data(
            response,
            request=request,
            position=position,
            key_prefix=key_prefix,
            human_readable=human_readable,
        )

    def _generate_write_payload(self, request: dict[Section, Any]) -> Payload:
        """Build the write payload. Invalid and read-only sections are skipped."""
        payload: Payload = []

        for section, values in request.items():
            if isinstance(section, Section):
                payload += self._generate_endpoint_write_payload(section.value, values)

        return payload

    def _generate_endpoint_write_payload(self, endpoint: Endpoint, values: object) -> Payload:
        """Build the write payload of one endpoint.

        A single value is written for position 1, a list or tuple writes one value per device index
        (``None`` skips a device).

        Raises
        ------
        APIError
            More than one value is given for a system-wide endpoint.

        """
        if endpoint.read_only:
            return []

        _values: list[object] = list(values) if isinstance(values, list | tuple) else [values]

        has_device_index: bool = "%s" in endpoint.value

        if not has_device_index and len(_values) > 1:
            message: str = f'"{endpoint.value}" is system wide, only one value can be written!'
            raise APIError(message)

        payload: Payload = [
            WritePayload(name=endpoint.value % idx if has_device_index else endpoint.value, value=str(value))
            for idx, value in enumerate(_values)
            if value is not None
        ]

        # Some endpoints need additional writes (e.g. the solar circuit priority).
        for extra_section, extra_values in endpoint.extra_writes(_values).items():
            payload += self._generate_endpoint_write_payload(extra_section.value, extra_values)

        return payload

    async def _write_values(self, request: dict[Section, Any]) -> None:
        """Write the requested values with one request."""
        payload: Payload = self._generate_write_payload(request)

        if not payload:
            return

        await self._post(
            payload=json.dumps(payload),
            endpoint=f"{EndpointPath.READ_WRITE_VARS}?action=set",
        )

    @staticmethod
    def _get_allowed_values(enum: type[Enum], /) -> list[str]:
        """Return all names and values of an enum, for error messages."""
        return [item for pair in ((_.name, str(_.value)) for _ in enum) for item in pair]

    @classmethod
    def _parse_enum_value(cls, value: int | str, enum: type[Enum], /) -> int:
        """Return the integer value for a mode given as integer or (case-insensitive) enum name."""
        if isinstance(value, int):
            return value

        try:
            return int(enum[value.upper()].value)
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {cls._get_allowed_values(enum)}"
            raise APIError(message) from error

    @staticmethod
    def _values_for_position(value: _T, position: int, /) -> list[_T | None]:
        """Return a write list that only sets the value for the given (1-based) position."""
        return [value if position == p else None for p in range(1, position + 1)]

    @staticmethod
    def _get_item(value: Value | list[Value], index: int = 0, /) -> Value:
        """Return the item at the index of a nested value (quantity > 1), or the value itself."""
        return value[index] if isinstance(value, list) else value

    @staticmethod
    def _to_int_or_str(value: float | str, /) -> int | str:
        """Return a value as integer if possible, otherwise as string."""
        try:
            return int(value)
        except ValueError:
            return str(value)

    async def _read_value(
        self,
        section: Section,
        position: int,
        convert: Callable[[float | str], _T],
        /,
        *,
        human_readable: bool,
        index: int = 0,
        attribute: str | None = None,
    ) -> _T:
        """Read one value (or attribute) of one device, including the extra attributes (e.g. limits).

        The getters read exactly one device, so the response holds one entry, even for ``position > 1``.
        """
        if position < 1:
            message: str = f"Invalid position {position}! Positions start at 1"
            raise APIError(message)

        response: dict[str, ValueList] = await self._read_data(
            request=section,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )

        item: Value = self._get_item(response[self._get_real_key(section)][0], index)

        return convert(item["attributes"][attribute] if attribute else item["value"])

    async def _read_float(
        self,
        section: Section,
        position: int = 1,
        /,
        *,
        human_readable: bool = True,
        index: int = 0,
        attribute: str | None = None,
    ) -> float:
        """Read one value (or attribute) of one device as float."""
        return await self._read_value(
            section, position, float, human_readable=human_readable, index=index, attribute=attribute
        )

    async def _read_int(
        self,
        section: Section,
        position: int = 1,
        /,
        *,
        human_readable: bool = True,
        index: int = 0,
        attribute: str | None = None,
    ) -> int:
        """Read one value (or attribute) of one device as integer."""
        return await self._read_value(
            section, position, int, human_readable=human_readable, index=index, attribute=attribute
        )

    async def _read_str(
        self,
        section: Section,
        position: int = 1,
        /,
        *,
        human_readable: bool = True,
        index: int = 0,
    ) -> str:
        """Read one value of one device as string."""
        return await self._read_value(section, position, str, human_readable=human_readable, index=index)

    async def _read_int_or_str(
        self,
        section: Section,
        position: int = 1,
        /,
        *,
        human_readable: bool = True,
        index: int = 0,
    ) -> int | str:
        """Read one value of one device as integer, or as string if it is human-readable."""
        return await self._read_value(
            section, position, self._to_int_or_str, human_readable=human_readable, index=index
        )

    async def _read_heating_curve_points(self, heating_curves: tuple[tuple[int, str], ...], /) -> HeatingCurves:
        """Read the points of the given (index, name) heating curves with one request."""
        if not heating_curves:
            return {}

        # Only the values are needed, so no attributes are requested (attr="0").
        payload: Payload = [
            ReadPayload(name=name, attr="0")
            for idx, _ in heating_curves
            for name in (
                LineTablePool.HEATING_CURVE_NAME.value.value % idx,
                LineTablePool.HEATING_CURVE_POINTS.value.value % idx,
                *(
                    point.value.value % (idx, point_idx)
                    for point_idx in range(MAX_HEATING_CURVE_POINTS)
                    for point in (LineTablePool.HEATING_CURVE_POINT_X, LineTablePool.HEATING_CURVE_POINT_Y)
                ),
            )
        ]

        response: Response = await self._post(
            payload=json.dumps(payload),
            endpoint=EndpointPath.READ_WRITE_VARS,
        )

        data: HeatingCurves = {}

        data_idx: int = 0
        points_per_table: int = MAX_HEATING_CURVE_POINTS
        values_per_point: int = 2

        valid_curves: set[str] = {name for _, name in heating_curves}

        for _ in heating_curves:
            name: str = response[data_idx]["value"]

            if name in valid_curves:
                no_of_points: int = min(int(response[data_idx + 1]["value"]), points_per_table)
                raw = response[data_idx + 2 : data_idx + 2 + points_per_table * values_per_point]

                points = tuple(
                    HeatingCurvePoint(
                        outdoor=float(raw[i]["value"]),
                        flow=float(raw[i + 1]["value"]),
                    )
                    for i in range(0, no_of_points * values_per_point, values_per_point)
                )

                data[name] = points

            data_idx += 2 + points_per_table * values_per_point

        return data

    async def _write_for_position(self, section: Section, value: float | str, position: int = 1, /) -> None:
        """Write a value for one (1-based) position, all other positions are left unchanged."""
        await self._write_values(request={section: self._values_for_position(value, position)})

    async def _write_mode(self, section: Section, mode: int | str, enum: type[Enum], position: int = 1, /) -> None:
        """Write a mode given as integer or (case-insensitive) enum name for one (1-based) position."""
        await self._write_for_position(section, self._parse_enum_value(mode, enum), position)


class SystemEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the system data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.system.get_info()

    """

    async def get_positions(self) -> Position:
        """Get the number of installed devices e.g. heat circuit, solar circuit, etc.

        Returns
        -------
        Position
            The number of installed devices per device type

        """
        response: dict[str, ValueList] = await self._read_data(
            request=[
                System.HEAT_PUMP_NUMBERS,
                System.HEAT_CIRCUIT_NUMBERS,
                System.SOLAR_CIRCUIT_NUMBERS,
                System.BUFFER_TANK_NUMBERS,
                System.HOT_WATER_TANK_NUMBERS,
                System.EXTERNAL_HEAT_SOURCE_NUMBERS,
                System.SWITCH_VALVE_NUMBERS,
            ],
            key_prefix=False,
            extra_attributes=True,
        )

        positions: dict[str, int] = {}

        for key, values in response.items():
            item: Value = self._get_item(values[0])
            positions[key.replace("_numbers", "")] = int(item["value"])

        return Position(**positions)

    async def get_info(self) -> dict[str, Any]:
        """Get the system information.

        Returns
        -------
        dict[str, Any]
            A dictionary with system information

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getSystemInstalled",
        )
        response[0].pop("ret", None)
        return response[0]

    async def get_hmi_info(self) -> dict[str, Any]:
        """Get the Web HMI information.

        Returns
        -------
        dict[str, Any]
            A dictionary with Web HMI information

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getHmiInstalled",
        )
        response[0].pop("ret", None)
        return response[0]

    async def get_device_info(self) -> dict[str, Any]:
        """Get the control unit information.

        Returns
        -------
        dict[str, Any]
            A dictionary with control unit information

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.DEVICE_CONTROL}?action=getDeviceInfo",
        )
        response[0].pop("ret", None)
        return response[0]

    async def get_number_of_buffer_tanks(self) -> int:
        """Get the number of buffer tanks.

        Returns
        -------
        int
            Number of installed buffer tanks

        """
        return await self._read_int(System.BUFFER_TANK_NUMBERS)

    async def get_number_of_hot_water_tanks(self) -> int:
        """Get the number of hot water tanks.

        Returns
        -------
        int
            Number of installed hot water tanks

        """
        return await self._read_int(System.HOT_WATER_TANK_NUMBERS)

    async def get_number_of_heat_pumps(self) -> int:
        """Get the number of heat pumps.

        Returns
        -------
        int
            Number of installed heat pumps

        """
        return await self._read_int(System.HEAT_PUMP_NUMBERS)

    async def get_number_of_heating_circuits(self) -> int:
        """Get the number of heating circuits.

        Returns
        -------
        int
            Number of installed heating circuits

        """
        return await self._read_int(System.HEAT_CIRCUIT_NUMBERS)

    async def get_number_of_external_heat_sources(self) -> int:
        """Get the number of external heat sources.

        Returns
        -------
        int
            Number of installed external heat sources

        """
        return await self._read_int(System.EXTERNAL_HEAT_SOURCE_NUMBERS)

    async def get_number_of_switch_valves(self) -> int:
        """Get the number of switch valves.

        Returns
        -------
        int
            Number of installed switch valves

        """
        return await self._read_int(System.SWITCH_VALVE_NUMBERS)

    async def has_photovoltaics(self, *, human_readable: bool = True) -> int | str:
        """Check if photovoltaics is available.

        Parameters
        ----------
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(System.HAS_PHOTOVOLTAICS, human_readable=human_readable)

    async def has_outdoor_temperature(self, *, human_readable: bool = True) -> int | str:
        """Check if outdoor temperature sensor is available.

        Parameters
        ----------
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(System.HAS_OUTDOOR_TEMPERATURE, human_readable=human_readable)

    async def get_outdoor_temperature(self) -> float:
        """Get the outdoor temperature.

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(System.OUTDOOR_TEMPERATURE)

    async def get_operating_mode(self, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the system.

        Parameters
        ----------
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            -1(SETUP) / (0) STANDBY / (1) SUMMER / (2) AUTO_HEAT / (3) AUTO_COOL / (4) AUTO

        """
        return await self._read_int_or_str(System.OPERATING_MODE, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str) -> None:
        """Set the operating mode from the system.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or STANDBY

        """
        _mode: int = self._parse_enum_value(mode, SystemOperatingMode)

        await self._write_values(request={System.OPERATING_MODE: _mode})

    async def get_cpu_usage(self) -> float:
        """Get the CPU usage.

        Returns
        -------
        float
            CPU usage in percent

        """
        return await self._read_float(System.CPU_USAGE) / 10

    async def get_webview_cpu_usage(self) -> float:
        """Get the webview CPU usage.

        Returns
        -------
        float
            Webview CPU usage in percent

        """
        return await self._read_float(System.WEBVIEW_CPU_USAGE) / 10

    async def get_webserver_cpu_usage(self) -> float:
        """Get the webserver CPU usage.

        Returns
        -------
        float
            Webserver CPU usage in percent

        """
        return await self._read_float(System.WEBSERVER_CPU_USAGE) / 10

    async def get_control_cpu_usage(self) -> float:
        """Get the control CPU usage.

        Returns
        -------
        float
            Control CPU usage in percent

        """
        return await self._read_float(System.CONTROL_CPU_USAGE) / 10

    async def get_ram_usage(self) -> int:
        """Get the RAM usage.

        Returns
        -------
        int
            RAM usage in kilobyte

        """
        return await self._read_int(System.RAM_USAGE)

    async def get_free_ram(self) -> int:
        """Get the free RAM.

        Returns
        -------
        int
            Free RAM in kilobyte

        """
        return await self._read_int(System.FREE_RAM)

    async def get_timezone(self) -> str:
        """Get the timezone.

        Returns
        -------
        str
            Timezone as name e.g. Europe/Vienna

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.DATE_TIME}?action=getTimeZone",
        )
        return str(response[0]["timezone"])


class BufferTankEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the buffer tank data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.buffer_tank.get_name()

    """

    async def get_name(self, position: int = 1) -> str:
        """Get the buffer tank name.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        str
            Buffer tank name

        """
        return await self._read_str(BufferTank.NAME, position)

    async def get_current_top_temperature(self, position: int = 1) -> float:
        """Get the current top temperature from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.CURRENT_TOP_TEMPERATURE, position)

    async def get_current_bottom_temperature(self, position: int = 1) -> float:
        """Get the current bottom temperature from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.CURRENT_BOTTOM_TEMPERATURE, position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON) / 2 (HEAT_UP)

        """
        return await self._read_int_or_str(BufferTank.OPERATING_MODE, position, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the buffer tank, starting at 1

        """
        await self._write_mode(BufferTank.OPERATING_MODE, mode, BufferTankOperatingMode, position)

    async def get_standby_temperature(self, position: int = 1) -> float:
        """Get the standby temperature from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.STANDBY_TEMPERATURE, position)

    async def set_standby_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the standby temperature from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The standby temperature in °C
        position
            Position of the buffer tank, starting at 1

        """
        await self._write_for_position(BufferTank.STANDBY_TEMPERATURE, temperature, position)

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get the target temperature from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.TARGET_TEMPERATURE, position)

    async def get_excess_energy_target_temperature(self, position: int = 1) -> float:
        """Get the excess energy target temperature from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.EXCESS_ENERGY_TARGET_TEMPERATURE, position)

    async def set_excess_energy_target_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target temperature from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target temperature in °C
        position
            Position of the buffer tank, starting at 1

        """
        await self._write_for_position(BufferTank.EXCESS_ENERGY_TARGET_TEMPERATURE, temperature, position)

    async def get_excess_energy_target_temperature_hysteresis(self, position: int = 1) -> float:
        """Get the excess energy target temperature hysteresis from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS, position)

    async def set_excess_energy_target_temperature_hysteresis(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target temperature hysteresis from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target temperature in °C
        position
            Position of the buffer tank, starting at 1

        """
        await self._write_for_position(BufferTank.EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS, temperature, position)

    async def get_outdoor_temperature_excess_energy_limit(self, position: int = 1) -> float:
        """Get the outdoor temperature excess energy limit from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(BufferTank.OUTDOOR_TEMPERATURE_EXCESS_ENERGY_LIMIT, position)

    async def set_outdoor_temperature_excess_energy_limit(self, temperature: float, position: int = 1) -> None:
        """Set the outdoor temperature excess energy limit from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The outdoor temperature excess energy limit temperature in °C
        position
            Position of the buffer tank, starting at 1

        """
        await self._write_for_position(BufferTank.OUTDOOR_TEMPERATURE_EXCESS_ENERGY_LIMIT, temperature, position)

    async def get_use_excess_energy(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the use excess energy state.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(BufferTank.USE_EXCESS_ENERGY, position, human_readable=human_readable)

    async def set_use_excess_energy(self, mode: int | str, position: int = 1) -> None:
        """Set the use excess energy.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the buffer tank, starting at 1

        """
        await self._write_mode(BufferTank.USE_EXCESS_ENERGY, mode, BoolEnum, position)

    async def get_excess_energy_mode(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the excess energy mode.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) HEATING / (2) COOLING

        """
        return await self._read_int_or_str(BufferTank.EXCESS_ENERGY_MODE, position, human_readable=human_readable)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(BufferTank.HEAT_REQUEST, position, human_readable=human_readable)

    async def get_cool_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the cool request state from the buffer tank.

        Parameters
        ----------
        position
            Position of the buffer tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(BufferTank.COOL_REQUEST, position, human_readable=human_readable)


class HotWaterTankEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the hot water tank data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.hot_water_tank.get_name()

    """

    async def get_name(self, position: int = 1) -> str:
        """Get the hot water tank name.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        str
            Hot water tank name

        """
        return await self._read_str(HotWaterTank.NAME, position)

    async def get_current_temperature(self, position: int = 1) -> float:
        """Get the current temperature from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.CURRENT_TEMPERATURE, position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) AUTO / (2) ON / (3) HEAT_UP

        """
        return await self._read_int_or_str(HotWaterTank.OPERATING_MODE, position, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the hot water tank, starting at 1

        """
        await self._write_mode(HotWaterTank.OPERATING_MODE, mode, HotWaterTankOperatingMode, position)

    async def get_min_target_temperature(self, position: int = 1) -> int:
        """Get the minimum target temperature from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        int
            Temperature in °C

        """
        return await self._read_int(HotWaterTank.TARGET_TEMPERATURE, position, attribute="lower_limit")

    async def get_max_target_temperature(self, position: int = 1) -> int:
        """Get the maximum target temperature from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        int
            Temperature in °C

        """
        return await self._read_int(HotWaterTank.TARGET_TEMPERATURE, position, attribute="upper_limit")

    async def get_standby_temperature(self, position: int = 1) -> float:
        """Get the standby temperature from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.STANDBY_TEMPERATURE, position)

    async def set_standby_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the standby temperature from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The standby temperature in °C
        position
            Position of the hot water tank, starting at 1

        """
        await self._write_for_position(HotWaterTank.STANDBY_TEMPERATURE, temperature, position)

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get the target temperature from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.TARGET_TEMPERATURE, position)

    async def set_target_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature in °C
        position
            Position of the hot water tank, starting at 1

        """
        await self._write_for_position(HotWaterTank.TARGET_TEMPERATURE, temperature, position)

    async def get_excess_energy_target_temperature(self, position: int = 1) -> float:
        """Get the excess energy target temperature from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.EXCESS_ENERGY_TARGET_TEMPERATURE, position)

    async def set_excess_energy_target_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target temperature from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target temperature in °C
        position
            Position of the hot water tank, starting at 1

        """
        await self._write_for_position(HotWaterTank.EXCESS_ENERGY_TARGET_TEMPERATURE, temperature, position)

    async def get_excess_energy_target_temperature_hysteresis(self, position: int = 1) -> float:
        """Get the excess energy target temperature hysteresis from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS, position)

    async def set_excess_energy_target_temperature_hysteresis(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target temperature hysteresis from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target temperature in °C
        position
            Position of the hot water tank, starting at 1

        """
        await self._write_for_position(HotWaterTank.EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS, temperature, position)

    async def get_use_excess_energy(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the use excess energy state.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(HotWaterTank.USE_EXCESS_ENERGY, position, human_readable=human_readable)

    async def set_use_excess_energy(self, mode: int | str, position: int = 1) -> None:
        """Set the use excess energy.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the hot water tank, starting at 1

        """
        await self._write_mode(HotWaterTank.USE_EXCESS_ENERGY, mode, BoolEnum, position)

    async def get_excess_energy_mode(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the excess energy mode.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) HEATING / (2) COOLING

        """
        return await self._read_int_or_str(HotWaterTank.EXCESS_ENERGY_MODE, position, human_readable=human_readable)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the hot water tank.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HotWaterTank.HEAT_REQUEST, position, human_readable=human_readable)

    async def has_fresh_water_module(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if fresh water module is available.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HotWaterTank.HAS_FRESH_WATER_MODULE, position, human_readable=human_readable)

    async def get_fresh_water_flow(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the fresh water flow from the fresh water module.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HotWaterTank.FRESH_WATER_FLOW, position, human_readable=human_readable)

    async def get_fresh_water_module_temperature(self, position: int = 1) -> float:
        """Get the fresh water module temperature.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.FRESH_WATER_MODULE_TEMPERATURE, position)

    async def get_fresh_water_module_pump_speed(self, position: int = 1) -> float:
        """Get the fresh water module pump speed.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Pump speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HotWaterTank.FRESH_WATER_MODULE_PUMP_SPEED, position)

    async def get_circulation_return_temperature(self, position: int = 1) -> float:
        """Get the circulation return temperature.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HotWaterTank.CIRCULATION_RETURN_TEMPERATURE, position)

    async def get_circulation_pump_state(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the circulation pump state.

        Parameters
        ----------
        position
            Position of the hot water tank, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HotWaterTank.CIRCULATION_PUMP_STATE, position, human_readable=human_readable)


class HeatPumpEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the heat pump data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.heat_pump.get_name()

    """

    async def get_name(self, position: int = 1) -> str:
        """Get the heat pump name.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        str
            Heat pump name

        """
        return await self._read_str(HeatPump.NAME, position)

    async def get_state(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat pump state.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) STANDBY / (1) FLOW / (2) AUTO_HEAT / (3) DEFROST / (4) AUTO_COOL / (5) INFLOW / (6) PUMP_DOWN /
            (7) SHUTDOWN / (8) ERROR

        """
        return await self._read_int_or_str(HeatPump.STATE, position, human_readable=human_readable)

    async def get_substate(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat pump substate.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) NONE / (1) OIL_PREHEATING / (2, 3) PUMP_PRE_RUN / (4) RANDOM_DELAY / (5, 21, 22) PRESSURE_EQUALIZATION /
            (6) DEFROST_PRE_FLOW / (7) DEFROST_MONITORING / (8) SNOW_DETECTION / (9) FLUSHING /
            (10) DEFROST_INITIALIZATION / (11) PREHEAT_FLOW / (12) DEFROST / (13, 25) DRIP / (14) DEFROST_END /
            (15, 16) OPEN / (17) COMPRESSOR_POST_RUN / (18) PUMP_POST_RUN / (19) LUBRICATION_PULSE /
            (20, 26) REDUCED_SPEED / (23) COMPRESSOR_DELAY / (24) DEFROST_VENTING / (27) SWITCH_HEATING_COOLING /
            (28, 33) WAIT_FOR_COMPRESSOR / (29) COMPRESSOR_STOP / (30) BIVALENT_LOCK / (31) LOCKED /
            (32) RETURN_FLOW_OFF / (34) MIXER_OPEN / (35) ZONE_VALVE / (36) ELECTRIC_DEFROST / (37) COUNTERFLOW_VALVE

        """
        return await self._read_int_or_str(HeatPump.SUBSTATE, position, human_readable=human_readable)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON / (2) BACKUP

        """
        return await self._read_int_or_str(HeatPump.OPERATING_MODE, position, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the heat pump.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the heat pump, starting at 1

        """
        await self._write_mode(HeatPump.OPERATING_MODE, mode, HeatPumpOperatingMode, position)

    async def get_compressor_use_night_speed(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the compressor use night speed state.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(HeatPump.COMPRESSOR_USE_NIGHT_SPEED, position, human_readable=human_readable)

    async def set_compressor_use_night_speed(self, mode: int | str, position: int = 1) -> None:
        """Set the compressor use night speed.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the heat pump, starting at 1

        """
        await self._write_mode(HeatPump.COMPRESSOR_USE_NIGHT_SPEED, mode, BoolEnum, position)

    async def get_compressor_night_speed(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> float:
        """Get the compressor night speed.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Has no effect, kept for backwards compatibility

        Returns
        -------
        float
            Compressor night speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatPump.COMPRESSOR_NIGHT_SPEED, position, human_readable=human_readable)

    async def set_compressor_night_speed(self, speed: float, position: int = 1) -> None:
        """Set the compressor night speed.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        speed
            Speed as a fraction from 0 to 1 (1 = 100 %), e.g. ``0.95``
        position
            Position of the heat pump, starting at 1

        """
        await self._write_for_position(HeatPump.COMPRESSOR_NIGHT_SPEED, speed, position)

    async def get_min_compressor_night_speed(self, position: int = 1) -> float:
        """Get the minimum compressor night speed.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Minimum compressor night speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatPump.COMPRESSOR_NIGHT_SPEED, position, attribute="lower_limit")

    async def get_max_compressor_night_speed(self, position: int = 1) -> float:
        """Get the maximum compressor night speed.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Maximum compressor night speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatPump.COMPRESSOR_NIGHT_SPEED, position, attribute="upper_limit")

    async def get_circulation_pump_speed(self, position: int = 1) -> float:
        """Get the circulation pump speed.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Circulation pump speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatPump.CIRCULATION_PUMP_SPEED, position)

    async def get_source_pump_speed(self, position: int = 1) -> float:
        """Get the source pump speed.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Source pump speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatPump.SOURCE_PUMP_SPEED, position)

    async def get_flow_temperature(self, position: int = 1) -> float:
        """Get the flow temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatPump.FLOW_TEMPERATURE, position)

    async def get_return_flow_temperature(self, position: int = 1) -> float:
        """Get the return flow temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatPump.RETURN_FLOW_TEMPERATURE, position)

    async def get_source_input_temperature(self, position: int = 1) -> float:
        """Get the source input temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatPump.SOURCE_INPUT_TEMPERATURE, position)

    async def get_source_output_temperature(self, position: int = 1) -> float:
        """Get the source output temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatPump.SOURCE_OUTPUT_TEMPERATURE, position)

    async def get_compressor_input_temperature(self, position: int = 1) -> float:
        """Get the compressor input temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatPump.COMPRESSOR_INPUT_TEMPERATURE, position)

    async def get_compressor_output_temperature(self, position: int = 1) -> float:
        """Get the compressor output temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE, position)

    async def get_compressor_speed(self, position: int = 1) -> float:
        """Get the compressor speed from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Compressor speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatPump.COMPRESSOR, position)

    async def get_condenser_temperature(self, position: int = 1) -> float:
        """Get the condenser temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
             Temperature in °C

        """
        return await self._read_float(HeatPump.CONDENSER_TEMPERATURE, position)

    async def get_vaporizer_temperature(self, position: int = 1) -> float:
        """Get the vaporizer temperature from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
             Temperature in °C

        """
        return await self._read_float(HeatPump.VAPORIZER_TEMPERATURE, position)

    async def get_target_overheating(self, position: int = 1) -> float:
        """Get the target overheating from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
             Temperature in °C

        """
        return await self._read_float(HeatPump.TARGET_OVERHEATING, position)

    async def get_current_overheating(self, position: int = 1) -> float:
        """Get the current overheating from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
             Temperature in °C

        """
        return await self._read_float(HeatPump.CURRENT_OVERHEATING, position)

    async def get_expansion_valve_position(self, position: int = 1) -> int:
        """Get the expansion valve position from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
             Step position

        """
        return await self._read_int(HeatPump.EXPANSION_VALVE_POSITION, position)

    async def get_high_pressure(self, position: int = 1) -> float:
        """Get the high pressure from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
             High pressure in bar

        """
        return await self._read_float(HeatPump.HIGH_PRESSURE, position)

    async def get_low_pressure(self, position: int = 1) -> float:
        """Get the low pressure from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
             Low pressure in bar

        """
        return await self._read_float(HeatPump.LOW_PRESSURE, position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HEAT_REQUEST, position, human_readable=human_readable)

    async def get_consuming_excess_energy(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the consuming excess energy from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.CONSUMING_EXCESS_ENERGY, position, human_readable=human_readable)

    async def get_excess_energy_operating_time(self, position: int = 1) -> int:
        """Get the excess energy operating time from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
            Operating time in seconds

        """
        return await self._read_int(HeatPump.EXCESS_ENERGY_OPERATING_TIME, position)

    async def get_excess_energy_max_runtime(self, position: int = 1) -> int:
        """Get the excess energy maximum runtime from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
            Excess energy maximum runtime in seconds

        """
        return await self._read_int(HeatPump.EXCESS_ENERGY_MAX_RUNTIME, position)

    async def get_excess_energy_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
            Number of excess energy activation

        """
        return await self._read_int(HeatPump.EXCESS_ENERGY_ACTIVATION_COUNTER, position)

    async def get_compressor_power(self, position: int = 1) -> float:
        """Get the compressor power from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Compressor power in W

        """
        return await self._read_float(HeatPump.COMPRESSOR_POWER, position)

    async def get_heating_power(self, position: int = 1) -> float:
        """Get the heating power from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Heating power in W

        """
        return await self._read_float(HeatPump.HEATING_POWER, position)

    async def get_hot_water_power(self, position: int = 1) -> float:
        """Get the hot water power from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Hot water power in W

        """
        return await self._read_float(HeatPump.HOT_WATER_POWER, position)

    async def get_cop(self, position: int = 1) -> float:
        """Get the COP from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            COP

        """
        return await self._read_float(HeatPump.COP, position)

    async def get_heating_energy(self, position: int = 1) -> float:
        """Get the heating energy from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Heating energy in J

        """
        return await self._read_float(HeatPump.HEATING_ENERGY, position)

    async def get_heating_energy_consumption(self, position: int = 1) -> float:
        """Get the energy consumption for heating from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Energy consumption for heating in kWh

        """
        return await self._read_float(HeatPump.HEATING_ENERGY_CONSUMPTION, position)

    async def get_heating_spf(self, position: int = 1) -> float:
        """Get the heating SPF from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Heating SPF

        """
        return await self._read_float(HeatPump.HEATING_SPF, position)

    async def get_cooling_energy(self, position: int = 1) -> float:
        """Get the cooling energy from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Cooling energy in J

        """
        return await self._read_float(HeatPump.COOLING_ENERGY, position)

    async def get_cooling_energy_consumption(self, position: int = 1) -> float:
        """Get the cooling energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Cooling energy consumption in kWh

        """
        return await self._read_float(HeatPump.COOLING_ENERGY_CONSUMPTION, position)

    async def get_cooling_spf(self, position: int = 1) -> float:
        """Get the cooling SPF from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Cooling SPF

        """
        return await self._read_float(HeatPump.COOLING_SPF, position)

    async def get_hot_water_energy(self, position: int = 1) -> float:
        """Get the hot water energy from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Hot water energy in J

        """
        return await self._read_float(HeatPump.HOT_WATER_ENERGY, position)

    async def get_hot_water_energy_consumption(self, position: int = 1) -> float:
        """Get the hot water energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Hot water energy consumption in kWh

        """
        return await self._read_float(HeatPump.HOT_WATER_ENERGY_CONSUMPTION, position)

    async def get_hot_water_spf(self, position: int = 1) -> float:
        """Get the hot water SPF from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Hot water SPF

        """
        return await self._read_float(HeatPump.HOT_WATER_SPF, position)

    async def get_total_thermal_energy(self, position: int = 1) -> float:
        """Get the total thermal energy from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Total thermal energy in J

        """
        return await self._read_float(HeatPump.TOTAL_THERMAL_ENERGY, position)

    async def get_total_energy_consumption(self, position: int = 1) -> float:
        """Get the total energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Total energy consumption in kWh

        """
        return await self._read_float(HeatPump.TOTAL_ENERGY_CONSUMPTION, position)

    async def get_excess_energy_consumption(self, position: int = 1) -> float:
        """Get the excess energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Excess energy consumption in kWh

        """
        return await self._read_float(HeatPump.EXCESS_ENERGY_CONSUMPTION, position)

    async def get_heating_excess_energy_consumption(self, position: int = 1) -> float:
        """Get the heating excess energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Heating excess energy consumption in kWh

        """
        return await self._read_float(HeatPump.HEATING_EXCESS_ENERGY_CONSUMPTION, position)

    async def get_cooling_excess_energy_consumption(self, position: int = 1) -> float:
        """Get the cooling excess energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Cooling excess energy consumption in kWh

        """
        return await self._read_float(HeatPump.COOLING_EXCESS_ENERGY_CONSUMPTION, position)

    async def get_hot_water_excess_energy_consumption(self, position: int = 1) -> float:
        """Get the hot water excess energy consumption from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            Hot water excess energy consumption in kWh

        """
        return await self._read_float(HeatPump.HOT_WATER_EXCESS_ENERGY_CONSUMPTION, position)

    async def get_total_spf(self, position: int = 1) -> float:
        """Get the SPF from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        float
            SPF

        """
        return await self._read_float(HeatPump.TOTAL_SPF, position)

    async def has_active_cooling(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if active cooling for the heat pump is available.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HAS_ACTIVE_COOLING, position, human_readable=human_readable)

    async def has_passive_cooling(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if passive cooling for the heat pump is available.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HAS_PASSIVE_COOLING, position, human_readable=human_readable)

    async def get_operating_time(self, position: int = 1) -> int:
        """Get the operating time from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
            Operating time in seconds

        """
        return await self._read_int(HeatPump.OPERATING_TIME, position)

    async def get_max_runtime(self, position: int = 1) -> int:
        """Get the maximum runtime from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
            Maximum runtime in seconds

        """
        return await self._read_int(HeatPump.MAX_RUNTIME, position)

    async def get_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter from the heat pump.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1

        Returns
        -------
        int
            Number of heat pump activations

        """
        return await self._read_int(HeatPump.ACTIVATION_COUNTER, position)

    async def has_compressor_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a compressor failure.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HAS_COMPRESSOR_FAILURE, position, human_readable=human_readable)

    async def has_source_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source failure.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HAS_SOURCE_FAILURE, position, human_readable=human_readable)

    async def has_source_actuator_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source actuator failure.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(
            HeatPump.HAS_SOURCE_ACTUATOR_FAILURE, position, human_readable=human_readable
        )

    async def has_three_phase_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a three-phase failure.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HAS_THREE_PHASE_FAILURE, position, human_readable=human_readable)

    async def has_source_pressure_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source pressure failure.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(
            HeatPump.HAS_SOURCE_PRESSURE_FAILURE, position, human_readable=human_readable
        )

    async def has_vfd_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source pressure variable frequency drive (VFD) failure.

        Parameters
        ----------
        position
            Position of the heat pump, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatPump.HAS_VFD_FAILURE, position, human_readable=human_readable)


class HeatCircuitEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the heat circuit data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.heat_circuit.get_name()

    """

    async def get_name(self, position: int = 1) -> str:
        """Get the heat circuit name.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        str
            Heat circuit name

        """
        return await self._read_str(HeatCircuit.NAME, position)

    async def get_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the mode from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (HEATING) / 1 (COOLING) / 2 (HEATING_AND_COOLING) / 3 (HEATING_AND_ACTIVE_COOLING)

        """
        return await self._read_int_or_str(HeatCircuit.MODE, position, human_readable=human_readable)

    async def has_room_temperature(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if room temperature from the heat circuit is available.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.HAS_ROOM_TEMPERATURE, position, human_readable=human_readable)

    async def get_room_temperature(self, position: int = 1) -> float:
        """Get the room temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.ROOM_TEMPERATURE, position)

    async def has_room_humidity(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if room humidity from the heat circuit is available.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.HAS_ROOM_HUMIDITY, position, human_readable=human_readable)

    async def get_room_humidity(self, position: int = 1) -> float:
        """Get the room humidity from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Humidity in percent

        """
        return await self._read_float(HeatCircuit.ROOM_HUMIDITY, position)

    async def get_dew_point(self, position: int = 1) -> float:
        """Get the dew point from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.DEW_POINT, position)

    async def get_flow_temperature_setpoint(self, position: int = 1) -> float:
        """Get the flow temperature setpoint from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.FLOW_TEMPERATURE_SETPOINT, position)

    async def has_mixer(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if heating circuit mixer is available.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.HAS_MIXER, position, human_readable=human_readable)

    async def get_mixer_flow_temperature(self, position: int = 1) -> float:
        """Get the mixer flow temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.MIXER_FLOW_TEMPERATURE, position)

    async def get_mixer_return_flow_temperature(self, position: int = 1) -> float:
        """Get the mixer return flow temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.MIXER_RETURN_FLOW_TEMPERATURE, position)

    async def get_mixer_position(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the mixer position.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            -1 (CLOSED) / 0 (OFF) / 1 (OPEN)

        """
        return await self._read_int_or_str(HeatCircuit.MIXER_POSITION, position, human_readable=human_readable)

    async def get_pump_state(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the pump state.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.PUMP_STATE, position, human_readable=human_readable)

    async def has_return_flow_temperature(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the return flow temperature sensor is available.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(
            HeatCircuit.HAS_RETURN_FLOW_TEMPERATURE, position, human_readable=human_readable
        )

    async def get_return_flow_temperature(self, position: int = 1) -> float:
        """Get the return flow temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.RETURN_FLOW_TEMPERATURE, position)

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get the target temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_TEMPERATURE, position)

    async def get_use_excess_energy(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the use excess energy state.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(HeatCircuit.USE_EXCESS_ENERGY, position, human_readable=human_readable)

    async def set_use_excess_energy(self, mode: int | str, position: int = 1) -> None:
        """Set the use excess energy.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_mode(HeatCircuit.USE_EXCESS_ENERGY, mode, BoolEnum, position)

    async def get_excess_energy_mode(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the excess energy mode.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) HEATING / (2) COOLING

        """
        return await self._read_int_or_str(HeatCircuit.EXCESS_ENERGY_MODE, position, human_readable=human_readable)

    async def get_excess_energy_target_temperature(self, position: int = 1) -> float:
        """Get the excess energy target temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_TARGET_TEMPERATURE, position)

    async def set_excess_energy_target_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target temperature from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_TARGET_TEMPERATURE, temperature, position)

    async def get_excess_energy_target_temperature_hysteresis(self, position: int = 1) -> float:
        """Get the excess energy target temperature hysteresis from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS, position)

    async def set_excess_energy_target_temperature_hysteresis(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target temperature hysteresis from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target temperature in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_TARGET_TEMPERATURE_HYSTERESIS, temperature, position)

    async def get_excess_energy_target_cooling_temperature(self, position: int = 1) -> float:
        """Get the excess energy target cooling temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE, position)

    async def set_excess_energy_target_cooling_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy target cooling temperature from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target cooling temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE, temperature, position)

    async def get_excess_energy_target_cooling_temperature_hysteresis(self, position: int = 1) -> float:
        """Get the excess energy target cooling temperature hysteresis from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE_HYSTERESIS, position)

    async def set_excess_energy_target_cooling_temperature_hysteresis(
        self, temperature: float, position: int = 1
    ) -> None:
        """Set the excess energy target cooling temperature hysteresis from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy target cooling temperature in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(
            HeatCircuit.EXCESS_ENERGY_TARGET_COOLING_TEMPERATURE_HYSTERESIS, temperature, position
        )

    async def get_selected_target_temperature(self, position: int = 1) -> float:
        """Get the selected target temperature from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.SELECTED_TARGET_TEMPERATURE, position)

    async def get_target_temperature_day(self, position: int = 1) -> float:
        """Get the target temperature for the day from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_TEMPERATURE_DAY, position)

    async def set_target_temperature_day(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.TARGET_TEMPERATURE_DAY, temperature, position)

    async def get_target_cooling_temperature_day(self, position: int = 1) -> float:
        """Get the target cooling temperature for the day from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_COOLING_TEMPERATURE_DAY, position)

    async def set_target_cooling_temperature_day(self, temperature: float, position: int = 1) -> None:
        """Set the target cooling temperature for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target cooling temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.TARGET_COOLING_TEMPERATURE_DAY, temperature, position)

    async def get_heating_limit_day(self, position: int = 1) -> float:
        """Get the heating limit for the day from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.HEATING_LIMIT_DAY, position)

    async def set_heating_limit_day(self, temperature: float, position: int = 1) -> None:
        """Set the heating limit for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The heating limit temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.HEATING_LIMIT_DAY, temperature, position)

    async def get_cooling_limit_day(self, position: int = 1) -> float:
        """Get the cooling limit for the day from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.COOLING_LIMIT_DAY, position)

    async def set_cooling_limit_day(self, temperature: float, position: int = 1) -> None:
        """Set the cooling limit for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The cooling limit temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.COOLING_LIMIT_DAY, temperature, position)

    async def get_excess_energy_heating_limit_day(self, position: int = 1) -> float:
        """Get the excess energy heating limit for the day from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_HEATING_LIMIT_DAY, position)

    async def set_excess_energy_heating_limit_day(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy heating limit for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy heating limit temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_HEATING_LIMIT_DAY, temperature, position)

    async def get_excess_energy_cooling_limit_day(self, position: int = 1) -> float:
        """Get the excess energy cooling limit for the day from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_COOLING_LIMIT_DAY, position)

    async def set_excess_energy_cooling_limit_day(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy cooling limit for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy cooling limit temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_COOLING_LIMIT_DAY, temperature, position)

    async def get_target_temperature_night(self, position: int = 1) -> float:
        """Get the target temperature for the night from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_TEMPERATURE_NIGHT, position)

    async def set_target_temperature_night(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.TARGET_TEMPERATURE_NIGHT, temperature, position)

    async def get_target_cooling_temperature_night(self, position: int = 1) -> float:
        """Get the target cooling temperature for the night from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_COOLING_TEMPERATURE_NIGHT, position)

    async def set_target_cooling_temperature_night(self, temperature: float, position: int = 1) -> None:
        """Set the target cooling temperature for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target cooling temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.TARGET_COOLING_TEMPERATURE_NIGHT, temperature, position)

    async def get_heating_limit_night(self, position: int = 1) -> float:
        """Get the heating limit for the night from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.HEATING_LIMIT_NIGHT, position)

    async def set_heating_limit_night(self, temperature: float, position: int = 1) -> None:
        """Set the heating limit for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The heating limit temperature for the night in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.HEATING_LIMIT_NIGHT, temperature, position)

    async def get_cooling_limit_night(self, position: int = 1) -> float:
        """Get the cooling limit for the night from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.COOLING_LIMIT_NIGHT, position)

    async def set_cooling_limit_night(self, temperature: float, position: int = 1) -> None:
        """Set the cooling limit for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The cooling limit temperature for the night in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.COOLING_LIMIT_NIGHT, temperature, position)

    async def get_excess_energy_heating_limit_night(self, position: int = 1) -> float:
        """Get the excess energy heating limit for the night from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_HEATING_LIMIT_NIGHT, position)

    async def set_excess_energy_heating_limit_night(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy heating limit for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy heating limit temperature for the night in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_HEATING_LIMIT_NIGHT, temperature, position)

    async def get_excess_energy_cooling_limit_night(self, position: int = 1) -> float:
        """Get the excess energy cooling limit for the night from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.EXCESS_ENERGY_COOLING_LIMIT_NIGHT, position)

    async def set_excess_energy_cooling_limit_night(self, temperature: float, position: int = 1) -> None:
        """Set the excess energy cooling limit for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The excess energy cooling limit temperature for the night in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.EXCESS_ENERGY_COOLING_LIMIT_NIGHT, temperature, position)

    async def get_target_temperature_away(self, position: int = 1) -> float:
        """Get the target temperature when away for the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_TEMPERATURE_AWAY, position)

    async def set_target_temperature_away(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature when away for the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature for the day in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.TARGET_TEMPERATURE_AWAY, temperature, position)

    async def get_target_temperature_offset(self, position: int = 1) -> float:
        """Get the target temperature offset from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(HeatCircuit.TARGET_TEMPERATURE_OFFSET, position)

    async def set_target_temperature_offset(self, offset: float, position: int = 1) -> None:
        """Set the target temperature offset for the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        offset
            The target temperature offset
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.TARGET_TEMPERATURE_OFFSET, offset, position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (AUTO) / (2) DAY / (3) NIGHT / (4) HOLIDAY / (5) PARTY / (8) EXTERNAL / (9) ROOM_CONTROL

        """
        return await self._read_int_or_str(HeatCircuit.OPERATING_MODE, position, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_mode(HeatCircuit.OPERATING_MODE, mode, HeatCircuitOperatingMode, position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.HEAT_REQUEST, position, human_readable=human_readable)

    async def get_cool_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the cool request state from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.COOL_REQUEST, position, human_readable=human_readable)

    async def get_away_start_date(self, position: int = 1) -> int:
        """Get the away start date from the heating circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        int
            Start date as unix timestamp

        """
        return await self._read_int(HeatCircuit.AWAY_START_DATE, position)

    async def set_away_start_date(self, timestamp: int, position: int = 1) -> None:
        """Set the away start date from the heating circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        timestamp
            Start date as unix timestamp
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.AWAY_START_DATE, timestamp, position)

    async def get_away_end_date(self, position: int = 1) -> int:
        """Get the away end date from the heating circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        int
            End date as unix timestamp

        """
        return await self._read_int(HeatCircuit.AWAY_END_DATE, position)

    async def set_away_end_date(self, timestamp: int, position: int = 1) -> None:
        """Set the away end date from the heating circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        timestamp
            End date as unix timestamp
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.AWAY_END_DATE, timestamp, position)

    async def get_heating_curve_offset(self, position: int = 1) -> float:
        """Get the heating curve offset from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Offset in °C

        """
        return await self._read_float(HeatCircuit.HEATING_CURVE_OFFSET, position)

    async def set_heating_curve_offset(self, offset: float, position: int = 1) -> None:
        """Set the heating curve offset from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        offset
            The offset in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.HEATING_CURVE_OFFSET, offset, position)

    async def get_cooling_curve_offset(self, position: int = 1) -> float:
        """Get the cooling curve offset from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Offset in °C

        """
        return await self._read_float(HeatCircuit.COOLING_CURVE_OFFSET, position)

    async def set_cooling_curve_offset(self, offset: float, position: int = 1) -> None:
        """Set the cooling curve offset from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        offset
            The offset in °C
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.COOLING_CURVE_OFFSET, offset, position)

    async def get_heating_curve_slope(self, position: int = 1) -> float:
        """Get the heating curve slope from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Slope

        """
        return await self._read_float(HeatCircuit.HEATING_CURVE_SLOPE, position)

    async def set_heating_curve_slope(self, slope: float, position: int = 1) -> None:
        """Set the heating curve slope from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        slope
            The slope
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.HEATING_CURVE_SLOPE, slope, position)

    async def get_cooling_curve_slope(self, position: int = 1) -> float:
        """Get the cooling curve slope from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Slope

        """
        return await self._read_float(HeatCircuit.COOLING_CURVE_SLOPE, position)

    async def set_cooling_curve_slope(self, slope: float, position: int = 1) -> None:
        """Set the cooling curve slope from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        slope
            The slope
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_for_position(HeatCircuit.COOLING_CURVE_SLOPE, slope, position)

    async def get_use_heating_curve(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the use heating curve from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(HeatCircuit.USE_HEATING_CURVE, position, human_readable=human_readable)

    async def set_use_heating_curve(self, mode: int | str, position: int = 1) -> None:
        """Set the use heating curve.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the heating circuit, starting at 1

        """
        await self._write_mode(HeatCircuit.USE_HEATING_CURVE, mode, BoolEnum, position)

    async def get_heating_curve(self, position: int = 1) -> str:
        """Get the heating curve from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        str
            Name of the heating curve, e.g. HC1

        """
        return await self._read_str(HeatCircuit.HEATING_CURVE, position)

    async def set_heating_curve(self, heating_curve: str, position: int = 1) -> None:
        """Set the heating curve from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        heating_curve
            The heating curve name, e.g. HC1
        position
            Position of the heating circuit, starting at 1

        """
        curve_names: list[str] = [name for _, name in await self.get_available_heating_curves()]

        if heating_curve not in curve_names:
            message: str = f"Invalid value! Allowed values are {curve_names}"
            raise APIError(message)

        await self._write_for_position(HeatCircuit.HEATING_CURVE, heating_curve, position)

    async def get_cooling_curve(self, position: int = 1) -> str:
        """Get the cooling curve from the heat circuit.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        str
            Name of the cooling curve, e.g. HC1

        """
        return await self._read_str(HeatCircuit.COOLING_CURVE, position)

    async def set_cooling_curve(self, cooling_curve: str, position: int = 1) -> None:
        """Set the cooling curve from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        cooling_curve
            The cooling curve name, e.g. HC2
        position
            Position of the heating circuit, starting at 1

        """
        curve_names: list[str] = [name for _, name in await self.get_available_heating_curves()]

        if cooling_curve not in curve_names:
            message: str = f"Invalid value! Allowed values are {curve_names}"
            raise APIError(message)

        await self._write_for_position(HeatCircuit.COOLING_CURVE, cooling_curve, position)

    async def get_heating_curve_points(self, heating_curve: str | None = None) -> HeatingCurves:
        """Get the heating curve points.

        Parameters
        ----------
        heating_curve
            The heating curve name

        Returns
        -------
        HeatingCurves
            One or more heating curves and the points

        """
        heating_curves: tuple[tuple[int, str], ...] = await self.get_available_heating_curves()

        if heating_curve is None:
            return await self._read_heating_curve_points(heating_curves)

        # Only the requested heating curve is read.
        data: HeatingCurves = await self._read_heating_curve_points(
            tuple(curve for curve in heating_curves if curve[1] == heating_curve),
        )

        try:
            return {heating_curve: data[heating_curve]}
        except KeyError as error:
            message: str = f'Heating curve "{heating_curve}" not found'
            raise APIError(message) from error

    async def set_heating_curve_points(self, heating_curve: str, points: HeatingCurvePoints) -> None:
        """Set the heating curve points.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        heating_curve
            The heating curve name
        points
            Heating curve points

        Raises
        ------
        APIError
            The heating curve is invalid.

        """
        message: str

        heating_curves = await self.get_available_heating_curves()

        curve_map: dict[str, int] = {name: idx for idx, name in heating_curves}

        try:
            idx = curve_map[heating_curve]
        except KeyError as error:
            message = f"Invalid value! Allowed values are {[name for _, name in heating_curves]}"
            raise APIError(message) from error
        else:
            read_payload: Payload = [
                ReadPayload(
                    name=LineTablePool.HEATING_CURVE_NAME.value.value % idx,
                    attr="0",
                ),
            ]

            read_response: Response = await self._post(
                payload=json.dumps(read_payload),
                endpoint=EndpointPath.READ_WRITE_VARS,
            )

            if read_response[0]["value"] != heating_curve:
                message = f'Name of heating curve "{heating_curve}" does not match entry with index {idx}'
                raise APIError(message)

            write_payload: Payload = [
                WritePayload(
                    name=LineTablePool.HEATING_CURVE_POINTS.value.value % idx,
                    value=str(len(points) or MIN_HEATING_CURVE_POINTS),
                ),
            ]

            for point_idx in range(MAX_HEATING_CURVE_POINTS):
                point: HeatingCurvePoint | None = None

                if point_idx < len(points):
                    point = points[point_idx]

                write_payload += [
                    WritePayload(
                        name=LineTablePool.HEATING_CURVE_POINT_X.value.value % (idx, point_idx),
                        value=str(point.outdoor) if point else "0",
                    ),
                    WritePayload(
                        name=LineTablePool.HEATING_CURVE_POINT_Y.value.value % (idx, point_idx),
                        value=str(point.flow) if point else "0",
                    ),
                ]

            write_payload += [
                WritePayload(
                    name=LineTablePool.SAVE_HEATING_CURVE.value.value % idx,
                    value="192",
                ),
            ]

            await self._post(
                payload=json.dumps(write_payload),
                endpoint=f"{EndpointPath.READ_WRITE_VARS}?action=set",
            )

    async def get_available_heating_curves(self) -> tuple[tuple[int, str], ...]:
        """Get available heating curves.

        Returns
        -------
        tuple[tuple[int, str], ...]
            Index and heating curve name pairs

        """
        payload: Payload = [
            ReadPayload(name=LineTablePool.HEATING_CURVE_NAME.value.value % idx, attr="0")
            for idx in range(_HEATING_CURVE_POOL_SIZE)
        ]

        response: Response = await self._post(
            payload=json.dumps(payload),
            endpoint=EndpointPath.READ_WRITE_VARS,
        )

        return tuple((idx, item["value"]) for idx, item in enumerate(response) if item["value"].startswith("HC"))

    async def has_pump(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heating circuit pump is available.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.HAS_PUMP, position, human_readable=human_readable)

    async def has_var_speed_pump(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heating circuit pump has a variable speed.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(HeatCircuit.HAS_VAR_SPEED_PUMP, position, human_readable=human_readable)

    async def get_pump_speed(self, position: int = 1) -> float:
        """Get pump speed.

        Parameters
        ----------
        position
            Position of the heating circuit, starting at 1

        Returns
        -------
        float
            Pump speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(HeatCircuit.PUMP_SPEED, position)


class SolarCircuitEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the solar circuit data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.solar_circuit.get_name()

    """

    async def get_name(self, position: int = 1) -> str:
        """Get the solar circuit name.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        str
            Solar circuit name

        """
        return await self._read_str(SolarCircuit.NAME, position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(SolarCircuit.OPERATING_MODE, position, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the solar circuit, starting at 1

        """
        await self._write_mode(SolarCircuit.OPERATING_MODE, mode, BoolEnum, position)

    async def get_priority_1_before_2(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get priority 1 before 2 for the pumps from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(SolarCircuit.PRIORITY_1_BEFORE_2, position, human_readable=human_readable)

    async def set_priority_1_before_2(self, mode: int | str, position: int = 1) -> None:
        """Set the priority 1 before 2 for the pumps from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the solar circuit, starting at 1

        """
        await self._write_mode(SolarCircuit.PRIORITY_1_BEFORE_2, mode, BoolEnum, position)

    async def get_source_temperature(self, position: int = 1) -> float:
        """Get source temperature from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(SolarCircuit.SOURCE_TEMPERATURE, position)

    async def get_pump_1_speed(self, position: int = 1) -> float:
        """Get pump 1 speed.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Pump 1 speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(SolarCircuit.PUMP_1, position)

    async def get_pump_2_speed(self, position: int = 1) -> float:
        """Get pump 2 speed.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Pump 2 speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(SolarCircuit.PUMP_2, position)

    async def get_current_temperature_1(self, position: int = 1) -> float:
        """Get current temperature 1 from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(SolarCircuit.CURRENT_TEMPERATURE, position, index=0)

    async def get_current_temperature_2(self, position: int = 1) -> float:
        """Get current temperature 2 from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(SolarCircuit.CURRENT_TEMPERATURE, position, index=1)

    async def get_target_temperature_1(self, position: int = 1) -> float:
        """Get target temperature 1 from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(SolarCircuit.TARGET_TEMPERATURE, position, index=0)

    async def set_target_temperature_1(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature 1 from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature in °C
        position
            Position of the solar circuit, starting at 1

        """
        # Two consumers per solar circuit: consumer 1 is genericHeat[2 * (position - 1)].
        quantity: int = SolarCircuit.TARGET_TEMPERATURE.value.quantity
        await self._write_for_position(SolarCircuit.TARGET_TEMPERATURE, temperature, quantity * position - 1)

    async def get_target_temperature_2(self, position: int = 1) -> float:
        """Get target temperature 2 from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(SolarCircuit.TARGET_TEMPERATURE, position, index=1)

    async def set_target_temperature_2(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature 2 from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature in °C
        position
            Position of the solar circuit, starting at 1

        """
        # Two consumers per solar circuit: consumer 2 is genericHeat[2 * (position - 1) + 1].
        quantity: int = SolarCircuit.TARGET_TEMPERATURE.value.quantity
        await self._write_for_position(SolarCircuit.TARGET_TEMPERATURE, temperature, quantity * position)

    async def get_heat_request_1(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request 1 state from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(SolarCircuit.HEAT_REQUEST, position, human_readable=human_readable, index=0)

    async def get_heat_request_2(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request 2 state from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(SolarCircuit.HEAT_REQUEST, position, human_readable=human_readable, index=1)

    async def get_heating_energy(self, position: int = 1) -> float:
        """Get heating energy from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Heating energy in J

        """
        return await self._read_float(SolarCircuit.HEATING_ENERGY, position)

    async def get_daily_energy(self, position: int = 1) -> float:
        """Get daily energy from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Daily energy in J

        """
        return await self._read_float(SolarCircuit.DAILY_ENERGY, position)

    async def get_actual_power(self, position: int = 1) -> float:
        """Get actual power from the solar circuit.

        Parameters
        ----------
        position
            Position of the solar circuit, starting at 1

        Returns
        -------
        float
            Actual power in W

        """
        return await self._read_float(SolarCircuit.ACTUAL_POWER, position)


class ExternalHeatSourceEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the external heat source data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.external_heat_source.get_operating_mode()

    """

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(ExternalHeatSource.OPERATING_MODE, position, human_readable=human_readable)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the external heat source.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the external heat source, starting at 1

        """
        await self._write_mode(ExternalHeatSource.OPERATING_MODE, mode, BoolEnum, position)

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get target temperature from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(ExternalHeatSource.TARGET_TEMPERATURE, position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(ExternalHeatSource.HEAT_REQUEST, position, human_readable=human_readable)

    async def get_operating_time(self, position: int = 1) -> int:
        """Get the operating time from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Operating time in seconds

        """
        return await self._read_int(ExternalHeatSource.OPERATING_TIME, position)

    async def get_max_runtime(self, position: int = 1) -> int:
        """Get the maximum runtime from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Maximum runtime in seconds

        """
        return await self._read_int(ExternalHeatSource.MAX_RUNTIME, position)

    async def get_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Number of external heat source activation

        """
        return await self._read_int(ExternalHeatSource.ACTIVATION_COUNTER, position)

    async def get_consuming_excess_energy(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the consuming excess energy from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            0 (OFF) / 1 (ON)

        """
        return await self._read_int_or_str(
            ExternalHeatSource.CONSUMING_EXCESS_ENERGY, position, human_readable=human_readable
        )

    async def get_excess_energy_operating_time(self, position: int = 1) -> int:
        """Get the excess energy operating time from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Excess energy operating time in seconds

        """
        return await self._read_int(ExternalHeatSource.EXCESS_ENERGY_OPERATING_TIME, position)

    async def get_excess_energy_max_runtime(self, position: int = 1) -> int:
        """Get the excess energy maximum runtime from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Excess energy maximum runtime in seconds

        """
        return await self._read_int(ExternalHeatSource.EXCESS_ENERGY_MAX_RUNTIME, position)

    async def get_excess_energy_activation_counter(self, position: int = 1) -> int:
        """Get the excess energy activation counter from the external heat source.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Number of excess energy external heat source activation

        """
        return await self._read_int(ExternalHeatSource.EXCESS_ENERGY_ACTIVATION_COUNTER, position)

    async def get_use_excess_energy(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the use excess energy state.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(
            ExternalHeatSource.USE_EXCESS_ENERGY, position, human_readable=human_readable
        )

    async def set_use_excess_energy(self, mode: int | str, position: int = 1) -> None:
        """Set the use excess energy.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            Position of the external heat source, starting at 1

        """
        await self._write_mode(ExternalHeatSource.USE_EXCESS_ENERGY, mode, BoolEnum, position)

    async def get_min_runtime_excess_energy(self, position: int = 1) -> int:
        """Get the minimum runtime excess energy.

        Parameters
        ----------
        position
            Position of the external heat source, starting at 1

        Returns
        -------
        int
            Runtime in minutes

        """
        return await self._read_int(ExternalHeatSource.MIN_RUNTIME_EXCESS_ENERGY, position)

    async def set_min_runtime_excess_energy(self, minute: int, position: int = 1) -> None:
        """Set the minimum runtime excess energy.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        minute
            The minimum runtime in minutes
        position
            Position of the external heat source, starting at 1

        """
        await self._write_for_position(ExternalHeatSource.MIN_RUNTIME_EXCESS_ENERGY, minute, position)


class SwitchValveEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the switch valve data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.switch_valve.get_position()

    """

    async def get_position(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get switch valve position.

        Parameters
        ----------
        position
            Position of the switch valve, starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) NEUTRAL / (1) OPEN / (2) CLOSED

        """
        return await self._read_int_or_str(SwitchValve.POSITION, position, human_readable=human_readable)


class PassiveCoolingEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the passive cooling data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.passive_cooling.get_temperature()

    """

    async def get_temperature(self, position: int = 1) -> float:
        """Get the temperature from passive cooling.

        Parameters
        ----------
        position
            Position of the passive cooling unit (one per heat pump), starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(PassiveCooling.TEMPERATURE, position)

    async def get_switch_valve_position(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get switch valve position from passive cooling.

        Parameters
        ----------
        position
            Position of the passive cooling unit (one per heat pump), starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) NEUTRAL / (1) OPEN / (2) CLOSED

        """
        return await self._read_int_or_str(
            PassiveCooling.SWITCH_VALVE_POSITION, position, human_readable=human_readable
        )

    async def get_circulation_pump_speed(self, position: int = 1) -> float:
        """Get the circulation pump speed from passive cooling.

        Parameters
        ----------
        position
            Position of the passive cooling unit (one per heat pump), starting at 1

        Returns
        -------
        float
            Circulation pump speed as a fraction from 0 to 1 (1 = 100 %)

        """
        return await self._read_float(PassiveCooling.CIRCULATION_PUMP_SPEED, position)

    async def get_mixer_target_temperature(self, position: int = 1) -> float:
        """Get the mixer target temperature from passive cooling.

        Parameters
        ----------
        position
            Position of the passive cooling unit (one per heat pump), starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(PassiveCooling.MIXER_TARGET_TEMPERATURE, position)

    async def get_mixer_flow_temperature(self, position: int = 1) -> float:
        """Get the mixer flow temperature from passive cooling.

        Parameters
        ----------
        position
            Position of the passive cooling unit (one per heat pump), starting at 1

        Returns
        -------
        float
            Temperature in °C

        """
        return await self._read_float(PassiveCooling.MIXER_FLOW_TEMPERATURE, position)

    async def get_mixer_position(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the mixer position.

        Parameters
        ----------
        position
            Position of the passive cooling unit (one per heat pump), starting at 1
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            -1 (CLOSED) / 0 (OFF) / 1 (OPEN)

        """
        return await self._read_int_or_str(PassiveCooling.MIXER_POSITION, position, human_readable=human_readable)


class PhotovoltaicsEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the photovoltaics data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    ...     host="ap4400.local",
    ...     username="test",
    ...     password="test",
    ...     ssl=True,
    ...     skip_ssl_verification=True
    ... )
    >>> await client.photovoltaics.get_excess_power()

    """

    async def get_excess_energy_active(
        self,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get the excess energy active.

        Parameters
        ----------
        human_readable
            Return a human-readable string

        Returns
        -------
        int | str
            (0) OFF / (1) ON

        """
        return await self._read_int_or_str(Photovoltaics.EXCESS_ENERGY_ACTIVE, human_readable=human_readable)

    async def get_excess_power(self) -> float:
        """Get excess power.

        Returns
        -------
        float
            Excess power in W

        """
        return await self._read_float(Photovoltaics.EXCESS_POWER)

    async def get_daily_energy(self) -> float:
        """Get daily energy.

        Returns
        -------
        float
            Daily energy in J

        """
        return await self._read_float(Photovoltaics.DAILY_ENERGY)

    async def get_total_energy(self) -> float:
        """Get total energy.

        Returns
        -------
        float
            Total energy in J

        """
        return await self._read_float(Photovoltaics.TOTAL_ENERGY)
