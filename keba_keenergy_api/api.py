"""Asynchronous client for the KEBA KeEnergy Web HMI API."""

import json
from typing import Any

from aiohttp import ClientSession
from aiohttp import encode_basic_auth

from keba_keenergy_api.constants import EndpointPath
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SectionPrefix
from keba_keenergy_api.endpoints import BaseEndpoints
from keba_keenergy_api.endpoints import BufferTankEndpoints
from keba_keenergy_api.endpoints import ExternalHeatSourceEndpoints
from keba_keenergy_api.endpoints import HeatCircuitEndpoints
from keba_keenergy_api.endpoints import HeatingCurves
from keba_keenergy_api.endpoints import HeatPumpEndpoints
from keba_keenergy_api.endpoints import HotWaterTankEndpoints
from keba_keenergy_api.endpoints import PassiveCoolingEndpoints
from keba_keenergy_api.endpoints import PhotovoltaicsEndpoints
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.endpoints import Response
from keba_keenergy_api.endpoints import SolarCircuitEndpoints
from keba_keenergy_api.endpoints import SwitchValveEndpoints
from keba_keenergy_api.endpoints import SystemEndpoints
from keba_keenergy_api.endpoints import Value
from keba_keenergy_api.endpoints import ValueResponse


class KebaKeEnergyAPI(BaseEndpoints):
    """Asynchronous client for the KEBA KeEnergy Web HMI API.

    The client exposes endpoint groups and convenience methods for reading and writing
    controller values. A caller may provide an existing :class:`aiohttp.ClientSession`
    to manage its own session lifecycle.
    """

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
        """Initialize the API client.

        Configure the device URL, optional HTTP Basic authentication, TLS settings,
        and the optional shared :class:`aiohttp.ClientSession`.

        Parameters
        ----------
        host
            The hostname or IP address, e.g. ``ap4400.local``.
        username
            Username for HTTP Basic authentication.
        password
            Password for HTTP Basic authentication.
        ssl
            Use HTTPS for API URLs.
        skip_ssl_verification
            Disable TLS certificate verification, for example for self-signed certificates.
        session
            Optional session shared with the endpoint clients.

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

        self.auth: str | None = None

        if username and password:
            self.auth = encode_basic_auth(username, password)

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
        """Return the base URL of the KEBA controller.

        Returns
        -------
        str
            e.g. https://ap4400.local

        """
        return f"{self.schema}://{self.host}"

    @property
    def system(self) -> SystemEndpoints:
        """Return an endpoint client for system-level values."""
        return SystemEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def buffer_tank(self) -> BufferTankEndpoints:
        """Return an endpoint client for buffer-tank values."""
        return BufferTankEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def hot_water_tank(self) -> HotWaterTankEndpoints:
        """Return an endpoint client for hot-water-tank values."""
        return HotWaterTankEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def heat_pump(self) -> HeatPumpEndpoints:
        """Return an endpoint client for heat-pump values."""
        return HeatPumpEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def heat_circuit(self) -> HeatCircuitEndpoints:
        """Return an endpoint client for heating-circuit values."""
        return HeatCircuitEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def solar_circuit(self) -> SolarCircuitEndpoints:
        """Return an endpoint client for solar-circuit values."""
        return SolarCircuitEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def external_heat_source(self) -> ExternalHeatSourceEndpoints:
        """Return an endpoint client for external-heat-source values."""
        return ExternalHeatSourceEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def switch_valve(self) -> SwitchValveEndpoints:
        """Return an endpoint client for switch-valve values."""
        return SwitchValveEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def passive_cooling(self) -> PassiveCoolingEndpoints:
        """Return an endpoint client for passive-cooling values."""
        return PassiveCoolingEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def photovoltaics(self) -> PhotovoltaicsEndpoints:
        """Return an endpoint client for photovoltaic values."""
        return PhotovoltaicsEndpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    async def _group_data(  # noqa: C901
        self,
        response: dict[str, list[list[Value]] | list[Value]],
        /,
        *,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Group raw API values by their KEBA section prefix.

        Args:
            response: Raw values returned by the underlying API request.
            extra_attributes: Whether to enrich heating-curve values with point data.

        Returns:
            Values grouped by section, with section prefixes removed from keys.

        """
        data: dict[str, ValueResponse] = {
            SectionPrefix.SYSTEM.value: {},
            SectionPrefix.BUFFER_TANK.value: {},
            SectionPrefix.HOT_WATER_TANK.value: {},
            SectionPrefix.HEAT_PUMP.value: {},
            SectionPrefix.HEAT_CIRCUIT.value: {},
            SectionPrefix.SOLAR_CIRCUIT.value: {},
            SectionPrefix.EXTERNAL_HEAT_SOURCE.value: {},
            SectionPrefix.SWITCH_VALVE.value: {},
            SectionPrefix.PASSIVE_COOLING.value: {},
            SectionPrefix.PHOTOVOLTAICS.value: {},
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

                if extra_attributes:
                    await self._extra_attributes_heating_curve(key, value)

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
            elif key.startswith(SectionPrefix.PASSIVE_COOLING):
                _key = key.lower().replace(f"{SectionPrefix.PASSIVE_COOLING.value}_", "")
                data[SectionPrefix.PASSIVE_COOLING][_key] = value
            elif key.startswith(SectionPrefix.PHOTOVOLTAICS):
                _key = key.lower().replace(f"{SectionPrefix.PHOTOVOLTAICS.value}_", "")
                data[SectionPrefix.PHOTOVOLTAICS][_key] = value[0]

        return data

    async def read_data(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] | None = None,
        *,
        human_readable: bool = True,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Read requested values and group them by section.

        The underlying API request is delegated to :meth:`BaseEndpoints._read_data`.
        If no device positions are supplied, the installed positions are queried first.

        Parameters
        ----------
        request
            Section or a list of sections e.g. [BufferTank.NAME, ...]
        position
            Installed device position(s), such as buffer-tank positions.
        human_readable
            Whether values should be returned as human-readable strings.
        extra_attributes
            Whether to append additional attributes, including heating-curve points.

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
            A dictionary keyed by section prefix, containing the requested values.

        """
        if position is None:
            position = await self.system.get_positions()

        response: dict[str, list[list[Value]] | list[Value]] = await self._read_data(
            request=request,
            position=position,
            human_readable=human_readable,
            extra_attributes=extra_attributes,
        )

        return await self._group_data(response, extra_attributes=extra_attributes)

    async def write_data(self, request: dict[Section, Any]) -> None:
        """Write multiple values to the controller.

        Each mapping key identifies a section. Its value is a tuple of values indexed
        by device position, where the first tuple item corresponds to position 1.

        Parameters
        ----------
        request
            A mapping from section to a tuple of values; the first tuple item targets position 1.

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
        """Return requested sections supported by the controller's Web HMI version.

        Each requested section is checked using the API's read-children endpoint.
        The returned list preserves request order and contains each supported section
        at most once.

        Parameters
        ----------
        request
            Section or a list of sections e.g. [BufferTank.NAME, ...]
        position
            Installed device position(s), such as buffer-tank positions.

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

    async def _extra_attributes_heating_curve(self, key: str, value: list[list[Value]] | list[Value], /) -> None:
        """Add heating-curve points to the attributes of matching response values.

        Args:
            key: Original key returned by the KEBA API.
            value: Values associated with the key. Matching dictionary entries are
                enriched in place with the outdoor-temperature and flow-temperature
                points.

        """
        if key.lower() == self._get_real_key(HeatCircuit.HEATING_CURVE):
            heating_curve_points: HeatingCurves = await self.heat_circuit.get_heating_curve_points()

            for item in value:
                if isinstance(item, dict):
                    item["attributes"]["points"] = [
                        {"outdoor": d[0], "flow": round(d[1], 2)} for d in heating_curve_points[item["value"]]
                    ]
