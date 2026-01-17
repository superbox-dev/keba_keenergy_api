import json
from typing import Any

from aiohttp import BasicAuth
from aiohttp import ClientSession

from keba_keenergy_api.constants import EndpointPath
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SectionPrefix
from keba_keenergy_api.endpoints import BaseEndpoints
from keba_keenergy_api.endpoints import BufferTankEndpoints
from keba_keenergy_api.endpoints import ExternalHeatSourceEndpoints
from keba_keenergy_api.endpoints import HeatCircuitEndpoints
from keba_keenergy_api.endpoints import HeatPumpEndpoints
from keba_keenergy_api.endpoints import HotWaterTankEndpoints
from keba_keenergy_api.endpoints import PhotovoltaicsEndpoints
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.endpoints import Response
from keba_keenergy_api.endpoints import SolarCircuitEndpoints
from keba_keenergy_api.endpoints import SwitchValveEndpoints
from keba_keenergy_api.endpoints import SystemEndpoints
from keba_keenergy_api.endpoints import Value
from keba_keenergy_api.endpoints import ValueResponse


class KebaKeEnergyAPI(BaseEndpoints):
    """An asynchronous client to interact with KEBA KeEnergy API from the Web HMI."""

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        *,
        ssl: bool = False,
        skip_ssl_verification: bool = False,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize API with host and optionally authentication credentials.

        Parameters
        ----------
        host
            The hostname or IP adress e.g. ap4400.local
        username
            Required for basic auth
        password
            Required for basic auth
        ssl
            Enable https schema for API URLs
        skip_ssl_verification
            Disable SSL verification (required for self-signed certificates)
        session
            Add an aiohttp client session

        Examples
        --------
        >>> client = KebaKeEnergyAPI(
        >>>     host="ap4400.local",
        >>>     username="test",
        >>>     password="test",
        >>>     ssl=True,
        >>>     skip_ssl_verification=True
        >>> )

        """
        self.host: str = host
        self.schema: str = "https" if ssl else "http"

        self.auth: BasicAuth | None = None

        if username and password:
            self.auth = BasicAuth(login=username, password=password, encoding="utf-8")

        self.ssl: bool = ssl
        self.skip_ssl_verification: bool = skip_ssl_verification
        self.session: ClientSession | None = session

        super().__init__(
            base_url=self.device_url,
            auth=self.auth,
            ssl=ssl,
            skip_ssl_verification=skip_ssl_verification,
            session=session,
        )

    @property
    def device_url(self) -> str:
        """Get the device URL.

        Returns
        -------
        str
            e.g. https://ap4400.local

        """
        return f"{self.schema}://{self.host}"

    @property
    def system(self) -> SystemEndpoints:
        """Get the system endpoints."""
        return SystemEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def buffer_tank(self) -> BufferTankEndpoints:
        """Get buffer tank endpoints."""
        return BufferTankEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def hot_water_tank(self) -> HotWaterTankEndpoints:
        """Get hot water tank endpoints."""
        return HotWaterTankEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def heat_pump(self) -> HeatPumpEndpoints:
        """Get heat pump endpoints."""
        return HeatPumpEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def heat_circuit(self) -> HeatCircuitEndpoints:
        """Get heat circuit endpoints."""
        return HeatCircuitEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def solar_circuit(self) -> SolarCircuitEndpoints:
        """Get solar circuit endpoints."""
        return SolarCircuitEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def external_heat_source(self) -> ExternalHeatSourceEndpoints:
        """Get external heat source endpoints."""
        return ExternalHeatSourceEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def switch_valve(self) -> SwitchValveEndpoints:
        """Get switch valve endpoints."""
        return SwitchValveEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def photovoltaics(self) -> PhotovoltaicsEndpoints:
        """Get photovoltaics endpoints."""
        return PhotovoltaicsEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @staticmethod
    def _group_data(response: dict[str, list[list[Value]] | list[Value]], /) -> dict[str, ValueResponse]:  # noqa: C901
        data: dict[str, ValueResponse] = {
            SectionPrefix.SYSTEM.value: {},
            SectionPrefix.BUFFER_TANK.value: {},
            SectionPrefix.HOT_WATER_TANK.value: {},
            SectionPrefix.HEAT_PUMP.value: {},
            SectionPrefix.HEAT_CIRCUIT.value: {},
            SectionPrefix.SOLAR_CIRCUIT.value: {},
            SectionPrefix.EXTERNAL_HEAT_SOURCE.value: {},
            SectionPrefix.SWITCH_VALVE.value: {},
            SectionPrefix.PHOTOVOLTAIC.value: {},
        }

        for key, value in response.items():
            _key: str = ""

            if key.startswith(SectionPrefix.SYSTEM):
                _key = key.lower().replace(f"{SectionPrefix.SYSTEM.value}_", "")
                data[SectionPrefix.SYSTEM][_key] = value[0]
            elif key.startswith(SectionPrefix.BUFFER_TANK):
                _key = key.lower().replace(f"{SectionPrefix.BUFFER_TANK.value}_", "")
                data[SectionPrefix.BUFFER_TANK][_key] = value
            elif key.startswith(SectionPrefix.HOT_WATER_TANK):
                _key = key.lower().replace(f"{SectionPrefix.HOT_WATER_TANK.value}_", "")
                data[SectionPrefix.HOT_WATER_TANK][_key] = value
            elif key.startswith(SectionPrefix.HEAT_PUMP):
                _key = key.lower().replace(f"{SectionPrefix.HEAT_PUMP.value}_", "")
                data[SectionPrefix.HEAT_PUMP][_key] = value
            elif key.startswith(SectionPrefix.HEAT_CIRCUIT):
                _key = key.lower().replace(f"{SectionPrefix.HEAT_CIRCUIT.value}_", "")
                data[SectionPrefix.HEAT_CIRCUIT][_key] = value
            elif key.startswith(SectionPrefix.SOLAR_CIRCUIT):
                _key = key.lower().replace(f"{SectionPrefix.SOLAR_CIRCUIT.value}_", "")
                data[SectionPrefix.SOLAR_CIRCUIT][_key] = value
            elif key.startswith(SectionPrefix.EXTERNAL_HEAT_SOURCE):
                _key = key.lower().replace(f"{SectionPrefix.EXTERNAL_HEAT_SOURCE.value}_", "")
                data[SectionPrefix.EXTERNAL_HEAT_SOURCE][_key] = value
            elif key.startswith(SectionPrefix.SWITCH_VALVE):
                _key = key.lower().replace(f"{SectionPrefix.SWITCH_VALVE.value}_", "")
                data[SectionPrefix.SWITCH_VALVE][_key] = value
            elif key.startswith(SectionPrefix.PHOTOVOLTAIC):
                _key = key.lower().replace(f"{SectionPrefix.PHOTOVOLTAIC.value}_", "")
                data[SectionPrefix.PHOTOVOLTAIC][_key] = value[0]

        return data

    async def read_data(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] | None = None,
        *,
        human_readable: bool = True,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Read multiple data from API with one request.

        Parameters
        ----------
        request
            Section or a list of sections e.g. [BufferTank.NAME, ...]
        position
            The number of the installed devices e.g. number of buffer tanks
        human_readable
            Return a human-readable string
        extra_attributes
            Append the extra attributes to the response

        Examples
        --------
        >>> await client.read_data(
        >>>     request=[
        >>>         HeatCircuit.TARGET_TEMPERATURE,
        >>>         HeatCircuit.TARGET_TEMPERATURE_DAY
        >>>     ]
        >>> )

        Returns
        -------
        dictionary
            A dictionary with section as key and reponse data as value

        """
        if position is None:
            position = await self.system.get_positions()

        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=request,
            position=position,
            human_readable=human_readable,
            extra_attributes=extra_attributes,
        )

        return self._group_data(response)

    async def write_data(self, request: dict[Section, Any]) -> None:
        """Write multiple data to API with one request.

        Parameters
        ----------
        request
            A dictionary with section as key and value to set as a tuple (first index is position 1)

        Examples
        --------
        >>> await client.write_data(
        >>>     request={
        >>>        HeatCircuit.TARGET_TEMPERATURE_DAY: (20, None, 5),
        >>>        HeatCircuit.TARGET_TEMPERATURE_NIGHT: (16,),
        >>>     }
        >>> )

        """
        await self._write_values(request=request)

    async def filter_request(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] | None = None,
    ) -> list[Section]:
        """Return only available section that are supported by the Web HMI software version.

        Parameters
        ----------
        request
            Section or a list of sections e.g. [BufferTank.NAME, ...]
        position
            The number of the installed devices e.g. number of buffer tanks

        Returns
        -------
        request
            A list of sections e.g. [BufferTank.NAME, ...]

        Examples
        --------
        >>> data = await client.filter_request(
        >>>     request=[
        >>>         HeatCircuit.TARGET_TEMPERATURE,
        >>>         HeatCircuit.TARGET_TEMPERATURE_DAY
        >>>     ]
        >>> )

        """
        if position is None:
            position = await self.system.get_positions()

        if not isinstance(request, list):
            request = [request]

        if isinstance(position, int):
            position = [position]

        filtered_sections: list[Section] = []

        payloads = self._generate_read_children_payloads(
            request=request,
            position=position,
        )

        for section, payload in payloads:
            response: Response = await self._post(
                payload=json.dumps(payload),
                endpoint=EndpointPath.READ_VAR_CHILDREN,
            )

            if response[0]["ret"] == "OK" and section not in filtered_sections:
                filtered_sections.append(section)

        return filtered_sections
