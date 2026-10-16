# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Asynchronous client for the KEBA KeEnergy Web HMI API."""

import json
from typing import Any
from typing import TypeVar

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

_E = TypeVar("_E", bound=BaseEndpoints)


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
        ...     host="ap4400.local",
        ...     username="test",
        ...     password="test",
        ...     ssl=True,
        ...     skip_ssl_verification=True
        ... )

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

    def _create_endpoints(self, endpoints: type[_E], /) -> _E:
        """Return an endpoint client with the connection settings of this client."""
        return endpoints(
            base_url=self.device_url,
            auth=self.auth,
            ssl=self.ssl,
            skip_ssl_verification=self.skip_ssl_verification,
            session=self.session,
        )

    @property
    def system(self) -> SystemEndpoints:
        """Return an endpoint client for system-level values."""
        return self._create_endpoints(SystemEndpoints)

    @property
    def buffer_tank(self) -> BufferTankEndpoints:
        """Return an endpoint client for buffer-tank values."""
        return self._create_endpoints(BufferTankEndpoints)

    @property
    def hot_water_tank(self) -> HotWaterTankEndpoints:
        """Return an endpoint client for hot-water-tank values."""
        return self._create_endpoints(HotWaterTankEndpoints)

    @property
    def heat_pump(self) -> HeatPumpEndpoints:
        """Return an endpoint client for heat-pump values."""
        return self._create_endpoints(HeatPumpEndpoints)

    @property
    def heat_circuit(self) -> HeatCircuitEndpoints:
        """Return an endpoint client for heating-circuit values."""
        return self._create_endpoints(HeatCircuitEndpoints)

    @property
    def solar_circuit(self) -> SolarCircuitEndpoints:
        """Return an endpoint client for solar-circuit values."""
        return self._create_endpoints(SolarCircuitEndpoints)

    @property
    def external_heat_source(self) -> ExternalHeatSourceEndpoints:
        """Return an endpoint client for external-heat-source values."""
        return self._create_endpoints(ExternalHeatSourceEndpoints)

    @property
    def switch_valve(self) -> SwitchValveEndpoints:
        """Return an endpoint client for switch-valve values."""
        return self._create_endpoints(SwitchValveEndpoints)

    @property
    def passive_cooling(self) -> PassiveCoolingEndpoints:
        """Return an endpoint client for passive-cooling values."""
        return self._create_endpoints(PassiveCoolingEndpoints)

    @property
    def photovoltaics(self) -> PhotovoltaicsEndpoints:
        """Return an endpoint client for photovoltaic values."""
        return self._create_endpoints(PhotovoltaicsEndpoints)

    async def _group_data(
        self,
        response: dict[str, list[list[Value]] | list[Value]],
        /,
        *,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Group raw API values by their section prefix.

        Parameters
        ----------
        response
            Values returned by :meth:`BaseEndpoints._read_data`, keyed by ``<prefix>_<section name>``.
        extra_attributes
            Whether to enrich heating curve values with their points.

        Returns
        -------
        dict[str, ValueResponse]
            Values grouped by section prefix, with the prefix removed from the keys. System and
            photovoltaics values are single values, all others are lists with one entry per device.

        """
        data: dict[str, ValueResponse] = {prefix.value: {} for prefix in SectionPrefix}
        single_value_prefixes: tuple[SectionPrefix, ...] = (SectionPrefix.SYSTEM, SectionPrefix.PHOTOVOLTAICS)

        for key, value in response.items():
            for prefix in SectionPrefix:
                if not key.startswith(prefix.value):
                    continue

                if prefix is SectionPrefix.HEAT_CIRCUIT and extra_attributes:
                    await self._extra_attributes_heating_curve(key, value)

                _key: str = key.lower().removeprefix(f"{prefix.value}_")
                data[prefix.value][_key] = value[0] if prefix in single_value_prefixes else value
                break

        return data

    async def read_data(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] | None = None,
        *,
        human_readable: bool = True,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Read the requested values with one request and group them by section.

        If no position is given, the installed devices are read from the control unit first
        (one additional request).

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

        Returns
        -------
        dict[str, ValueResponse]
            A dictionary keyed by section prefix, containing the requested values.

        Examples
        --------
        >>> await client.read_data(
        ...     request=[
        ...         HeatCircuit.TARGET_TEMPERATURE,
        ...         HeatCircuit.TARGET_TEMPERATURE_DAY
        ...     ]
        ... )

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

    async def read_message_ids(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] | None = None,
    ) -> dict[Section, list[int]]:
        """Read the message ids of sensors, to find out whether a sensor is in use.

        A message id other than 0 means that the control unit has a message for this sensor,
        e.g. the sensor is not connected. Only sections with a confirmed message id are read,
        all of them with one request.

        Parameters
        ----------
        request
            Section or a list of sections e.g. [HeatPump.HAS_VFD_FAILURE, ...]
        position
            Installed device position(s), such as heat-pump positions.

        Returns
        -------
        dict[Section, list[int]]
            A dictionary with the section as key and a list of message ids as value, one per device
            (position * quantity + sub index). 0 means the sensor is in use.

        Examples
        --------
        >>> await client.read_message_ids(
        ...     request=[HeatPump.HAS_VFD_FAILURE, HeatCircuit.ROOM_TEMPERATURE]
        ... )

        """
        if position is None:
            position = await self.system.get_positions()

        request, position = self._normalize_request(request, position)

        requests: list[tuple[Section, str]] = self._generate_message_id_requests(
            request=request,
            position=position,
        )

        values: list[int] = await self._read_message_ids([path for _, path in requests])

        message_ids: dict[Section, list[int]] = {s: [] for s in request if s.value.message_id_path}

        for (section, _), value in zip(requests, values, strict=True):
            message_ids[section].append(value)

        return message_ids

    async def write_data(self, request: dict[Section, Any]) -> None:
        """Write multiple values with one request.

        **Attention!** Writing values should remain within normal limits, as is the case with typical use of the
        Web HMI. Permanent and very frequent writing of values reduces the lifetime of the built-in flash memory.

        Each key is a section, the value is a single value (position 1) or a tuple with one value per device
        (the first item is position 1, ``None`` skips a device). System-wide sections accept only one value.
        Read-only sections are ignored.

        Parameters
        ----------
        request
            A mapping from section to a value or a tuple of values.

        Raises
        ------
        APIError
            More than one value is given for a system-wide section.

        Examples
        --------
        >>> await client.write_data(
        ...     request={
        ...        HeatCircuit.TARGET_TEMPERATURE_DAY: (20, None, 5),
        ...        HeatCircuit.TARGET_TEMPERATURE_NIGHT: (16,),
        ...     }
        ... )

        """
        await self._write_values(request=request)

    async def filter_request(
        self,
        request: Section | list[Section],
        position: Position | int | list[int] | None = None,
    ) -> list[Section]:
        """Return the requested sections that are supported by the Web HMI software version.

        Each section is checked per installed device with the read-children endpoint (one request
        per section and device). Sections of devices that are not installed are skipped. The result
        keeps the request order and contains each supported section once.

        Parameters
        ----------
        request
            Section or a list of sections e.g. [BufferTank.NAME, ...]
        position
            Installed device position(s), such as buffer-tank positions.

        Returns
        -------
        list[Section]
            The supported sections e.g. [BufferTank.NAME, ...]

        Examples
        --------
        >>> sections = await client.filter_request(
        ...     request=[
        ...         HeatCircuit.TARGET_TEMPERATURE,
        ...         HeatCircuit.TARGET_TEMPERATURE_DAY
        ...     ]
        ... )

        """
        if position is None:
            position = await self.system.get_positions()

        request, position = self._normalize_request(request, position)

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
        """Add the heating curve points to the attributes of heating curve values (in place).

        Parameters
        ----------
        key
            Response key, only ``heat_circuit_heating_curve`` is enriched.
        value
            Values of the key. Each entry gets an attribute ``points`` with ``outdoor`` and ``flow``
            temperatures.

        """
        if key.lower() == self._get_real_key(HeatCircuit.HEATING_CURVE):
            heating_curve_points: HeatingCurves = await self.heat_circuit.get_heating_curve_points()

            for item in value:
                if isinstance(item, dict):
                    item["attributes"]["points"] = [
                        {"outdoor": d[0], "flow": round(d[1], 2)} for d in heating_curve_points.get(item["value"], ())
                    ]
