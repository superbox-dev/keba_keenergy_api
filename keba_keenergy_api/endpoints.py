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
from keba_keenergy_api.constants import HeatCircuitHeatingCurve
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HeatCircuitUseHeatingCurve
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HeatPumpCompressorUseNightSpeed
from keba_keenergy_api.constants import HeatPumpOperatingMode
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.constants import LineTablePool
from keba_keenergy_api.constants import MAX_HEATING_CURVE_POINTS
from keba_keenergy_api.constants import MIN_HEATING_CURVE_POINTS
from keba_keenergy_api.constants import Photovoltaic
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import SolarCircuitOperatingMode
from keba_keenergy_api.constants import SwitchValve
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


class ReadChildrenPayload(TypedDict):
    parent: str
    filter: str


class Position(NamedTuple):
    heat_pump: int
    heat_circuit: int
    solar_circuit: int
    buffer_tank: int
    hot_water_tank: int
    external_heat_source: int
    switch_valve: int


class HeatingCurvePoint(NamedTuple):
    outdoor: float
    flow: float


class Value(TypedDict, total=False):
    value: Any
    attributes: dict[str, Any]


ValueResponse: TypeAlias = dict[str, list[list[Value]] | list[Value] | Value]
Payload: TypeAlias = list[ReadPayload | WritePayload]
Response: TypeAlias = list[dict[str, Any]]

HeatingCurvePoints = tuple[HeatingCurvePoint, ...]
HeatingCurves: TypeAlias = dict[str, HeatingCurvePoints]


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
            url: str = f"{self._base_url}{endpoint or ''}"

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

    def _generate_read_children_payloads(
        self,
        request: list[Section],
        position: Position | list[int],
    ) -> list[tuple[Section, ReadChildrenPayload]]:
        payloads: list[tuple[Section, ReadChildrenPayload]] = []

        for section in request:
            for idx in self._get_position_index(section=section, position=position):
                for sub_idx in range(idx * 2, section.value.quantity + idx * 2):
                    parent: str = section.value.value if idx is True else section.value.value % idx

                    if section.value.quantity > 1:
                        parent = section.value.value % sub_idx

                    payloads += [(section, ReadChildrenPayload(parent=parent, filter="none"))]

        return payloads

    @staticmethod
    def _convert_value(section: Section, response: Response, *, human_readable: bool) -> float | int | str:
        value: float | int | str = section.value.value_type(response[0]["value"])
        value = round(value, 2) if isinstance(value, float) else value

        if value in ["true", "false"]:
            value = 1 if value == "true" else 0

        if human_readable and section.value.human_readable:
            try:
                value = section.value.human_readable(value).name.lower()
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
        if not isinstance(request, list):
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
            if isinstance(endpoint_properties, Section):
                if not endpoint_properties.value.read_only:
                    if isinstance(values, list | tuple):
                        for idx, value in enumerate(values):
                            if value is not None:
                                name: str = endpoint_properties.value.value % idx

                                payload += [
                                    WritePayload(
                                        name=name,
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

                # Append extra calls from a helper function
                if hasattr(endpoint_properties.value, "helper"):
                    child_request: dict[Section, Any] = endpoint_properties.value.helper(values)
                    child_payload: Payload = self._generate_write_payload(child_request)

                    payload += child_payload

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
    """API Endpoints to send and retrieve the system data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.system.get_info()

    """

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
        """Get the number of installed devices e.g. heat circuit, solar circuit, etc.

        Returns
        -------
        tuple
            A named tuple with the position information

        """
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
                    System.SWITCH_VALVE_NUMBERS,
                ],
                key_prefix=False,
                allowed_type=System,
                extra_attributes=True,
            ),
        )

        return Position(**{k.replace("_numbers", ""): int(v[0]["value"]) for k, v in response.items()})

    async def get_info(self) -> dict[str, Any]:
        """Get the system information.

        Returns
        -------
        dict
            A dictionary with system information

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getSystemInstalled",
        )
        response[0].pop("ret")
        return response[0]

    async def get_hmi_info(self) -> dict[str, Any]:
        """Get the Web HMI information.

        Returns
        -------
        dict
            A dictionary with Web HMI information

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getHmiInstalled",
        )
        response[0].pop("ret")
        return response[0]

    async def get_device_info(self) -> dict[str, Any]:
        """Get the control unit information.

        Returns
        -------
        dict
            A dictionary with control unit information

        """
        response: Response = await self._post(
            endpoint=f"{EndpointPath.DEVICE_CONTROL}?action=getDeviceInfo",
        )
        response[0].pop("ret")
        return response[0]

    async def get_number_of_buffer_tanks(self) -> int:
        """Get the number of buffer tanks.

        Returns
        -------
        int
            Number of installed buffer tanks

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.BUFFER_TANK_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.BUFFER_TANK_NUMBERS)

    async def get_number_of_hot_water_tanks(self) -> int:
        """Get the number of hot water tanks.

        Returns
        -------
        int
            Number of installed hot water tanks

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HOT_WATER_TANK_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.HOT_WATER_TANK_NUMBERS)

    async def get_number_of_heat_pumps(self) -> int:
        """Get the number of heat pumps.

        Returns
        -------
        int
            Number of installed heat pumps

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HEAT_PUMP_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.HEAT_PUMP_NUMBERS)

    async def get_number_of_heating_circuits(self) -> int:
        """Get the number of heating circuits.

        Returns
        -------
        int
            Number of installed heating circuits

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HEAT_CIRCUIT_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.HEAT_CIRCUIT_NUMBERS)

    async def get_number_of_external_heat_sources(self) -> int:
        """Get the number of external heat sources.

        Returns
        -------
        int
            Number of installed external heat sources

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.EXTERNAL_HEAT_SOURCE_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.EXTERNAL_HEAT_SOURCE_NUMBERS)

    async def get_number_of_switch_valves(self) -> int:
        """Get the number of switch valves.

        Returns
        -------
        int
            Number of installed switch valves

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.SWITCH_VALVE_NUMBERS,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.SWITCH_VALVE_NUMBERS)

    async def has_photovoltaics(self, *, human_readable: bool = True) -> int | str:
        """Check if photovoltaics is available.

        Parameters
        ----------
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.HAS_PHOTOVOLTAICS,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=System.HAS_PHOTOVOLTAICS)

    async def get_outdoor_temperature(self) -> float:
        """Get the outdoor temperature.

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, Any] = await self._read_data(
            request=System.OUTDOOR_TEMPERATURE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.OUTDOOR_TEMPERATURE)

    async def get_operating_mode(self, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the system.

        Parameters
        ----------
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            -1(SETUP) / (0) STANDBY / (1) SUMMER / (2) AUTO_HEAT / (3) AUTO_COOL / (4) AUTO

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=System.OPERATING_MODE,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=System.OPERATING_MODE)

    async def set_operating_mode(self, mode: int | str) -> None:
        """Set the operating mode from the system.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or STANDBY

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else SystemOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(SystemOperatingMode)}"
            raise APIError(message) from error

        await self._write_values(request={System.OPERATING_MODE: _mode})

    async def get_cpu_usage(self) -> float:
        """Get the CPU usage.

        Returns
        -------
        float
            CPU usage in percent

        """
        response: dict[str, Any] = await self._read_data(
            request=System.CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.CPU_USAGE) / 10

    async def get_webview_cpu_usage(self) -> float:
        """Get the webview CPU usage.

        Returns
        -------
        float
            Webview CPU usage in percent

        """
        response: dict[str, Any] = await self._read_data(
            request=System.WEBVIEW_CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.WEBVIEW_CPU_USAGE) / 10

    async def get_webserver_cpu_usage(self) -> float:
        """Get the webserver CPU usage.

        Returns
        -------
        float
            Webserver CPU usage in percent

        """
        response: dict[str, Any] = await self._read_data(
            request=System.WEBSERVER_CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.WEBSERVER_CPU_USAGE) / 10

    async def get_control_cpu_usage(self) -> float:
        """Get the control CPU usage.

        Returns
        -------
        float
            Control CPU usage in percent

        """
        response: dict[str, Any] = await self._read_data(
            request=System.CONTROL_CPU_USAGE,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=System.CONTROL_CPU_USAGE) / 10

    async def get_ram_usage(self) -> int:
        """Get the RAM usage.

        Returns
        -------
        int
            RAM usage in kilobyte

        """
        response: dict[str, Any] = await self._read_data(
            request=System.RAM_USAGE,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.RAM_USAGE)

    async def get_free_ram(self) -> int:
        """Get the free RAM.

        Returns
        -------
        int
            Free RAM in kilobyte.

        """
        response: dict[str, Any] = await self._read_data(
            request=System.FREE_RAM,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=System.FREE_RAM)

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
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.buffer_tank.get_name()

    """

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
        """Get the buffer tank name.

        Parameters
        ----------
        position
            The number of the buffer tanks

        Returns
        -------
        string
            Buffer tank name

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=BufferTank.NAME, position=position)

    async def get_current_top_temperature(self, position: int = 1) -> float:
        """Get the current top temperature from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.CURRENT_TOP_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.CURRENT_TOP_TEMPERATURE, position=position)

    async def get_current_bottom_temperature(self, position: int = 1) -> float:
        """Get the current bottom temperature from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.CURRENT_BOTTOM_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.CURRENT_BOTTOM_TEMPERATURE, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON) / 2 (HEAT_UP)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=BufferTank.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the buffer tanks

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else BufferTankOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(BufferTankOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={BufferTank.OPERATING_MODE: modes})

    async def get_standby_temperature(self, position: int = 1) -> float:
        """Get the standby temperature from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.STANDBY_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.STANDBY_TEMPERATURE, position=position)

    async def set_standby_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the standby temperature from the buffer tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The standby temperature in °C
        position
            The number of the buffer tanks

        """
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={BufferTank.STANDBY_TEMPERATURE: temperatures})

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get the target temperature from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=BufferTank.TARGET_TEMPERATURE, position=position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=BufferTank.HEAT_REQUEST, position=position)

    async def get_cool_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the cool request state from the buffer tank.

        Parameters
        ----------
        position
            The number of the buffer tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=BufferTank.COOL_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=BufferTank.COOL_REQUEST, position=position)


class HotWaterTankEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the hot water tank data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.hot_water_tank.get_name()

    """

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
        """Get the hot water tank name.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        string
            Hot water tank name

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HotWaterTank.NAME, position=position)

    async def get_current_temperature(self, position: int = 1) -> float:
        """Get the current temperature from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.CURRENT_TEMPERATURE, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) OFF / (1) AUTO / (2) ON / (3) HEAT_UP

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the hot water tanks

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else HotWaterTankOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(HotWaterTankOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HotWaterTank.OPERATING_MODE: modes})

    async def get_min_target_temperature(self, position: int = 1) -> int:
        """Get the minimum target temperature from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
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
        """Get the maximum target temperature from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
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
        """Get the standby temperature from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.STANDBY_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.STANDBY_TEMPERATURE, position=position)

    async def set_standby_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the standby temperature from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The standby temperature in °C
        position
            The number of the hot water tanks

        """
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.STANDBY_TEMPERATURE: temperatures})

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get the target temperature from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.TARGET_TEMPERATURE, position=position)

    async def set_target_temperature(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature from the hot water tank.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature in °C
        position
            The number of the hot water tanks

        """
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.TARGET_TEMPERATURE: temperatures})

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the hot water tank.

        Parameters
        ----------
        position
            The number of the hot water tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.HEAT_REQUEST, position=position)

    async def get_hot_water_flow(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the hot water flow from the fresh water module.

        Parameters
        ----------
        position
            The number of the hot water tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.HOT_WATER_FLOW,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.HOT_WATER_FLOW, position=position)

    async def get_fresh_water_module_temperature(self, position: int = 1) -> float:
        """Get the fresh water module temperature.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.FRESH_WATER_MODULE_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.FRESH_WATER_MODULE_TEMPERATURE, position=position)

    async def get_fresh_water_module_pump_speed(self, position: int = 1) -> float:
        """Get the fresh water module pump speed.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Pump speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.FRESH_WATER_MODULE_PUMP_SPEED,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.FRESH_WATER_MODULE_PUMP_SPEED, position=position)

    async def get_circulation_return_temperature(self, position: int = 1) -> float:
        """Get the circulation return temperature.

        Parameters
        ----------
        position
            The number of the hot water tanks

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.CIRCULATION_RETURN_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HotWaterTank.CIRCULATION_RETURN_TEMPERATURE, position=position)

    async def get_circulation_pump_state(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the circulation pump state.

        Parameters
        ----------
        position
            The number of the hot water tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HotWaterTank.CIRCULATION_PUMP_STATE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HotWaterTank.CIRCULATION_PUMP_STATE, position=position)


class HeatPumpEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the heat pump data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.heat_pump.get_name()

    """

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
        """Get the heat pump name.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        string
            Heat pum tank name

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HeatPump.NAME, position=position)

    async def get_state(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat pump state.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) STANDBY / (1) FLOW / (2) AUTO_HEAT / (3) DEFROST / (4) AUTO_COOL / (5) INFLOW / (6) PUMP_DOWN /
            (7) SHUTDOWN / (8) ERROR

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.STATE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.STATE, position=position)

    async def get_substate(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat pump substate.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) NONE /(1) OIL_PREHEATING / (2, 3) PUMP_PRE_RUN / (4) RANDOM_DELAY / (5, 21, 22) PRESSURE_EQUALIZATION
            (6) DEFROST_PRE_FLOW / (7) DEFROST_MONITORING / (8) SNOW_DETECTION / (9) FLUSHING /
            (10) DEFROST_INITIALIZATION / (11) PREHEAT_FLOW / (12) DEFROST / (13, 25) DRIP / (14) DEFROST_END /
            (15, 16) OPEN / (17) COMPRESSOR_POST_RUN / (18) PUMP_POST_RUN / (19) LUBRICATION_PULSE /
            (20, 26) / REDUCED_SPEED / (23) COMPRESSOR_DELAY / (24) DEFROST_VENTING / (27) SWITCH_HEATING_COOLING /
            (28, 33) / WAIT_FOR_COMPRESSOR / (29) COMPRESSOR_STOP / (30) BIVALENT_LOCK / (31) LOCKED /
            (32) RETURN_FLOW_OFF / (34) MIXER_OPEN / (35) ZONE_VALVE / (36) ELECTRIC_DEFROST / (37) COUNTERFLOW_VALVE

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SUBSTATE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.SUBSTATE, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) OFF / (1) ON / (2) BACKUP

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the heat pump.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the heat pumps

        """
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
        """Get the compressor use night speed state.

        Parameters
        ----------
        position
            The number of the hot water tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) OFF / (1) ON

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_USE_NIGHT_SPEED,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.COMPRESSOR_USE_NIGHT_SPEED, position=position)

    async def set_compressor_use_night_speed(self, mode: int | str, position: int = 1) -> None:
        """Set the compressor use night speed.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the heat pumps

        """
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
        """Get the compressor night speed.

        Parameters
        ----------
        position
            The number of the hot water tanks
        human_readable
            Return a human-readable string

        Returns
        -------
        float
            Compressor night speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_NIGHT_SPEED,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_NIGHT_SPEED, position=position)

    async def set_compressor_night_speed(self, speed: float, position: int = 1) -> None:
        """Set the compressor night speed.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        speed
            Set the speed in percent
        position
            The number of the heat pumps

        """
        speeds: list[float | None] = [speed if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatPump.COMPRESSOR_NIGHT_SPEED: speeds})

    async def get_min_compressor_night_speed(self, position: int = 1) -> float:
        """Get the minimum compressor night speed.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Minimum compressor night speed in percent

        """
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
        """Get the maximum compressor night speed.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Maximum compressor night speed in percent

        """
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

    async def get_circulation_pump_speed(self, position: int = 1) -> float:
        """Get the circulation pump speed.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Circulation pump speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.CIRCULATION_PUMP,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.CIRCULATION_PUMP, position=position)

    async def get_source_pump_speed(self, position: int = 1) -> float:
        """Get the source pump speed.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Source pump speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_PUMP_SPEED,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.SOURCE_PUMP_SPEED, position=position)

    async def get_flow_temperature(self, position: int = 1) -> float:
        """Get the flow temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.FLOW_TEMPERATURE, position=position)

    async def get_return_flow_temperature(self, position: int = 1) -> float:
        """Get the return flow temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.RETURN_FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.RETURN_FLOW_TEMPERATURE, position=position)

    async def get_source_input_temperature(self, position: int = 1) -> float:
        """Get the source input temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_INPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.SOURCE_INPUT_TEMPERATURE, position=position)

    async def get_source_output_temperature(self, position: int = 1) -> float:
        """Get the source output temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_OUTPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.SOURCE_OUTPUT_TEMPERATURE, position=position)

    async def get_compressor_input_temperature(self, position: int = 1) -> float:
        """Get the compressor input temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_INPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_INPUT_TEMPERATURE, position=position)

    async def get_compressor_output_temperature(self, position: int = 1) -> float:
        """Get the compressor output temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE, position=position)

    async def get_compressor_speed(self, position: int = 1) -> float:
        """Get the compressor speed from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
             Compressor speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR, position=position)

    async def get_condenser_temperature(self, position: int = 1) -> float:
        """Get the condenser temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
             Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.CONDENSER_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.CONDENSER_TEMPERATURE, position=position)

    async def get_vaporizer_temperature(self, position: int = 1) -> float:
        """Get the vaporizer temperature from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
             Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.VAPORIZER_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.VAPORIZER_TEMPERATURE, position=position)

    async def get_high_pressure(self, position: int = 1) -> float:
        """Get the high pressure from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
             High pressure in bar

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HIGH_PRESSURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HIGH_PRESSURE, position=position)

    async def get_low_pressure(self, position: int = 1) -> float:
        """Get the low pressure from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
             Low pressure in bar

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.LOW_PRESSURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.LOW_PRESSURE, position=position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the heat pump.

        Parameters
        ----------
        position
            The number of the external heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HEAT_REQUEST, position=position)

    async def get_compressor_power(self, position: int = 1) -> float:
        """Get the compressor power from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Compressor power in W

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COMPRESSOR_POWER, position=position)

    async def get_heating_power(self, position: int = 1) -> float:
        """Get the heating power from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Heating power in W

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_POWER, position=position)

    async def get_hot_water_power(self, position: int = 1) -> float:
        """Get the hot water power from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            hot water power in W

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_POWER, position=position)

    async def get_cop(self, position: int = 1) -> float:
        """Get the COP from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            COP

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COP,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COP, position=position)

    async def get_heating_energy(self, position: int = 1) -> float:
        """Get the heating energy from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Heating energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_ENERGY, position=position)

    async def get_heating_energy_consumption(self, position: int = 1) -> float:
        """Get the energy consumption for heating from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Energy consumption for heating in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_ENERGY_CONSUMPTION, position=position)

    async def get_heating_spf(self, position: int = 1) -> float:
        """Get the heating SPF from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Heating SPF

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HEATING_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HEATING_SPF, position=position)

    async def get_cooling_energy(self, position: int = 1) -> float:
        """Get the cooling energy from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Cooling energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COOLING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COOLING_ENERGY, position=position)

    async def get_cooling_energy_consumption(self, position: int = 1) -> float:
        """Get the cooling energy consumption from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Cooling energy consumption in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COOLING_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COOLING_ENERGY_CONSUMPTION, position=position)

    async def get_cooling_spf(self, position: int = 1) -> float:
        """Get the cooling SPF from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Cooling SPF

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.COOLING_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.COOLING_SPF, position=position)

    async def get_hot_water_energy(self, position: int = 1) -> float:
        """Get the hot water energy from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Hot water energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_ENERGY, position=position)

    async def get_hot_water_energy_consumption(self, position: int = 1) -> float:
        """Get the hot water energy consumption from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Hot water energy consumption in kWh.

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_ENERGY_CONSUMPTION, position=position)

    async def get_hot_water_spf(self, position: int = 1) -> float:
        """Get the hot water SPF from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Hot water SPF

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.HOT_WATER_SPF, position=position)

    async def get_total_thermal_energy(self, position: int = 1) -> float:
        """Get the total thermal energy from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Total thermal energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_THERMAL_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.TOTAL_THERMAL_ENERGY, position=position)

    async def get_total_energy_consumption(self, position: int = 1) -> float:
        """Get the total energy consumption from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            Total energy consumption in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.TOTAL_ENERGY_CONSUMPTION, position=position)

    async def get_total_spf(self, position: int = 1) -> float:
        """Get the SPF from the heat pump.

        Parameters
        ----------
        position
            The number of the heat pumps

        Returns
        -------
        float
            SPF

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_SPF,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatPump.TOTAL_SPF, position=position)

    async def has_passive_cooling(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if passive cooling for the heat pump is available.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_PASSIVE_COOLING,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_PASSIVE_COOLING, position=position)

    async def get_operating_time(self, position: int = 1) -> int:
        """Get the operating time from the external heat pump.

        Parameters
        ----------
        position
            The number of the external heat pumps

        Returns
        -------
        integer
            Operating time in seconds

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.OPERATING_TIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatPump.OPERATING_TIME, position=position)

    async def get_max_runtime(self, position: int = 1) -> int:
        """Get the maximum runtime from the external heat pump.

        Parameters
        ----------
        position
            The number of the external heat pumps

        Returns
        -------
        integer
            Maximum runtime in seconds

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.MAX_RUNTIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatPump.MAX_RUNTIME, position=position)

    async def get_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter from the heat pump.

        Parameters
        ----------
        position
            The number of the external heat pumps

        Returns
        -------
        integer
            Number of external heat source activation

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.ACTIVATION_COUNTER,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatPump.ACTIVATION_COUNTER, position=position)

    async def has_compressor_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a compressor failure.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_COMPRESSOR_FAILURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_COMPRESSOR_FAILURE, position=position)

    async def has_source_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source failure.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_SOURCE_FAILURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_SOURCE_FAILURE, position=position)

    async def has_source_actuator_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source actuator failure.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_SOURCE_ACTUATOR_FAILURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_SOURCE_ACTUATOR_FAILURE, position=position)

    async def has_three_phase_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a three-phase failure.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_THREE_PHASE_FAILURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_THREE_PHASE_FAILURE, position=position)

    async def has_source_pressure_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source pressure failure.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_SOURCE_PRESSURE_FAILURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_SOURCE_PRESSURE_FAILURE, position=position)

    async def has_vfd_failure(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if the heat pump has a source pressure variable frequency drive (VFD) failure.

        Parameters
        ----------
        position
            The number of the heat pumps
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatPump.HAS_VFD_FAILURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatPump.HAS_VFD_FAILURE, position=position)


class HeatCircuitEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the heat circuit data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.heat_circuit.get_name()

    """

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
        """Get the heat circuit name.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        string
            Heat circuit name

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HeatCircuit.NAME, position=position)

    async def has_room_temperature(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if room temperature from the heat circuit is available.

        Parameters
        ----------
        position
            The number of the heat circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HAS_ROOM_TEMPERATURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.HAS_ROOM_TEMPERATURE, position=position)

    async def get_room_temperature(self, position: int = 1) -> float:
        """Get the room temperature from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.ROOM_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.ROOM_TEMPERATURE, position=position)

    async def has_room_humidity(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Check if room humidity from the heat circuit is available.

        Parameters
        ----------
        position
            The number of the heat circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HAS_ROOM_HUMIDITY,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.HAS_ROOM_HUMIDITY, position=position)

    async def get_room_humidity(self, position: int = 1) -> float:
        """Get the room humidity from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Humidity in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.ROOM_HUMIDITY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.ROOM_HUMIDITY, position=position)

    async def get_dew_point(self, position: int = 1) -> float:
        """Get the dew point from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.DEW_POINT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.DEW_POINT, position=position)

    async def get_flow_temperature_setpoint(self, position: int = 1) -> float:
        """Get the flow temperature setpoint from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.FLOW_TEMPERATURE_SETPOINT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.FLOW_TEMPERATURE_SETPOINT, position=position)

    async def get_mixer_flow_temperature(self, position: int = 1) -> float:
        """Get the mixer flow temperature from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.FLOW_TEMPERATURE, position=position)

    async def get_mixer_return_flow_temperature(self, position: int = 1) -> float:
        """Get the mixer return flow temperature from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.MIXER_RETURN_FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.MIXER_RETURN_FLOW_TEMPERATURE, position=position)

    async def get_return_flow_temperature(self, position: int = 1) -> float:
        """Get the return flow temperature from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.RETURN_FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )

        return self._get_float_value(response, section=HeatCircuit.RETURN_FLOW_TEMPERATURE, position=position)

    async def get_target_temperature(self, position: int = 1) -> float:
        """Get the target temperature from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE, position=position)

    async def get_selected_target_temperature(self, position: int = 1) -> float:
        """Get the selected target temperature from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.SELECTED_TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.SELECTED_TARGET_TEMPERATURE, position=position)

    async def get_target_temperature_day(self, position: int = 1) -> float:
        """Get the target temperature for the day from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_DAY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_DAY, position=position)

    async def set_target_temperature_day(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature for the day from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature for the day in °C
        position
            The number of the heat circuits

        """
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_DAY: temperatures})

    async def get_heating_limit_day(self, position: int = 1) -> float:
        """Get the heating limit for the day from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_LIMIT_DAY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.HEATING_LIMIT_DAY, position=position)

    async def get_target_temperature_night(self, position: int = 1) -> float:
        """Get the target temperature for the night from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_NIGHT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_NIGHT, position=position)

    async def set_target_temperature_night(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature for the night from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature for the day in °C
        position
            The number of the heat circuits

        """
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_NIGHT: temperatures})

    async def get_heating_limit_night(self, position: int = 1) -> float:
        """Get the heating limit for the night from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_LIMIT_NIGHT,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.HEATING_LIMIT_NIGHT, position=position)

    async def get_target_temperature_away(self, position: int = 1) -> float:
        """Get the target temperature when away for the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_AWAY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_AWAY, position=position)

    async def set_target_temperature_away(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature when away for the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            The target temperature for the day in °C
        position
            The number of the heat circuits

        """
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_AWAY: temperatures})

    async def get_target_temperature_offset(self, position: int = 1) -> float:
        """Get the target temperature offset from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_OFFSET,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.TARGET_TEMPERATURE_OFFSET, position=position)

    async def set_target_temperature_offset(self, offset: float, position: int = 1) -> None:
        """Set the target temperature offset for the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        offset
            The target temperature offset
        position
            The number of the heat circuits

        """
        offsets: list[float | None] = [offset if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_OFFSET: offsets})

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (AUTO) / (2) DAY / (3) NIGHT / (4) HOLIDAY / (5) PARTY / (8) EXTERNAL / (9) ROOM_CONTROL

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the heat circuits

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatCircuitOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(HeatCircuitOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatCircuit.OPERATING_MODE: modes})

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the heat circuit.

        Parameters
        ----------
        position
            The number of the external heat circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.HEAT_REQUEST, position=position)

    async def get_cool_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the cool request state from the heat circuit.

        Parameters
        ----------
        position
            The number of the external heat circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.COOL_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.COOL_REQUEST, position=position)

    async def get_away_start_date(self, position: int = 1) -> int:
        """Get the away start date from the heating circuit.

        Parameters
        ----------
        position
            The number of the external heat circuits

        Returns
        -------
        integer
            Start date as unix timestamp

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.AWAY_START_DATE,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatCircuit.AWAY_START_DATE, position=position)

    async def set_away_start_date(self, timestamp: int, position: int = 1) -> None:
        """Set the away start date from the heating circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        timestamp
            Start date as unix timestamp
        position
            The number of the external heat circuits

        """
        timestamps: list[float | None] = [timestamp if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.AWAY_START_DATE: timestamps})

    async def get_away_end_date(self, position: int = 1) -> int:
        """Get the away end date from the heating circuit.

        Parameters
        ----------
        position
            The number of the external heat circuits

        Returns
        -------
        integer
            Start date as unix timestamp

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.AWAY_END_DATE,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=HeatCircuit.AWAY_END_DATE, position=position)

    async def set_away_end_date(self, timestamp: int, position: int = 1) -> None:
        """Set the away end date from the heating circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        timestamp
            Start date as unix timestamp
        position
            The number of the external heat circuits

        """
        timestamps: list[float | None] = [timestamp if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.AWAY_END_DATE: timestamps})

    async def get_heating_curve_offset(self, position: int = 1) -> float:
        """Get the heating curve offset from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Offset in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_CURVE_OFFSET,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.HEATING_CURVE_OFFSET, position=position)

    async def set_heating_curve_offset(self, offset: float, position: int = 1) -> None:
        """Set the heating curve offset from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        offset
            The offset in °C
        position
            The number of the heat circuits

        """
        offsets: list[float | None] = [offset if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.HEATING_CURVE_OFFSET: offsets})

    async def get_heating_curve_slope(self, position: int = 1) -> float:
        """Get the heating curve slope from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        float
            Slope

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_CURVE_SLOPE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=HeatCircuit.HEATING_CURVE_SLOPE, position=position)

    async def set_heating_curve_slope(self, slope: float, position: int = 1) -> None:
        """Set the heating curve slope from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        slope
            The slope
        position
            The number of the heat circuits

        """
        slopes: list[float | None] = [slope if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.HEATING_CURVE_SLOPE: slopes})

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
            The number of the heat circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) OFF / (1) ON

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.USE_HEATING_CURVE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=HeatCircuit.USE_HEATING_CURVE, position=position)

    async def set_use_heating_curve(self, mode: int | str, position: int = 1) -> None:
        """Set the use heating curve.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the heat circuits

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatCircuitUseHeatingCurve[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(HeatCircuitUseHeatingCurve)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatCircuit.USE_HEATING_CURVE: modes})

    async def get_heating_curve(self, position: int = 1) -> str:
        """Get the heating curve from the heat circuit.

        Parameters
        ----------
        position
            The number of the heat circuits

        Returns
        -------
        string

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_CURVE,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=HeatCircuit.HEATING_CURVE, position=position).upper()

    async def set_heating_curve(self, heating_curve: str, position: int = 1) -> None:
        """Set the heating curve from the heat circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        heating_curve
            The heating curve name
        position
            The number of the heat circuits

        """
        try:
            _name = HeatCircuitHeatingCurve[heating_curve.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {[str(_.value) for _ in HeatCircuitHeatingCurve]}"
            raise APIError(message) from error

        names: list[str | None] = [_name if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatCircuit.HEATING_CURVE: names})

    async def get_heating_curve_points(self, heating_curve: str | None = None) -> HeatingCurves:
        """Get the heating curve points.

        Parameters
        ----------
        heating_curve
            The heating curve name

        Returns
        -------
        dict
            One or more heating curves and the points

        """
        payload: Payload = []

        # HC1 - HC8 is position 0 - 7
        # HC FBH is 12
        # HC HK is 13

        for idx in [*list(range(8)), 12, 13]:
            payload += [
                ReadPayload(
                    name=LineTablePool.HEATING_CURVE_NAME.value.value % idx,
                    attr="1",
                ),
                ReadPayload(
                    name=LineTablePool.HEATING_CURVE_POINTS.value.value % idx,
                    attr="1",
                ),
            ]

            for point_idx in list(range(16)):
                payload += [
                    ReadPayload(
                        name=LineTablePool.HEATING_CURVE_POINT_X.value.value % (idx, point_idx),
                        attr="1",
                    ),
                    ReadPayload(
                        name=LineTablePool.HEATING_CURVE_POINT_Y.value.value % (idx, point_idx),
                        attr="1",
                    ),
                ]

        response: Response = await self._post(
            payload=json.dumps(payload),
            endpoint=EndpointPath.READ_WRITE_VARS,
        )

        data: HeatingCurves = {}

        data_idx: int = 0
        curve_indices = (*range(8), 12, 13)
        points_per_table: int = 16
        values_per_point: int = 2

        valid_curves: dict[str, str] = {curve.value: curve.name.lower() for curve in HeatCircuitHeatingCurve}

        for _ in curve_indices:
            raw_name = response[data_idx]["value"]
            name: str | None = valid_curves.get(raw_name)

            if name is not None:
                no_of_points = int(response[data_idx + 1]["value"])
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

        if heating_curve is not None:
            try:
                return {heating_curve.lower(): data[heating_curve.lower()]}
            except KeyError as error:
                message: str = f'Heating curve "{heating_curve}" not found'
                raise APIError(message) from error

        return data

    async def set_heating_curve_points(self, heating_curve: str, points: HeatingCurvePoints) -> None:
        """Set the heating curve points.

        Parameters
        ----------
        heating_curve
            The heating curve name
        points
            Heating curve points

        """
        message: str

        try:
            idx: int = HeatCircuitHeatingCurve[heating_curve].id
        except KeyError as error:
            message = f"Invalid value! Allowed values are {[str(_.value) for _ in HeatCircuitHeatingCurve]}"
            raise APIError(message) from error
        else:
            read_payload: Payload = [
                ReadPayload(
                    name=LineTablePool.HEATING_CURVE_NAME.value.value % idx,
                    attr="1",
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

            await self._post(
                payload=json.dumps(
                    WritePayload(
                        name=LineTablePool.SAVE_HEATING_CURVE.value.value % idx,
                        value="192",
                    )
                ),
                endpoint=f"{EndpointPath.READ_WRITE_VARS}?action=set",
            )


class SolarCircuitEndpoints(BaseEndpoints):
    """API Endpoints to send and retrieve the solar circuit data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.solar_circuit.get_name()

    """

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
        """Get the solar circuit name.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        string
            Solar circuit name

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.NAME,
            position=position,
            extra_attributes=True,
        )
        return self._get_str_value(response, section=SolarCircuit.NAME, position=position)

    async def get_operating_mode(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the operating mode from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.OPERATING_MODE, position=position)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the solar circuits

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else SolarCircuitOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(SolarCircuitOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={SolarCircuit.OPERATING_MODE: modes})

    async def get_priority_1_before_2(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get priority 1 before 2 for the pumps from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.PRIORITY_1_BEFORE_2,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.PRIORITY_1_BEFORE_2, position=position)

    async def set_priority_1_before_2(self, mode: int | str, position: int = 1) -> None:
        """Set the priority 1 before 2 for the pumps from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the solar circuits

        """
        try:
            _mode: int | None = mode if isinstance(mode, int) else SolarCircuitOperatingMode[mode.upper()].value
        except KeyError as error:
            message: str = f"Invalid value! Allowed values are {self._get_allowed_values(SolarCircuitOperatingMode)}"
            raise APIError(message) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(
            request={
                SolarCircuit.PRIORITY_1_BEFORE_2: modes,
            },
        )

    async def get_source_temperature(self, position: int = 1) -> float:
        """Get source temperature from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.SOURCE_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.SOURCE_TEMPERATURE, position=position)

    async def get_pump_1_speed(self, position: int = 1) -> float:
        """Get pump 1 speed.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Pump 1 speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.PUMP_1,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.PUMP_1, position=position)

    async def get_pump_2_speed(self, position: int = 1) -> float:
        """Get pump 2 speed.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Pump 2 speed in percent

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.PUMP_2,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.PUMP_2, position=position)

    async def get_current_temperature_1(self, position: int = 1) -> float:
        """Get current temperature 1 from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.CURRENT_TEMPERATURE, position=position, index=0)

    async def get_current_temperature_2(self, position: int = 1) -> float:
        """Get current temperature 2 from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.CURRENT_TEMPERATURE, position=position, index=1)

    async def get_target_temperature_1(self, position: int = 1) -> float:
        """Get target temperature 1 from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.TARGET_TEMPERATURE, position=position, index=0)

    async def set_target_temperature_1(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature 1 from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the solar circuits

        """
        temperatures: list[float | None] = [
            temperature if SolarCircuit.TARGET_TEMPERATURE.value.quantity * position - 1 == p else None
            for p in range(1, SolarCircuit.TARGET_TEMPERATURE.value.quantity * position + 1)
        ]
        await self._write_values(request={SolarCircuit.TARGET_TEMPERATURE: temperatures})

    async def get_target_temperature_2(self, position: int = 1) -> float:
        """Get target temperature 2 from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.TARGET_TEMPERATURE, position=position, index=1)

    async def set_target_temperature_2(self, temperature: float, position: int = 1) -> None:
        """Set the target temperature 2 from the solar circuit.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        temperature
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the solar circuits

        """
        temperatures: list[float | None] = [
            temperature if SolarCircuit.TARGET_TEMPERATURE.value.quantity * position == p else None
            for p in range(1, SolarCircuit.TARGET_TEMPERATURE.value.quantity * position + 1)
        ]
        await self._write_values(request={SolarCircuit.TARGET_TEMPERATURE: temperatures})

    async def get_heat_request_1(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request 1 state from the solar circuit.

        Parameters
        ----------
        position
            The number of the external solar circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.HEAT_REQUEST, position=position, index=0)

    async def get_heat_request_2(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request 2 state from the solar circuit.

        Parameters
        ----------
        position
            The number of the external solar circuits
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SolarCircuit.HEAT_REQUEST, position=position, index=1)

    async def get_heating_energy(self, position: int = 1) -> float:
        """Get heating energy from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Heating energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.HEATING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.HEATING_ENERGY, position=position)

    async def get_daily_energy(self, position: int = 1) -> float:
        """Get daily energy from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Daily energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.DAILY_ENERGY,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.DAILY_ENERGY)

    async def get_actual_power(self, position: int = 1) -> float:
        """Get actual power from the solar circuit.

        Parameters
        ----------
        position
            The number of the solar circuits

        Returns
        -------
        float
            Actual power in W

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SolarCircuit.ACTUAL_POWER,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=SolarCircuit.ACTUAL_POWER)


class ExternalHeatSourceEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the external heat source data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.external_heat_source.get_operating_mode()

    """

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
        """Get the operating mode from the external heat source.

        Parameters
        ----------
        position
            The number of the external heat sources
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=ExternalHeatSource.OPERATING_MODE)

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set the operating mode from the external heat source.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Parameters
        ----------
        mode
            Set the mode as integer or string (human-readable) e.g. 0 or OFF
        position
            The number of the external heat sources

        """
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
        """Get target temperature from the external heat source.

        Parameters
        ----------
        position
            The number of the external heat sources

        Returns
        -------
        float
            Temperature in °C

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=ExternalHeatSource.TARGET_TEMPERATURE, position=position)

    async def get_heat_request(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get the heat request state from the external heat source.

        Parameters
        ----------
        position
            The number of the external heat sources
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            0 (OFF) / 1 (ON)

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=ExternalHeatSource.HEAT_REQUEST, position=position)

    async def get_operating_time(self, position: int = 1) -> int:
        """Get the operating time from the external heat source.

        Parameters
        ----------
        position
            The number of the external heat sources

        Returns
        -------
        integer
            Operating time in seconds

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.OPERATING_TIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=ExternalHeatSource.OPERATING_TIME, position=position)

    async def get_max_runtime(self, position: int = 1) -> int:
        """Get the maximum runtime from the external heat source.

        Parameters
        ----------
        position
            The number of the external heat sources

        Returns
        -------
        integer
            Maximum runtime in seconds

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.MAX_RUNTIME,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=ExternalHeatSource.MAX_RUNTIME, position=position)

    async def get_activation_counter(self, position: int = 1) -> int:
        """Get the activation counter from the external heat source.

        Parameters
        ----------
        position
            The number of the external heat sources

        Returns
        -------
        integer
            Number of external heat source activation

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=ExternalHeatSource.ACTIVATION_COUNTER,
            position=position,
            extra_attributes=True,
        )
        return self._get_int_value(response, section=ExternalHeatSource.ACTIVATION_COUNTER, position=position)


class SwitchValveEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the switch valve data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.switch_valve.get_position()

    """

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

    async def get_position(self, position: int = 1, *, human_readable: bool = True) -> int | str:
        """Get switch valve position.

        Parameters
        ----------
        position
            The number of the switch valves
        human_readable
            Return a human-readable string

        Returns
        -------
        integer or string
            (0) NEUTRAL / (1) OPEN / (2) CLOSED

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=SwitchValve.POSITION,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        return self._get_int_or_str_value(response, section=SwitchValve.POSITION, position=position)


class PhotovoltaicsEndpoints(BaseEndpoints):
    """API Endpoints to retrieve the photovoltaic data.

    Examples
    --------
    >>> client = KebaKeEnergyAPI(
    >>>     host="ap4400.local",
    >>>     username="test",
    >>>     password="test",
    >>>     ssl=True,
    >>>     skip_ssl_verification=True
    >>> )
    >>> client.photovoltaics.get_excess_power()

    """

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
        """Get excess power.

        Returns
        -------
        float
            Excess power in W

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=Photovoltaic.EXCESS_POWER,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=Photovoltaic.EXCESS_POWER)

    async def get_daily_energy(self) -> float:
        """Get daily energy.

        Returns
        -------
        float
            Daily energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=Photovoltaic.DAILY_ENERGY,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=Photovoltaic.DAILY_ENERGY)

    async def get_total_energy(self) -> float:
        """Get total energy.

        Returns
        -------
        float
            Total energy in kWh

        """
        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=Photovoltaic.TOTAL_ENERGY,
            extra_attributes=True,
        )
        return self._get_float_value(response, section=Photovoltaic.TOTAL_ENERGY)
