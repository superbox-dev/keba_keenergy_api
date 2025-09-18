"""Retrieve hot water tank data."""

import json
import re
from enum import Enum
from json import JSONDecodeError
from re import Pattern
from typing import Any
from typing import NamedTuple
from typing import TypeAlias
from typing import TypedDict

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.constants import EndpointPath
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HeatPumpOperatingMode
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import System
from keba_keenergy_api.constants import SystemOperatingMode
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import InvalidJsonError


class ReadPayload(TypedDict):
    name: str
    attr: str


class WritePayload(TypedDict):
    name: str
    value: str


class Position(NamedTuple):
    heat_pump: int
    heat_circuit: int
    hot_water_tank: int


class Value(TypedDict, total=False):
    value: Any
    attributes: dict[str, Any]


ValueResponse: TypeAlias = dict[str, list[Value] | Value]
Payload: TypeAlias = list[ReadPayload | WritePayload]
Response: TypeAlias = list[dict[str, Any]]


class BaseEndpoints:
    """Base class for all endpoint classes."""

    KEY_PATTERN: Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

    def __init__(
        self,
        base_url: str,
        *,
        ssl: bool,
        session: ClientSession | None = None,
    ) -> None:
        self._base_url: str = base_url
        self._ssl: bool = ssl
        self._session: ClientSession | None = session

    async def _post(self, payload: str | None = None, endpoint: str | None = None) -> Response:
        """Run a POST request against the API."""
        session: ClientSession = (
            self._session
            if self._session and not self._session.closed
            else ClientSession(timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT))
        )

        try:
            async with session.post(
                f"{self._base_url}{endpoint if endpoint else ''}",
                ssl=self._ssl,
                data=payload,
            ) as resp:
                response: list[dict[str, Any]] = await resp.json(
                    content_type="application/json;charset=utf-8",
                )
        except JSONDecodeError as error:
            response_text = await resp.text()
            raise InvalidJsonError(response_text) from error
        finally:
            if not self._session:
                await session.close()

        if isinstance(response, dict) and "developerMessage" in response:
            raise APIError(response["developerMessage"])

        if isinstance(response, dict):
            response = [response]

        return response

    def _get_real_key(self, key: Section, *, key_prefix: bool = True) -> str:
        class_name: str = key.__class__.__name__
        _real_key: str = key.name.lower()

        if key_prefix is True:
            _real_key = f"{self.KEY_PATTERN.sub('_', class_name).lower()}_{_real_key}"

        return _real_key

    def _get_position_index(self, section: Section, position: Position | list[int | None]) -> list[int | None]:
        idx: list[int | None] = []

        if isinstance(section, System):
            idx = [None]
        elif isinstance(position, Position):
            position_key: str = f"{self.KEY_PATTERN.sub('_', section.__class__.__name__).lower()}"
            _position: int | None = getattr(position, position_key, None)
            idx = list(range(_position)) if _position else [None]
        elif isinstance(position, list):
            idx = [p if p is None else (p - 1) for p in position]

        return idx

    def _generate_read_payload(
        self,
        request: list[Section],
        position: Position | list[int | None],
        allowed_type: list[type[Enum]] | None,
        *,
        extra_attributes: bool = False,
    ) -> Payload:
        payload: Payload = []

        for section in request:
            if (allowed_type and type(section) in allowed_type) or allowed_type is None:
                for idx in self._get_position_index(section=section, position=position):
                    payload += [
                        ReadPayload(
                            name=section.value.value if idx is None else section.value.value % idx,
                            attr=str(int(extra_attributes is True)),
                        ),
                    ]

        return payload

    @staticmethod
    def _convert_value(section: Section, response: Response, *, human_readable: bool) -> float | int | str:
        value: float | int | str = section.value.value_type(response[0]["value"])
        value = round(value, 2) if isinstance(value, float) else value

        if human_readable and section.value.human_readable:
            try:
                value = section.value.human_readable(value).name.lower()
            except ValueError as error:
                msg: str = f"Can't convert value to human readable value! {response[0]}"

                raise APIError(msg) from error

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

    async def _read_data(
        self,
        request: Section | list[Section],
        position: Position | int | list[int | None] | None = 1,
        allowed_type: type[Enum] | list[type[Enum]] | None = None,
        *,
        key_prefix: bool = True,
        human_readable: bool = True,
        extra_attributes: bool = False,
    ) -> dict[str, list[Value]]:
        if isinstance(request, System | HotWaterTank | HeatPump | HeatCircuit):
            request = [request]

        if isinstance(position, int) or position is None:
            position = [position]

        if isinstance(allowed_type, type):
            allowed_type = [allowed_type]

        payload: Payload = self._generate_read_payload(
            request=request,
            position=position,
            allowed_type=allowed_type,
            extra_attributes=extra_attributes,
        )

        _response: Response = await self._post(
            payload=json.dumps(payload),
            endpoint=EndpointPath.READ_WRITE_VARS,
        )

        response: dict[str, list[Value]] = {}

        for section in request:
            if (allowed_type and type(section) in allowed_type) or not allowed_type:
                for _ in self._get_position_index(section=section, position=position):
                    response_key: str = self._get_real_key(section, key_prefix=key_prefix)

                    if not response.get(response_key):
                        response[response_key] = []

                    _value: Value = {
                        "value": self._convert_value(
                            section,
                            response=_response,
                            human_readable=human_readable,
                        ),
                        "attributes": self._clean_attributes(response=_response),
                    }

                    response[response_key].append(_value)
                    del _response[0]

        return response

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


class SystemEndpoints(BaseEndpoints):
    """Class to retrieve the system data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_positions(self) -> Position:
        """Get number of heat pump, heating circuit and hot water tank."""
        response: dict[str, list[Value]] = await self._read_data(
            request=[
                System.HEAT_PUMP_NUMBERS,
                System.HEAT_CIRCUIT_NUMBERS,
                System.HOT_WATER_TANK_NUMBERS,
            ],
            position=None,
            key_prefix=False,
            allowed_type=System,
            extra_attributes=True,
        )

        return Position(**{k.replace("_numbers", ""): int(v[0]["value"]) for k, v in response.items()})

    async def get_info(self) -> dict[str, Any]:
        """Get system information."""
        response: Response = await self._post(
            endpoint=f"{EndpointPath.SW_UPDATE}?action=getSystemInstalled",
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

    async def get_number_of_hot_water_tanks(self) -> int:
        """Get number of hot water tanks."""
        response: dict[str, list[Value]] = await self._read_data(
            request=System.HOT_WATER_TANK_NUMBERS,
            position=None,
            extra_attributes=True,
        )
        _key: str = self._get_real_key(System.HOT_WATER_TANK_NUMBERS)
        return int(response[_key][0]["value"])

    async def get_number_of_heat_pumps(self) -> int:
        """Get number of heat pumps."""
        response: dict[str, list[Value]] = await self._read_data(
            request=System.HEAT_PUMP_NUMBERS,
            position=None,
            extra_attributes=True,
        )
        _key: str = self._get_real_key(System.HEAT_PUMP_NUMBERS)
        return int(response[_key][0]["value"])

    async def get_number_of_heating_circuits(self) -> int:
        """Get number of heating circuits."""
        response: dict[str, list[Value]] = await self._read_data(
            request=System.HEAT_CIRCUIT_NUMBERS,
            position=None,
            extra_attributes=True,
        )
        _key: str = self._get_real_key(System.HEAT_CIRCUIT_NUMBERS)
        return int(response[_key][0]["value"])

    async def get_outdoor_temperature(self) -> float:
        """Get outdoor temperature."""
        response: dict[str, Any] = await self._read_data(
            request=System.OUTDOOR_TEMPERATURE,
            position=None,
            extra_attributes=True,
        )
        _key: str = self._get_real_key(System.OUTDOOR_TEMPERATURE)
        return float(response[_key][0]["value"])

    async def get_operating_mode(self, *, human_readable: bool = True) -> int | str:
        """Get system operating mode."""
        response: dict[str, list[Value]] = await self._read_data(
            request=System.OPERATING_MODE,
            position=None,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _key: str = self._get_real_key(System.OPERATING_MODE)

        try:
            _value: int | str = int(response[_key][0]["value"])
        except ValueError:
            _value = str(response[_key][0]["value"])

        return _value

    async def set_operating_mode(self, mode: int | str) -> None:
        """Set sytem operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else SystemOperatingMode[mode.upper()].value
        except KeyError as error:
            msg: str = "Invalid operating mode!"
            raise APIError(msg) from error

        await self._write_values(request={System.OPERATING_MODE: _mode})


class HotWaterTankEndpoints(BaseEndpoints):
    """Class to send and retrieve the hot water tank data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_current_temperature(self, position: int | None = 1) -> float:
        """Get current temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.CURRENT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.CURRENT_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_operating_mode(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.OPERATING_MODE)

        try:
            _value: int | str = int(response[_key][_idx]["value"])
        except ValueError:
            _value = str(response[_key][_idx]["value"])

        return _value

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HotWaterTankOperatingMode[mode.upper()].value
        except KeyError as error:
            msg: str = "Invalid operating mode!"
            raise APIError(msg) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HotWaterTank.OPERATING_MODE: modes})

    async def get_min_target_temperature(self, position: int | None = 1) -> int:
        """Get min possible target temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.TARGET_TEMPERATURE)
        return int(response[_key][_idx]["attributes"]["lower_limit"])

    async def get_max_target_temperature(self, position: int | None = 1) -> int:
        """Get max possible target temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.TARGET_TEMPERATURE)
        return int(response[_key][_idx]["attributes"]["upper_limit"])

    async def get_standby_temperature(self, position: int | None = 1) -> float:
        """Get standby temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.STANDBY_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.STANDBY_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def set_standby_temperature(self, temperature: int, position: int = 1) -> None:
        """Set standby temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.STANDBY_TEMPERATURE: temperatures})

    async def get_target_temperature(self, position: int | None = 1) -> float:
        """Get target temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.TARGET_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def set_target_temperature(self, temperature: int, position: int = 1) -> None:
        """Set target temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.TARGET_TEMPERATURE: temperatures})

    async def get_heat_request(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HotWaterTank.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.HEAT_REQUEST)
        _value: int | str = str(response[_key][_idx]["value"])

        if _value in ["true", "false"]:
            _value = 1 if _value == "true" else 0

        return _value


class HeatPumpEndpoints(BaseEndpoints):
    """Class to retrieve the heat pump data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_name(self, position: int | None = 1) -> str:
        """Get heat pump name."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.NAME,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.NAME)
        return str(response[_key][_idx]["value"])

    async def get_state(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get heat pump state."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.STATE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.STATE)

        try:
            _value: int | str = int(response[_key][_idx]["value"])
        except ValueError:
            _value = str(response[_key][_idx]["value"])

        return _value

    async def get_operating_mode(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.OPERATING_MODE)

        try:
            _value: int | str = int(response[_key][_idx]["value"])
        except ValueError:
            _value = str(response[_key][_idx]["value"])

        return _value

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatPumpOperatingMode[mode.upper()].value
        except KeyError as error:
            msg: str = "Invalid operating mode!"
            raise APIError(msg) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatPump.OPERATING_MODE: modes})

    async def get_circulation_pump(self, position: int | None = 1) -> float:
        """Get circulation pump."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.CIRCULATION_PUMP,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.CIRCULATION_PUMP)
        return float(response[_key][_idx]["value"])

    async def get_flow_temperature(self, position: int | None = 1) -> float:
        """Get flow temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.FLOW_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_return_flow_temperature(self, position: int | None = 1) -> float:
        """Get return flow temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.RETURN_FLOW_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.RETURN_FLOW_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_source_input_temperature(self, position: int | None = 1) -> float:
        """Get source input temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_INPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.SOURCE_INPUT_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_source_output_temperature(self, position: int | None = 1) -> float:
        """Get source output temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.SOURCE_OUTPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.SOURCE_OUTPUT_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_compressor_input_temperature(self, position: int | None = 1) -> float:
        """Get compressor input temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_INPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_INPUT_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_compressor_output_temperature(self, position: int | None = 1) -> float:
        """Get compressor output temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_compressor(self, position: int | None = 1) -> float:
        """Get compressor."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR)
        return float(response[_key][_idx]["value"])

    async def get_high_pressure(self, position: int | None = 1) -> float:
        """Get high pressure in bar."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HIGH_PRESSURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HIGH_PRESSURE)
        return float(response[_key][_idx]["value"])

    async def get_low_pressure(self, position: int | None = 1) -> float:
        """Get low pressure in bar."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.LOW_PRESSURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.LOW_PRESSURE)
        return float(response[_key][_idx]["value"])

    async def get_heat_request(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HEAT_REQUEST)
        _value: int | str = str(response[_key][_idx]["value"])

        if _value in ["true", "false"]:
            _value = 1 if _value == "true" else 0

        return _value

    async def get_compressor_power(self, position: int | None = 1) -> float:
        """Get compressor power."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COMPRESSOR_POWER,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_POWER)
        return float(response[_key][_idx]["value"])

    async def get_heating_power(self, position: int | None = 1) -> float:
        """Get heating power."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HEATING_POWER,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HEATING_POWER)
        return float(response[_key][_idx]["value"])

    async def get_hot_water_power(self, position: int | None = 1) -> float:
        """Get hot water power."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_POWER,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HOT_WATER_POWER)
        return float(response[_key][_idx]["value"])

    async def get_cop(self, position: int | None = 1) -> float:
        """Get COP."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COP,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COP)
        return float(response[_key][_idx]["value"])

    async def get_heating_energy(self, position: int | None = 1) -> float:
        """Get heat energy."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HEATING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HEATING_ENERGY)
        return float(response[_key][_idx]["value"])

    async def get_heating_energy_consumption(self, position: int | None = 1) -> float:
        """Get energy consumption for heating."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HEATING_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HEATING_ENERGY_CONSUMPTION)
        return float(response[_key][_idx]["value"])

    async def get_heating_spf(self, position: int | None = 1) -> float:
        """Get heating SPF."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HEATING_SPF,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HEATING_SPF)
        return float(response[_key][_idx]["value"])

    async def get_cooling_energy(self, position: int | None = 1) -> float:
        """Get cooling energy."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COOLING_ENERGY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COOLING_ENERGY)
        return float(response[_key][_idx]["value"])

    async def get_cooling_energy_consumption(self, position: int | None = 1) -> float:
        """Get cooling energy consumption."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COOLING_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COOLING_ENERGY_CONSUMPTION)
        return float(response[_key][_idx]["value"])

    async def get_cooling_spf(self, position: int | None = 1) -> float:
        """Get cooling SPF."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.COOLING_SPF,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COOLING_SPF)
        return float(response[_key][_idx]["value"])

    async def get_hot_water_energy(self, position: int | None = 1) -> float:
        """Get hot water energy."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_ENERGY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HOT_WATER_ENERGY)
        return float(response[_key][_idx]["value"])

    async def get_hot_water_energy_consumption(self, position: int | None = 1) -> float:
        """Get the hot_water energy consumption."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HOT_WATER_ENERGY_CONSUMPTION)
        return float(response[_key][_idx]["value"])

    async def get_hot_water_spf(self, position: int | None = 1) -> float:
        """Get hot water SPF."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.HOT_WATER_SPF,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HOT_WATER_SPF)
        return float(response[_key][_idx]["value"])

    async def get_total_thermal_energy(self, position: int | None = 1) -> float:
        """Get total thermal energy."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_THERMAL_ENERGY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.TOTAL_THERMAL_ENERGY)
        return float(response[_key][_idx]["value"])

    async def get_total_energy_consumption(self, position: int | None = 1) -> float:
        """Get total energy consumption."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_ENERGY_CONSUMPTION,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.TOTAL_ENERGY_CONSUMPTION)
        return float(response[_key][_idx]["value"])

    async def get_total_spf(self, position: int | None = 1) -> float:
        """Get SPF."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatPump.TOTAL_SPF,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.TOTAL_SPF)
        return float(response[_key][_idx]["value"])


class HeatCircuitEndpoints(BaseEndpoints):
    """Class to send and retrieve the heat pump data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_name(self, position: int | None = 1) -> str:
        """Get heat circuit name."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.NAME,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.NAME)
        return str(response[_key][_idx]["value"])

    async def has_room_temperature(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Has room temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.HAS_ROOM_TEMPERATURE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.HAS_ROOM_TEMPERATURE)
        _value: int | str = str(response[_key][_idx]["value"])

        if _value in ["true", "false"]:
            _value = 1 if _value == "true" else 0

        return _value

    async def get_room_temperature(self, position: int | None = 1) -> float:
        """Get room temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.ROOM_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.ROOM_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def has_room_humidity(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Has room humidity."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.HAS_ROOM_HUMIDITY,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.HAS_ROOM_HUMIDITY)
        _value: int | str = str(response[_key][_idx]["value"])

        if _value in ["true", "false"]:
            _value = 1 if _value == "true" else 0

        return _value

    async def get_room_humidity(self, position: int | None = 1) -> float:
        """Get room humidity."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.ROOM_HUMIDITY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.ROOM_HUMIDITY)
        return float(response[_key][_idx]["value"])

    async def get_dew_point(self, position: int | None = 1) -> float:
        """Get dew point."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.DEW_POINT,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.DEW_POINT)
        return float(response[_key][_idx]["value"])

    async def get_target_temperature(self, position: int | None = 1) -> float:
        """Get target temperature."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.TARGET_TEMPERATURE)
        return float(response[_key][_idx]["value"])

    async def get_target_temperature_day(self, position: int | None = 1) -> float:
        """Get target temperature for the day."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_DAY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.TARGET_TEMPERATURE_DAY)
        return float(response[_key][_idx]["value"])

    async def set_target_temperature_day(self, temperature: int, position: int = 1) -> None:
        """Set target temperature for the day."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_DAY: temperatures})

    async def get_heating_limit_day(self, position: int | None = 1) -> float:
        """Get the heating limit for the day."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_LIMIT_DAY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.HEATING_LIMIT_DAY)
        return float(response[_key][_idx]["value"])

    async def get_target_temperature_night(self, position: int | None = 1) -> float | None:
        """Get target temperature for the night."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_NIGHT,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.TARGET_TEMPERATURE_NIGHT)
        return float(response[_key][_idx]["value"])

    async def set_target_temperature_night(self, temperature: int, position: int = 1) -> None:
        """Set target temperature for the night."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_NIGHT: temperatures})

    async def get_heating_limit_night(self, position: int | None = 1) -> float:
        """Get the heating limit for the night."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.HEATING_LIMIT_NIGHT,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.HEATING_LIMIT_NIGHT)
        return float(response[_key][_idx]["value"])

    async def get_target_temperature_away(self, position: int | None = 1) -> float:
        """Get target temperature when away."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_AWAY,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.TARGET_TEMPERATURE_AWAY)
        return float(response[_key][_idx]["value"])

    async def set_target_temperature_away(self, temperature: int, position: int = 1) -> None:
        """Set target temperature when away."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_AWAY: temperatures})

    async def get_target_temperature_offset(self, position: int | None = 1) -> float:
        """Get target temperature offset."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.TARGET_TEMPERATURE_OFFSET,
            position=position,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.TARGET_TEMPERATURE_OFFSET)
        return float(response[_key][_idx]["value"])

    async def set_target_temperature_offset(self, offset: float, position: int = 1) -> None:
        """Set target temperature offset."""
        offsets: list[float | None] = [offset if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.TARGET_TEMPERATURE_OFFSET: offsets})

    async def get_operating_mode(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get operating mode."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.OPERATING_MODE,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.OPERATING_MODE)

        try:
            _value: int | str = int(response[_key][_idx]["value"])
        except ValueError:
            _value = str(response[_key][_idx]["value"])

        return _value

    async def set_operating_mode(self, mode: int | str, position: int = 1) -> None:
        """Set operating mode."""
        try:
            _mode: int | None = mode if isinstance(mode, int) else HeatCircuitOperatingMode[mode.upper()].value
        except KeyError as error:
            msg: str = "Invalid operating mode!"
            raise APIError(msg) from error

        modes: list[int | None] = [_mode if position == p else None for p in range(1, position + 1)]

        await self._write_values(request={HeatCircuit.OPERATING_MODE: modes})

    async def get_heat_request(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get heat request."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.HEAT_REQUEST)

        try:
            _value: int | str = int(response[_key][_idx]["value"])
        except ValueError:
            _value = str(response[_key][_idx]["value"])

        return _value

    async def get_external_cool_request(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get external cool request."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.EXTERNAL_COOL_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.EXTERNAL_COOL_REQUEST)
        _value: int | str = str(response[_key][_idx]["value"])

        if _value in ["true", "false"]:
            _value = 1 if _value == "true" else 0

        return _value

    async def get_external_heat_request(self, position: int | None = 1, *, human_readable: bool = True) -> int | str:
        """Get external heat request."""
        response: dict[str, list[Value]] = await self._read_data(
            request=HeatCircuit.EXTERNAL_HEAT_REQUEST,
            position=position,
            human_readable=human_readable,
            extra_attributes=True,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.EXTERNAL_HEAT_REQUEST)
        _value: int | str = str(response[_key][_idx]["value"])

        if _value in ["true", "false"]:
            _value = 1 if _value == "true" else 0

        return _value
