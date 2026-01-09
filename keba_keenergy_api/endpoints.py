"""Retrieve hot water tank data."""

import json
import re
from enum import Enum
from http import HTTPStatus
from re import Pattern
from typing import Any
from typing import NamedTuple
from typing import TypeAlias
from typing import TypedDict
from typing import cast

from aiohttp import BasicAuth
from aiohttp import ClientError
from aiohttp import ClientSession
from aiohttp import ClientTimeout

from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.constants import BufferTank
from keba_keenergy_api.constants import BufferTankOperatingMode
from keba_keenergy_api.constants import EndpointPath
from keba_keenergy_api.constants import ExternalHeatSource
from keba_keenergy_api.constants import ExternalHeatSourceOperatingMode
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HeatPumpCompressorUseNightSpeed
from keba_keenergy_api.constants import HeatPumpOperatingMode
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.constants import Photovoltaic
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import SolarCircuitOperatingMode
from keba_keenergy_api.constants import System
from keba_keenergy_api.constants import SystemOperatingMode
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import AuthenticationError


class ReadPayload(TypedDict):
    name: str
    attr: str


class WritePayload(TypedDict):
    name: str
    value: str


class Position(NamedTuple):
    heat_pump: int
    heat_circuit: int
    solar_circuit: int
    buffer_tank: int
    hot_water_tank: int
    external_heat_source: int


class Value(TypedDict, total=False):
    value: Any
    attributes: dict[str, Any]


ValueResponse: TypeAlias = dict[str, list[list[Value]] | list[Value] | Value]
Payload: TypeAlias = list[ReadPayload | WritePayload]
Response: TypeAlias = list[dict[str, Any]]


class BaseEndpoints:
    """Base class for all endpoint classes."""

    KEY_PATTERN: Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        self._base_url: str = base_url
        self._auth: BasicAuth | None = auth
        self._ssl: bool = ssl
        self._skip_ssl_verification: bool = skip_ssl_verification
        self._session: ClientSession | None = session

    async def _post(self, payload: str | None = None, endpoint: str | None = None) -> Response:
        """Run a POST request against the API."""
        session: ClientSession = (
            self._session
            if self._session and not self._session.closed
            else ClientSession(timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT))
        )

        try:
            url: str = f"{self._base_url}{endpoint if endpoint else ''}"

            async with session.post(
                url,
                auth=self._auth,
                ssl=False if self._skip_ssl_verification else self._ssl,
                data=payload,
            ) as resp:
                if resp.status <= HTTPStatus.MULTIPLE_CHOICES or resp.status == HTTPStatus.INTERNAL_SERVER_ERROR:
                    response: list[dict[str, Any]] = await resp.json()

                    if (
                        resp.status == HTTPStatus.INTERNAL_SERVER_ERROR
                        and isinstance(response, dict)
                        and "developerMessage" in response
                    ):
                        developer_message: str = response["developerMessage"]
                        raise APIError(developer_message, status=HTTPStatus(resp.status))
                if resp.status == HTTPStatus.UNAUTHORIZED:
                    raise AuthenticationError(status=HTTPStatus.UNAUTHORIZED)
                if resp.status >= HTTPStatus.BAD_REQUEST:
                    default_message: str = await resp.text()
                    raise APIError(default_message, status=HTTPStatus(resp.status))

                if isinstance(response, dict):
                    response = [response]

                return response
        except ClientError as error:
            raise APIError(str(error)) from error
        finally:
            if not self._session:
                await session.close()

    def _get_real_key(self, key: Section, /, *, key_prefix: bool = True) -> str:
        class_name: str = key.__class__.__name__
        _real_key: str = key.name.lower()

        if key_prefix is True:
            _real_key = f"{self.KEY_PATTERN.sub('_', class_name).lower()}_{_real_key}"

        return _real_key

    def _get_position_index(self, section: Section, position: Position | list[int]) -> list[bool | int]:
        idx: list[bool | int] = []

        if isinstance(section, System | Photovoltaic):
            idx = [True]
        elif isinstance(position, Position):
            position_key: str = f"{self.KEY_PATTERN.sub('_', section.__class__.__name__).lower()}"
            _position: int | None = getattr(position, position_key, None)
            idx = list(range(_position)) if _position else [False]
        elif isinstance(position, list):
            idx = [False if p == 0 else (p - 1) for p in position] if position else [True]

        return idx

    def _generate_read_payload(
        self,
        request: list[Section],
        position: Position | list[int],
        allowed_type: list[type[Enum]] | None,
        *,
        extra_attributes: bool = False,
    ) -> Payload:
        payload: Payload = []

        for section in request:
            if (allowed_type and type(section) in allowed_type) or allowed_type is None:
                for idx in self._get_position_index(section=section, position=position):
                    if idx is False:
                        continue

                    for sub_idx in range(idx * 2, section.value.quantity + idx * 2):
                        name: str = section.value.value if idx is True else section.value.value % idx

                        if section.value.quantity > 1:
                            name = section.value.value % sub_idx

                        payload += [
                            ReadPayload(
                                name=name,
                                attr=str(int(extra_attributes is True)),
                            ),
                        ]

        return payload

    @staticmethod
    def _convert_value(section: Section, response: Response, *, human_readable: bool) -> float | int | str:
        value: float | int | str = section.value.value_type(response[0]["value"])
        value = round(value, 2) if isinstance(value, float) else value

        if value in ["true", "false"]:
            value = 1 if value == "true" else 0

        if human_readable and section.value.human_readable:
            try:
                value = section.value.human_readable.from_value(value).name.lower()
            except ValueError as error:
                message: str = f"Can't convert value to human readable value! {response[0]}"
                raise APIError(message) from error

        return value

    @staticmethod
    def _clean_attributes(response: Response) -> dict[str, Any]:
        attributes: dict[str, Any] = response[0].get("attributes", {})
        converted_attributes: dict[str, Any] = {}
        re_pattern: Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

        for key, value in attributes.items():
            if key not in ["unitId", "longText", "formatId", "dynLowerLimit", "dynUpperLimit"]:
                new_attr_key: str = re_pattern.sub("_", key).lower()
                converted_attributes[new_attr_key] = value

        return converted_attributes

    def _get_response_data(
        self,
        response: Response,
        /,
        request: list[Section],
        position: Position | list[int],
        allowed_type: type[Enum] | list[type[Enum]] | None = None,
        *,
        key_prefix: bool = True,
        human_readable: bool = True,
    ) -> dict[str, list[list[Value]] | list[Value]]:
        _response_without_quantity: dict[str, list[Value]] = {}
        _response_with_quantity: dict[str, list[list[Value]]] = {}

        for section in request:
            if (allowed_type and type(section) in allowed_type) or not allowed_type:
                for idx in self._get_position_index(section=section, position=position):
                    if idx is False:
                        continue

                    response_key: str = self._get_real_key(section, key_prefix=key_prefix)
                    response_group: list[Value] = []

                    for _ in range(1, section.value.quantity + 1):
                        _value: Value = {
                            "value": self._convert_value(
                                section,
                                response=response,
                                human_readable=human_readable,
                            ),
                            "attributes": self._clean_attributes(response=response),
                        }

                        response_group.append(_value)
                        del response[0]

                    if section.value.quantity == 1:
                        _response_without_quantity.setdefault(response_key, []).append(response_group[0])
                    else:
                        _response_with_quantity.setdefault(response_key, []).append(response_group)

        _response: dict[str, list[Value] | list[list[Value]]] = {}
        _response.update(_response_without_quantity)
        _response.update(_response_with_quantity)

        return _response

    async def _read_data(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] = 1,
        allowed_type: type[Enum] | list[type[Enum]] | None = None,
        *,
        key_prefix: bool = True,
        human_readable: bool = True,
        extra_attributes: bool = False,
    ) -> dict[str, list[list[Value]] | list[Value]]:
        if isinstance(
            request,
            System
            | BufferTank
            | HotWaterTank
            | HeatPump
            | HeatCircuit
            | SolarCircuit
            | ExternalHeatSource
            | Photovoltaic,
        ):
            request = [request]

        if isinstance(position, int):
            position = [position]

        if isinstance(allowed_type, type):
            allowed_type = [allowed_type]

        payload: Payload = self._generate_read_payload(
            request=request,
            position=position,
            allowed_type=allowed_type,
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
            allowed_type=allowed_type,
            key_prefix=key_prefix,
            human_readable=human_readable,
        )

    def _generate_write_payload(self, request: dict[Section, Any]) -> Payload:
        payload: Payload = []

        for endpoint_properties, values in request.items():
            if not endpoint_properties.value.read_only:
                if isinstance(values, list | tuple):
                    for idx, value in enumerate(values):
                        if value is not None:
                            payload += [
                                WritePayload(
                                    name=endpoint_properties.value.value % idx,
                                    value=str(value),
                                ),
                            ]
                else:
                    payload += [
                        WritePayload(
                            name=endpoint_properties.value.value,
                            value=str(values),
                        ),
                    ]

        return payload

    async def _write_values(self, request: dict[Section, Any]) -> None:
        payload: Payload = self._generate_write_payload(request)

        await self._post(
            payload=json.dumps(payload),
            endpoint=f"{EndpointPath.READ_WRITE_VARS}?action=set",
        )

    @staticmethod
    def _get_allowed_values(enum: type[Enum], /) -> list[str]:
        return [item for pair in ((_.name, str(_.value)) for _ in enum) for item in pair]

    def _get_int_or_str_value(
        self,
        response: dict[str, list[list[Value]] | list[Value]],
        /,
        *,
        section: Section,
        position: int | None = None,
        index: int = 0,
    ) -> int | str:
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(section)

        value: Value | list[Value] = response[_key][_idx]
        _value: str | int = value[index]["value"] if isinstance(value, list) else value["value"]

        try:
            _value = int(_value)
        except ValueError:
            _value = str(_value)

        return _value

    def _get_float_value(
        self,
        response: dict[str, list[list[Value]] | list[Value]],
        /,
        *,
        section: Section,
        position: int | None = None,
        index: int = 0,
        attribute: str | None = None,
    ) -> float:
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(section)

        value: Value | list[Value] = response[_key][_idx]

        return float(
            (
                (value[index]["attributes"][attribute] if attribute else value[index]["value"])
                if isinstance(value, list)
                else (value["attributes"][attribute] if attribute else value["value"])
            ),
        )

    def _get_int_value(
        self,
        response: dict[str, list[list[Value]] | list[Value]],
        /,
        *,
        section: Section,
        position: int | None = None,
        index: int = 0,
        attribute: str | None = None,
    ) -> int:
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(section)

        value: Value | list[Value] = response[_key][_idx]

        return int(
            (
                (value[index]["attributes"][attribute] if attribute else value[index]["value"])
                if isinstance(value, list)
                else (value["attributes"][attribute] if attribute else value["value"])
            ),
        )

    def _get_str_value(
        self,
        response: dict[str, list[list[Value]] | list[Value]],
        /,
        *,
        section: Section,
        position: int | None = None,
        index: int = 0,
    ) -> str:
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(section)

        value: Value | list[Value] = response[_key][_idx]

        return str(value[index]["value"] if isinstance(value, list) else value["value"])


class SystemEndpoints(BaseEndpoints):
    """Class to retrieve the system data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_positions(self) -> Position:
        """Get number of heat pump, heat circuit, solar circuit, hot water tank and external heat sources."""
        response: dict[str, list[Value]] = cast(
            "dict[str, list[Value]]",
            await self._read_data(
                request=[
                    System.HEAT_PUMP_NUMBERS,
                    System.HEAT_CIRCUIT_NUMBERS,
                    System.SOLAR_CIRCUIT_NUMBERS,
                    System.BUFFER_TANK_NUMBERS,
                    System.HOT_WATER_TANK_NUMBERS,
                    System.EXTERNAL_HEAT_SOURCE_NUMBERS,
                ],
                key_prefix=False,
                allowed_type=System,
                extra_attributes=True,
            ),
        )

        return Position(**{k.replace("_numbers", ""): int(v[0]["value"]) for k, v in response.items()})

    async def get_info(self) -> dict[str, Any]:
        """Get system information."""
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getSystemInstalled",
        )
        response[0].pop("ret")
        return response[0]

    async def get_hmi_info(self) -> dict[str, Any]:
        """Get HMI information."""
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getHmiInstalled",
        )
        response[0].pop("ret")
        return response[0]

    async def get_device_info(self) -> dict[str, Any]:
        """Get device information."""
        response: Response = await self._post(
            endpoint=f"{EndpointPath.DEVICE_CONTROL}?action=getDeviceInfo",
        )
        response[0].pop("ret")
        return response[0]

    async def get_number_of_buffer_tanks(self) -> int:
        """Get number of buffer tanks."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.BUFFER_TANK_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.BUFFER_TANK_NUMBERS)

    async def get_number_of_hot_water_tanks(self) -> int:
        """Get number of hot water tanks."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HOT_WATER_TANK_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.HOT_WATER_TANK_NUMBERS)

    async def get_number_of_heat_pumps(self) -> int:
        """Get number of heat pumps."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HEAT_PUMP_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.HEAT_PUMP_NUMBERS)

    async def get_number_of_heating_circuits(self) -> int:
        """Get number of heating circuits."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HEAT_CIRCUIT_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.HEAT_CIRCUIT_NUMBERS)

    async def get_number_of_external_heat_sources(self) -> int:
        """Get number of external heat sources."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.EXTERNAL_HEAT_SOURCE_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.EXTERNAL_HEAT_SOURCE_NUMBERS)

    async def has_photovoltaics(self, *, human_readable: bool = True) -> int | str:
        """Has photovoltaics."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HAS_PHOTOVOLTAICS,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=System.HAS_PHOTOVOLTAICS)

    async def get_outdoor_temperature(self) -> float:
        """Get outdoor temperature."""
        response: dict[str, Any] = await self._read_data(
            request=System.OUTDOOR_TEMPERATURE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.OUTDOOR_TEMPERATURE)

    async def get_operating_mode(self, *, human_readable: bool = True) -> int | str:
        """Get system operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.OPERATING_MODE,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=System.OPERATING_MODE)

    async def set_operating_mode(self, mode: int | str) -> None:
        """Set system operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else SystemOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(SystemOperatingMode)}"
            raise APIError(message) from error

        await self._write_values(request={System.OPERATING_MODE: _mode})

    async def get_cpu_usage(self) -> float:
        """Get CPU usage in percent."""
        response: dict[str, Any] = await self._read_data(
            request=System.CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.CPU_USAGE) / 10

    async def get_webview_cpu_usage(self) -> float:
        """Get webview CPU usage in percent."""
        response: dict[str, Any] = await self._read_data(
            request=System.WEBVIEW_CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.WEBVIEW_CPU_USAGE) / 10

    async def get_webserver_cpu_usage(self) -> float:
        """Get webserver CPU usage in percent."""
        response: dict[str, Any] = await self._read_data(
            request=System.WEBSERVER_CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.WEBSERVER_CPU_USAGE) / 10

    async def get_control_cpu_usage(self) -> float:
        """Get control CPU usage in percent."""
        response: dict[str, Any] = await self._read_data(
            request=System.CONTROL_CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.CONTROL_CPU_USAGE) / 10

    async def get_ram_usage(self) -> int:
        """Get RAM usage in kilobyte."""
        response: dict[str, Any] = await self._read_data(
            request=System.RAM_USAGE,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.RAM_USAGE)

    async def get_free_ram(self) -> int:
        """Get free ram in kilobyte."""
        response: dict[str, Any] = await self._read_data(
            request=System.FREE_RAM,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.FREE_RAM)


class BufferTankEndpoints(BaseEndpoints):
    """Class to send and retrieve the buffer tank data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_name(self, position: int = 1) -> str:
        """Get buffer tank name."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=BufferTank.NAME, position=position)

    async def get_current_top_temperature(self, position: int = 1) -> float:
        """Get current top temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.CURRENT_TOP_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.CURRENT_TOP_TEMPERATURE, position=position)

    async def get_current_bottom_temperature(self, position: int = 1) -> float:
        """Get current bottom temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.CURRENT_BOTTOM_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.CURRENT_BOTTOM_TEMPERATURE, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=BufferTank.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else BufferTankOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(BufferTankOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={BufferTank.OPERATING_MODE: modes})

    async def get_standby_temperature(self, position: int = 1) -> float:
        """Get standby temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.STANDBY_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.STANDBY_TEMPERATURE, position=position)

    async def set_standby_temperature(self, temperature: int, position: int = 1) -> None:
        """Set standby temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={BufferTank.STANDBY_TEMPERATURE: temperatures})

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get target temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.TARGET_TEMPERATURE, position=position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=BufferTank.HEAT_REQUEST, position=position)

    async def get_cool_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get cool request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.COOL_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=BufferTank.COOL_REQUEST, position=position)


class HotWaterTankEndpoints(BaseEndpoints):
    """Class to send and retrieve the hot water tank data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_name(self, position: int = 1) -> str:
        """Get hot water tank name."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HotWaterTank.NAME, position=position)

    async def get_current_temperature(self, position: int = 1) -> float:
        """Get current temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.CURRENT_TEMPERATURE, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HotWaterTankOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(HotWaterTankOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HotWaterTank.OPERATING_MODE: modes})

    async def get_min_target_temperature(self, position: int = 1) -> int:
        """Get min target temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(
            response,
            section=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            attribute="lower_limit",
        )

    async def get_max_target_temperature(self, position: int = 1) -> int:
        """Get max target temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(
            response,
            section=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            attribute="upper_limit",
        )

    async def get_standby_temperature(self, position: int = 1) -> float:
        """Get standby temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.STANDBY_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.STANDBY_TEMPERATURE, position=position)

    async def set_standby_temperature(self, temperature: int, position: int = 1) -> None:
        """Set standby temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.STANDBY_TEMPERATURE: temperatures})

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get target temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.TARGET_TEMPERATURE, position=position)

    async def set_target_temperature(self, temperature: int, position: int = 1) -> None:
        """Set target temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.TARGET_TEMPERATURE: temperatures})

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.HEAT_REQUEST, position=position)

    async def get_hot_water_flow(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get hot water flow."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.HOT_WATER_FLOW,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.HOT_WATER_FLOW, position=position)

    async def get_fresh_water_module_temperature(self, position: int = 1) -> float:
        """Get fresh water module temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.FRESH_WATER_MODULE_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.FRESH_WATER_MODULE_TEMPERATURE, position=position)


class HeatPumpEndpoints(BaseEndpoints):
    """Class to retrieve the heat pump data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_name(self, position: int = 1) -> str:
        """Get heat pump name."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HeatPump.NAME, position=position)

    async def get_state(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat pump state."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.STATE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.STATE, position=position)

    async def get_substate(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat pump state."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SUBSTATE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.SUBSTATE, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatPumpOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(HeatPumpOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatPump.OPERATING_MODE: modes})

    async def get_compressor_use_night_speed(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> int | str:
        """Get compressor use night speed."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_USE_NIGHT_SPEED,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.COMPRESSOR_USE_NIGHT_SPEED, position=position)

    async def set_compressor_use_night_speed(self, mode: int | str, position: int = 1) -> None:
        """Set compressor use night speed."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatPumpCompressorUseNightSpeed[mode.upper()].value
        except KeyError as error:
            message: str = (
                f"Invalid value! Allowed values are {self._get_allowed_values(HeatPumpCompressorUseNightSpeed)}"
            )
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatPump.COMPRESSOR_USE_NIGHT_SPEED: modes})

    async def get_compressor_night_speed(
        self,
        position: int = 1,
        *,
        human_readable: bool = True,
    ) -> float:
        """Get compressor night speed."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_NIGHT_SPEED,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_NIGHT_SPEED, position=position)

    async def set_compressor_night_speed(self, speed: float, position: int = 1) -> None:
        """Set compressor night speed."""
        speeds: list[float | None] = [speed if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatPump.COMPRESSOR_NIGHT_SPEED: speeds})

    async def get_min_compressor_night_speed(self, position: int = 1) -> float:
        """Get min compressor night speed."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_NIGHT_SPEED,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(
            response,
            section=HeatPump.COMPRESSOR_NIGHT_SPEED,
            position=position,
            attribute="lower_limit",
        )

    async def get_max_compressor_night_speed(self, position: int = 1) -> float:
        """Get max compressor night speed."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_NIGHT_SPEED,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(
            response,
            section=HeatPump.COMPRESSOR_NIGHT_SPEED,
            position=position,
            attribute="upper_limit",
        )

    async def get_circulation_pump(self, position: int = 1) -> float:
        """Get circulation pump speed in percent (DEPRECATED)."""
        return await self.get_circulation_pump_speed(position)

    async def get_circulation_pump_speed(self, position: int = 1) -> float:
        """Get circulation pump speed in percent."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.CIRCULATION_PUMP,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.CIRCULATION_PUMP, position=position)

    async def get_source_pump_speed(self, position: int = 1) -> float:
        """Get source pump speed in percent."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_PUMP_SPEED,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.SOURCE_PUMP_SPEED, position=position)

    async def get_flow_temperature(self, position: int = 1) -> float:
        """Get flow temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.FLOW_TEMPERATURE, position=position)

    async def get_return_flow_temperature(self, position: int = 1) -> float:
        """Get return flow temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.RETURN_FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.RETURN_FLOW_TEMPERATURE, position=position)

    async def get_source_input_temperature(self, position: int = 1) -> float:
        """Get source input temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_INPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.SOURCE_INPUT_TEMPERATURE, position=position)

    async def get_source_output_temperature(self, position: int = 1) -> float:
        """Get source output temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_OUTPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.SOURCE_OUTPUT_TEMPERATURE, position=position)

    async def get_compressor_input_temperature(self, position: int = 1) -> float:
        """Get compressor input temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_INPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_INPUT_TEMPERATURE, position=position)

    async def get_compressor_output_temperature(self, position: int = 1) -> float:
        """Get compressor output temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE, position=position)

    async def get_compressor(self, position: int = 1) -> float:
        """Get compressor speed in percent (DEPRECATED)."""
        return await self.get_compressor_speed(position)

    async def get_compressor_speed(self, position: int = 1) -> float:
        """Get compressor speed in percent."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR, position=position)

    async def get_condenser_temperature(self, position: int = 1) -> float:
        """Get condenser temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.CONDENSER_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.CONDENSER_TEMPERATURE, position=position)

    async def get_vaporizer_temperature(self, position: int = 1) -> float:
        """Get vaporizer temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.VAPORIZER_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.VAPORIZER_TEMPERATURE, position=position)

    async def get_high_pressure(self, position: int = 1) -> float:
        """Get high pressure in bar."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HIGH_PRESSURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HIGH_PRESSURE, position=position)

    async def get_low_pressure(self, position: int = 1) -> float:
        """Get low pressure in bar."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.LOW_PRESSURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.LOW_PRESSURE, position=position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HEAT_REQUEST, position=position)

    async def get_compressor_power(self, position: int = 1) -> float:
        """Get compressor power in W."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_POWER, position=position)

    async def get_heating_power(self, position: int = 1) -> float:
        """Get heating power in W."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_POWER, position=position)

    async def get_hot_water_power(self, position: int = 1) -> float:
        """Get hot water power in W."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_POWER, position=position)

    async def get_cop(self, position: int = 1) -> float:
        """Get COP."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COP,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COP, position=position)

    async def get_heating_energy(self, position: int = 1) -> float:
        """Get heating energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_ENERGY, position=position)

    async def get_heating_energy_consumption(self, position: int = 1) -> float:
        """Get energy consumption for heating in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_ENERGY_CONSUMPTION, position=position)

    async def get_heating_spf(self, position: int = 1) -> float:
        """Get heating SPF."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_SPF, position=position)

    async def get_cooling_energy(self, position: int = 1) -> float:
        """Get cooling energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COOLING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COOLING_ENERGY, position=position)

    async def get_cooling_energy_consumption(self, position: int = 1) -> float:
        """Get cooling energy consumption in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COOLING_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COOLING_ENERGY_CONSUMPTION, position=position)

    async def get_cooling_spf(self, position: int = 1) -> float:
        """Get cooling SPF."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COOLING_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COOLING_SPF, position=position)

    async def get_hot_water_energy(self, position: int = 1) -> float:
        """Get hot water energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_ENERGY, position=position)

    async def get_hot_water_energy_consumption(self, position: int = 1) -> float:
        """Get the hot_water energy consumption in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_ENERGY_CONSUMPTION, position=position)

    async def get_hot_water_spf(self, position: int = 1) -> float:
        """Get hot water SPF."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_SPF, position=position)

    async def get_total_thermal_energy(self, position: int = 1) -> float:
        """Get total thermal energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_THERMAL_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.TOTAL_THERMAL_ENERGY, position=position)

    async def get_total_energy_consumption(self, position: int = 1) -> float:
        """Get total energy consumption in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.TOTAL_ENERGY_CONSUMPTION, position=position)

    async def get_total_spf(self, position: int = 1) -> float:
        """Get SPF."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.TOTAL_SPF, position=position)

    async def has_passive_cooling(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Has passive cooling."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_PASSIVE_COOLING,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_PASSIVE_COOLING, position=position)

    async def get_operating_time(self, position: int = 1) -> int:
        """Get the operating time."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.OPERATING_TIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatPump.OPERATING_TIME, position=position)

    async def get_max_runtime(self, position: int = 1) -> int:
        """Get the maximum runtime."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.MAX_RUNTIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatPump.MAX_RUNTIME, position=position)

    async def get_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.ACTIVATION_COUNTER,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatPump.ACTIVATION_COUNTER, position=position)


class HeatCircuitEndpoints(BaseEndpoints):
    """Class to send and retrieve the heating circuit data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_name(self, position: int = 1) -> str:
        """Get heat circuit name."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HeatCircuit.NAME, position=position)

    async def has_room_temperature(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Has room temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HAS_ROOM_TEMPERATURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.HAS_ROOM_TEMPERATURE, position=position)

    async def get_room_temperature(self, position: int = 1) -> float:
        """Get room temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.ROOM_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.ROOM_TEMPERATURE, position=position)

    async def has_room_humidity(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Has room humidity."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HAS_ROOM_HUMIDITY,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.HAS_ROOM_HUMIDITY, position=position)

    async def get_room_humidity(self, position: int = 1) -> float:
        """Get room humidity."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.ROOM_HUMIDITY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.ROOM_HUMIDITY, position=position)

    async def get_dew_point(self, position: int = 1) -> float:
        """Get dew point."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.DEW_POINT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.DEW_POINT, position=position)

    async def get_flow_temperature_setpoint(self, position: int = 1) -> float:
        """Get flow temperature setpoint."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.FLOW_TEMPERATURE_SETPOINT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.FLOW_TEMPERATURE_SETPOINT, position=position)

    async def get_flow_temperature(self, position: int = 1) -> float:
        """Get flow temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.FLOW_TEMPERATURE, position=position)

    async def get_return_flow_temperature(self, position: int = 1) -> float:
        """Get return flow temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.RETURN_FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )

        return self._get_float_value(response, section=HeatCircuit.RETURN_FLOW_TEMPERATURE, position=position)

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get target temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE, position=position)

    async def get_target_temperature_day(self, position: int = 1) -> float:
        """Get target temperature for the day."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_DAY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_DAY, position=position)

    async def set_target_temperature_day(self, temperature: int, position: int = 1) -> None:
        """Set target temperature for the day."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_DAY: temperatures})

    async def get_heating_limit_day(self, position: int = 1) -> float:
        """Get the heating limit for the day."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_LIMIT_DAY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.HEATING_LIMIT_DAY, position=position)

    async def get_target_temperature_night(self, position: int = 1) -> float:
        """Get target temperature for the night."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_NIGHT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_NIGHT, position=position)

    async def set_target_temperature_night(self, temperature: int, position: int = 1) -> None:
        """Set target temperature for the night."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_NIGHT: temperatures})

    async def get_heating_limit_night(self, position: int = 1) -> float:
        """Get the heating limit for the night."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_LIMIT_NIGHT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.HEATING_LIMIT_NIGHT, position=position)

    async def get_target_temperature_away(self, position: int = 1) -> float:
        """Get target temperature when away."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_AWAY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_AWAY, position=position)

    async def set_target_temperature_away(self, temperature: int, position: int = 1) -> None:
        """Set target temperature when away."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_AWAY: temperatures})

    async def get_target_temperature_offset(self, position: int = 1) -> float:
        """Get target temperature offset."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_OFFSET,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_OFFSET, position=position)

    async def set_target_temperature_offset(self, offset: float, position: int = 1) -> None:
        """Set target temperature offset."""
        offsets: list[float | None] = [offset if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_OFFSET: offsets})

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatCircuitOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(HeatCircuitOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatCircuit.OPERATING_MODE: modes})

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.HEAT_REQUEST, position=position)

    async def get_cool_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get cool request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.COOL_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.COOL_REQUEST, position=position)


class SolarCircuitEndpoints(BaseEndpoints):
    """Class to send and retrieve the solar circuit data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_name(self, position: int = 1) -> str:
        """Get solar circuit name."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=SolarCircuit.NAME, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else SolarCircuitOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(SolarCircuitOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={SolarCircuit.OPERATING_MODE: modes})

    async def get_source_temperature(self, position: int = 1) -> float:
        """Get source temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.SOURCE_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.SOURCE_TEMPERATURE, position=position)

    async def get_pump_1_speed(self, position: int = 1) -> float:
        """Get pump 1 speed."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.PUMP_1,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.PUMP_1, position=position)

    async def get_pump_2_speed(self, position: int = 1) -> float:
        """Get pump 2 speed."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.PUMP_2,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.PUMP_2, position=position)

    async def get_current_temperature_1(self, position: int = 1) -> float:
        """Get current temperature 1."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.CURRENT_TEMPERATURE, position=position, index=0)

    async def get_current_temperature_2(self, position: int = 1) -> float:
        """Get current temperature 2."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.CURRENT_TEMPERATURE, position=position, index=1)

    async def get_target_temperature_1(self, position: int = 1) -> float:
        """Get target temperature 1."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.TARGET_TEMPERATURE, position=position, index=0)

    async def set_target_temperature_1(self, temperature: int, position: int = 1) -> None:
        """Set target temperature 1."""
        temperatures: list[float | None] = [
            temperature if SolarCircuit.TARGET_TEMPERATURE.value.quantity * position - 1 == p else None
            for p in range(1, SolarCircuit.TARGET_TEMPERATURE.value.quantity * position + 1)
        ]
        await self._write_values(request={SolarCircuit.TARGET_TEMPERATURE: temperatures})

    async def get_target_temperature_2(self, position: int = 1) -> float:
        """Get target temperature 2."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.TARGET_TEMPERATURE, position=position, index=1)

    async def set_target_temperature_2(self, temperature: int, position: int = 1) -> None:
        """Set target temperature 2."""
        temperatures: list[float | None] = [
            temperature if SolarCircuit.TARGET_TEMPERATURE.value.quantity * position == p else None
            for p in range(1, SolarCircuit.TARGET_TEMPERATURE.value.quantity * position + 1)
        ]
        await self._write_values(request={SolarCircuit.TARGET_TEMPERATURE: temperatures})

    async def get_heat_request_1(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request 1."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.HEAT_REQUEST, position=position, index=0)

    async def get_heat_request_2(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request 2."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.HEAT_REQUEST, position=position, index=1)

    async def get_heating_energy(self, position: int = 1) -> float:
        """Get heating energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.HEATING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.HEATING_ENERGY, position=position)

    async def get_daily_energy(self, position: int = 1) -> float:
        """Get daily energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.DAILY_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.DAILY_ENERGY)

    async def get_actual_power(self, position: int = 1) -> float:
        """Get actual power in W."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.ACTUAL_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.ACTUAL_POWER)


class ExternalHeatSourceEndpoints(BaseEndpoints):
    """Class to send and retrieve the external heat source data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=ExternalHeatSource.OPERATING_MODE)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else ExternalHeatSourceOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = (
                f"Invalid value! Allowed values are {self._get_allowed_values(ExternalHeatSourceOperatingMode)}"
            )
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={ExternalHeatSource.OPERATING_MODE: modes})

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get target temperature."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=ExternalHeatSource.TARGET_TEMPERATURE, position=position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=ExternalHeatSource.HEAT_REQUEST, position=position)

    async def get_operating_time(self, position: int = 1) -> int:
        """Get the operating time."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.OPERATING_TIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=ExternalHeatSource.OPERATING_TIME, position=position)

    async def get_max_runtime(self, position: int = 1) -> int:
        """Get the maximum runtime."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.MAX_RUNTIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=ExternalHeatSource.MAX_RUNTIME, position=position)

    async def get_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.ACTIVATION_COUNTER,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=ExternalHeatSource.ACTIVATION_COUNTER, position=position)


class PhotovoltaicsEndpoints(BaseEndpoints):
    """Class to send and retrieve the photovoltaics data."""

    def __init__(
        self,
        base_url: str,
        *,
        auth: BasicAuth | None = None,
        ssl: bool,
        skip_ssl_verification: bool,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            auth=auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    async def get_excess_power(self) -> float:
        """Get excess power in W."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=Photovoltaic.EXCESS_POWER,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=Photovoltaic.EXCESS_POWER)

    async def get_daily_energy(self) -> float:
        """Get daily energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=Photovoltaic.DAILY_ENERGY,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=Photovoltaic.DAILY_ENERGY)

    async def get_total_energy(self) -> float:
        """Get total energy in kWh."""
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=Photovoltaic.TOTAL_ENERGY,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=Photovoltaic.TOTAL_ENERGY)
