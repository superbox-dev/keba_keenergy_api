# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the `KebaKeEnergyAPI` client."""

from typing import TYPE_CHECKING
from typing import Any
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
from aiohttp import ClientSession
from aiohttp import ServerTimeoutError
from aiohttp import encode_basic_auth
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import BufferTank
from keba_keenergy_api.constants import ExternalHeatSource
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import PassiveCooling
from keba_keenergy_api.constants import Photovoltaics
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import SwitchValve
from keba_keenergy_api.constants import System
from keba_keenergy_api.endpoints import HeatCircuitEndpoints
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import APITimeoutError
from keba_keenergy_api.error import AuthenticationError
from keba_keenergy_api.error import InvalidJsonError
from tests.test_api_data import read_data_expected_data_1
from tests.test_api_data import read_data_expected_data_2
from tests.test_api_data import read_data_expected_data_3
from tests.test_api_data import read_data_expected_data_4
from tests.test_api_data import read_data_expected_extra_attributes_3
from tests.test_api_data import read_data_expected_response_1
from tests.test_api_data import read_data_expected_response_2
from tests.test_api_data import read_data_expected_response_3
from tests.test_api_data import read_data_expected_response_4
from tests.test_api_data import read_data_extra_attributes_payload_3
from tests.test_api_data import read_data_option_payload_3
from tests.test_api_data import read_data_option_payload_4
from tests.test_api_data import read_data_payload_1
from tests.test_api_data import read_data_payload_2
from tests.test_api_data import read_data_payload_3
from tests.test_api_data import read_data_payload_4
from tests.test_api_data import read_message_ids_expected_data
from tests.test_api_data import read_message_ids_payload
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_names_payload

LOGIN: str = "test"
INVALID_LOGIN: str = "invalid"

if TYPE_CHECKING:
    from keba_keenergy_api.endpoints import ValueResponse


class TestApi:
    """Tests for `KebaKeEnergyAPI`, its requests and the error handling."""

    @pytest.mark.asyncio
    async def test_api(self) -> None:
        """Test a request with a client that creates its own session."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "10.808357",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: float = await client.system.get_outdoor_temperature()

            assert isinstance(response, float)
            assert response == pytest.approx(10.81)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_api_with_session(self) -> None:
        """Test that a passed session is used and not closed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "10.808357",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            session: ClientSession = ClientSession()
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)
            data: float = await client.system.get_outdoor_temperature()

            assert not session.closed
            await session.close()
            assert session.closed

            assert isinstance(data, float)
            assert data == pytest.approx(10.81)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_api_with_basic_auth(self) -> None:
        """Test that the credentials are sent as basic auth header."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "10.808357",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(
                host="mocked-host",
                username=LOGIN,
                password=LOGIN,
            )
            response: float = await client.system.get_outdoor_temperature()

            assert isinstance(response, float)
            assert response == pytest.approx(10.81)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                headers={
                    "Authorization": encode_basic_auth(LOGIN, LOGIN),
                },
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        (
            "section",
            "position",
            "payloads",
            "expected_requests",
            "expected_response",
        ),
        [
            (
                [
                    System.HOT_WATER_TANK_NUMBERS,
                    HotWaterTank.CURRENT_TEMPERATURE,
                    ExternalHeatSource.TARGET_TEMPERATURE,
                    PassiveCooling.TEMPERATURE,
                    Photovoltaics.TOTAL_ENERGY,
                ],
                1,
                (None, read_data_payload_1, None),
                (read_data_expected_data_1, None),
                read_data_expected_response_1,
            ),
            (
                [HeatCircuit.TARGET_TEMPERATURE, HeatPump.FLOW_TEMPERATURE],
                [0, 1, 3],
                (None, read_data_payload_2, None),
                (read_data_expected_data_2, None),
                read_data_expected_response_2,
            ),
            (
                [
                    System.OUTDOOR_TEMPERATURE,
                    HeatCircuit.TARGET_TEMPERATURE,
                    HeatCircuit.HEATING_CURVE,
                    HeatPump.FLOW_TEMPERATURE,
                    ExternalHeatSource.TARGET_TEMPERATURE,
                    PassiveCooling.TEMPERATURE,
                    SwitchValve.POSITION,
                ],
                None,
                (read_data_option_payload_3, read_data_payload_3, read_data_extra_attributes_payload_3),
                (read_data_expected_data_3, read_data_expected_extra_attributes_3),
                read_data_expected_response_3,
            ),
            (
                [
                    BufferTank.CURRENT_TOP_TEMPERATURE,
                    SolarCircuit.SOURCE_TEMPERATURE,
                    SolarCircuit.CURRENT_TEMPERATURE,
                    SolarCircuit.TARGET_TEMPERATURE,
                    SolarCircuit.HEAT_REQUEST,
                    HeatPump.SUBSTATE,
                ],
                None,
                (read_data_option_payload_4, read_data_payload_4, None),
                (read_data_expected_data_4, None),
                read_data_expected_response_4,
            ),
        ],
    )
    async def test_read_data(
        self,
        section: Section,
        position: int | list[int] | None,
        payloads: tuple[list[dict[str, Any]] | None, list[dict[str, Any]], list[dict[str, Any]] | None],
        expected_requests: tuple[str, str | None],
        expected_response: dict[str, Any],
    ) -> None:
        """Test that `read_data()` returns the values grouped by section."""
        option_payload, payload, extra_attributes_payload = payloads
        expected_data, expected_extra_attributes = expected_requests

        with aioresponses() as mock_keenergy_api:
            if option_payload is not None:
                mock_keenergy_api.post(
                    "http://mocked-host/var/readWriteVars",
                    payload=option_payload,
                    headers={"Content-Type": "application/json;charset=utf-8"},
                )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            if extra_attributes_payload:
                mock_keenergy_api.post(
                    "http://mocked-host/var/readWriteVars",
                    payload=heating_curve_names_payload,
                    headers={"Content-Type": "application/json;charset=utf-8"},
                )

                mock_keenergy_api.post(
                    "http://mocked-host/var/readWriteVars",
                    payload=extra_attributes_payload,
                    headers={"Content-Type": "application/json;charset=utf-8"},
                )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: dict[str, ValueResponse] = await client.read_data(
                request=section,
                position=position,
            )

            assert isinstance(response, dict)
            assert response == expected_response

            mock_keenergy_api.assert_any_call(
                url="http://mocked-host/var/readWriteVars",
                data=expected_data,
                method="POST",
                headers={},
                ssl=False,
            )

            if expected_extra_attributes:
                mock_keenergy_api.assert_any_call(
                    url="http://mocked-host/var/readWriteVars",
                    data=expected_extra_attributes,
                    method="POST",
                    headers={},
                    ssl=False,
                )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("section", "expected_data"),
        [
            (
                {
                    SolarCircuit.TARGET_TEMPERATURE: (
                        50,
                        None,
                        45,
                        35,
                    ),
                },
                (
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "value": "50"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value", "value": "45"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value", "value": "35"}]'
                ),
            ),
            (
                {
                    System.OPERATING_MODE: 1,
                },
                '[{"name": "APPL.CtrlAppl.sParam.param.operatingMode", "value": "1"}]',
            ),
            (
                {
                    HotWaterTank.STANDBY_TEMPERATURE: (10,),
                },
                '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "10"}]',
            ),
            (
                {
                    HotWaterTank.STANDBY_TEMPERATURE: (10,),
                    HotWaterTank.TARGET_TEMPERATURE: (
                        45,
                        44,
                    ),
                    SolarCircuit.PRIORITY_1_BEFORE_2: (
                        0,
                        1,
                    ),
                },
                (
                    "["
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "10"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "value": "45"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[1].param.normalSetTempMax.value", "value": "44"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[0]", "value": "0"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[1]", "value": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.priority", "value": "15"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].param.priority", "value": "14"}]'
                ),
            ),
            (
                {
                    HeatCircuit.TARGET_TEMPERATURE_DAY: 20,
                },
                '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "value": "20"}]',
            ),
            (
                {
                    System.OPERATING_MODE: (2,),
                },
                '[{"name": "APPL.CtrlAppl.sParam.param.operatingMode", "value": "2"}]',
            ),
            (
                {
                    System.OPERATING_MODE: (None,),
                    HeatCircuit.OPERATING_MODE: (2, 3, None, 1),
                },
                (
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "value": "2"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[1].param.operatingMode", "value": "3"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[3].param.operatingMode", "value": "1"}]'
                ),
            ),
            (
                {
                    SolarCircuit.PRIORITY_1_BEFORE_2: 1,
                },
                (
                    '[{"name": "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[0]", "value": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.priority", "value": "14"}]'
                ),
            ),
        ],
    )
    async def test_write_data(self, section: dict[Section, Any], expected_data: str) -> None:
        """Test that `write_data()` sends the values, skips `None` and adds the extra writes."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload=[{}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.write_data(request=section)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=expected_data,
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("section", "position", "repeat", "expected"),
        [
            (BufferTank.NAME, 1, 1, [BufferTank.NAME]),
            (SolarCircuit.PRIORITY_1_BEFORE_2, None, 1, [SolarCircuit.PRIORITY_1_BEFORE_2]),
            (SolarCircuit.HEAT_REQUEST, None, 2, [SolarCircuit.HEAT_REQUEST]),
            (
                [HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE],
                None,
                2,
                [HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE],
            ),
        ],
    )
    async def test_filter_request(
        self,
        section: Section | list[Section],
        position: int | list[int] | None,
        repeat: int,
        expected: list[Section],
    ) -> None:
        """Test that `filter_request()` keeps the sections supported by the control unit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty heat pumps",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty HC",
                            "lowerLimit": "0",
                            "upperLimit": "8",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty solar",
                            "upperLimit": "4",
                            "lowerLimit": "0",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers",
                        "attributes": {
                            "formatId": "fmt2p0",
                            "longText": "Qty buffers",
                            "upperLimit": "0",
                            "lowerLimit": "0",
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty HW tank",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources",
                        "attributes": {
                            "formatId": "fmt2p0",
                            "longText": "Qty ext. heat sources",
                            "upperLimit": "1",
                            "lowerLimit": "0",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves",
                        "attributes": {
                            "formatId": "fmt2p0",
                            "longText": "Qty switch valves",
                            "upperLimit": "0",
                            "lowerLimit": "0",
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                        },
                        "value": "1",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readVarChildren",
                payload={"ret": "OK", "children": []},
                headers={"Content-Type": "application/json;charset=utf-8"},
                repeat=repeat,
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: list[Section] = await client.filter_request(
                request=section,
                position=position,
            )
            assert data == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("section", "expected"),
        [
            (BufferTank.NAME, []),
            (
                [HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE],
                [HotWaterTank.CURRENT_TEMPERATURE],
            ),
        ],
    )
    async def test_filter_request_with_error(self, section: Section | list[Section], expected: list[Section]) -> None:
        """Test that `filter_request()` drops the sections rejected by the control unit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty heat pumps",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty HC",
                            "lowerLimit": "0",
                            "upperLimit": "8",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty solar",
                            "upperLimit": "4",
                            "lowerLimit": "0",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers",
                        "attributes": {
                            "formatId": "fmt2p0",
                            "longText": "Qty buffers",
                            "upperLimit": "0",
                            "lowerLimit": "0",
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty HW tank",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources",
                        "attributes": {
                            "formatId": "fmt2p0",
                            "longText": "Qty ext. heat sources",
                            "upperLimit": "1",
                            "lowerLimit": "0",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves",
                        "attributes": {
                            "formatId": "fmt2p0",
                            "longText": "Qty switch valves",
                            "upperLimit": "0",
                            "lowerLimit": "0",
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                        },
                        "value": "1",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            repeat: int = (len(section) if isinstance(section, list) else 1) - 1

            if repeat:
                mock_keenergy_api.post(
                    "http://mocked-host/var/readVarChildren",
                    payload={"ret": "OK", "children": []},
                    headers={"Content-Type": "application/json;charset=utf-8"},
                    repeat=(len(section) if isinstance(section, list) else 1) - 1,
                )

            mock_keenergy_api.post(
                "http://mocked-host/var/readVarChildren",
                payload={"ret": "ERROR"},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: list[Section] = await client.filter_request(request=section)
            assert data == expected

    @pytest.mark.asyncio
    async def test_invalid_credentials(self) -> None:
        """Test that a `401` response raises `AuthenticationError`."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload={},
                headers={"Content-Type": "text/html"},
                status=401,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(
                host="mocked-host",
                username=LOGIN,
                password=INVALID_LOGIN,
            )

            with pytest.raises(
                AuthenticationError, match="401 Unauthorized: No permission -- see authorization schemes"
            ):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_api_status_4xx(self) -> None:
        """Test that a `405` response raises `APIError`."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload={},
                headers={"Content-Type": "text/html"},
                status=405,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(
                host="mocked-host",
                username=LOGIN,
                password=LOGIN,
            )

            with pytest.raises(
                APIError, match=r"405 Method Not Allowed: Specified method is invalid for this resource - \{}"
            ):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_api_client_error(self) -> None:
        """Test that an `aiohttp` client error raises `APIError`."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                exception=ServerTimeoutError("Server took too long to respond"),
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match="Server took too long to respond"):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_api_error(self) -> None:
        """Test that a `500` response raises `APIError` with the developer message."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload={"developerMessage": "mocked-error"},
                headers={"Content-Type": "application/json;charset=utf-8"},
                status=500,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError, match="500 Internal Server Error: Server got itself in trouble - mocked-error"
            ):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_write_data_ignores_invalid_and_read_only_sections(self) -> None:
        """Test that `write_data()` skips unknown keys and read-only sections."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload=[{}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            request: dict[Any, Any] = {
                "invalid": 1,
                HeatPump.STATE: (1,),
                System.OPERATING_MODE: 1,
            }

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.write_data(request=request)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.param.operatingMode", "value": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_read_message_ids(self) -> None:
        """Test that `read_message_ids()` returns the message ids of all positions."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=read_data_option_payload_4,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=read_message_ids_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: dict[Section, list[int]] = await client.read_message_ids(
                request=[
                    HeatPump.HAS_VFD_FAILURE,
                    HeatCircuit.ROOM_TEMPERATURE,
                    SolarCircuit.CURRENT_TEMPERATURE,
                    System.OUTDOOR_TEMPERATURE,
                    # Has no message id and is skipped
                    HeatPump.STATE,
                ],
            )

            assert data == {
                HeatPump.HAS_VFD_FAILURE: [10, 0],
                HeatCircuit.ROOM_TEMPERATURE: [0],
                SolarCircuit.CURRENT_TEMPERATURE: [0, 10, 10, 0],
                System.OUTDOOR_TEMPERATURE: [0],
            }

            mock_keenergy_api.assert_any_call(
                url="http://mocked-host/var/readWriteVars",
                data=read_message_ids_expected_data,
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_read_message_ids_with_position(self) -> None:
        """Test `read_message_ids()` for a single position."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[1].FailureVFD.state.msgId", "value": "10"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: dict[Section, list[int]] = await client.read_message_ids(request=HeatPump.HAS_VFD_FAILURE, position=2)

            assert data == {HeatPump.HAS_VFD_FAILURE: [10]}

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[1].FailureVFD.state.msgId", "attr": "0"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_read_message_ids_without_message_id(self) -> None:
        """Test that `read_message_ids()` sends no request for sections without a message id."""
        with aioresponses() as mock_keenergy_api:
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: dict[Section, list[int]] = await client.read_message_ids(request=[HeatPump.STATE], position=1)

            assert data == {}
            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_write_data_with_multiple_values_for_system_section(self) -> None:
        """Test that `write_data()` raises `APIError` for more than one value of a system-wide section."""
        with aioresponses() as mock_keenergy_api:
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=r'"APPL\.CtrlAppl\.sParam\.param\.operatingMode" is system wide, only one value can be written!',
            ):
                await client.write_data(request={System.OPERATING_MODE: (1, 2)})

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_write_data_without_writable_sections(self) -> None:
        """Test that `write_data()` sends no request if there is nothing to write."""
        with aioresponses() as mock_keenergy_api:
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.write_data(request={HeatPump.STATE: (1,), HeatCircuit.TARGET_TEMPERATURE_DAY: (None,)})

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_value_with_invalid_position(self) -> None:
        """Test that a getter raises `APIError` for position `0` and sends no request."""
        with aioresponses() as mock_keenergy_api:
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match="Invalid position 0! Positions start at 1"):
                await client.heat_circuit.get_target_temperature_day(position=0)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_set_value_with_position_0_writes_nothing(self) -> None:
        """Test that a setter with position `0` sends no request."""
        with aioresponses() as mock_keenergy_api:
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_temperature_day(20, position=0)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("status", "body", "expected_error"),
        [
            (500, '{"developerMessage": "mocked-error"}', "500 Internal Server Error: .* - mocked-error"),
            (500, "[]", r"500 Internal Server Error: .* - \[]"),
            (500, "<html>Error</html>", "500 Internal Server Error: .* - <html>Error</html>"),
            (
                400,
                '{"developerMessage": "mocked-error"}',
                r'400 Bad Request: .* - \{"developerMessage": "mocked-error"}',
            ),
            (502, "<html>Bad Gateway</html>", "502 Bad Gateway: .* - <html>Bad Gateway</html>"),
            (301, "", "301 Moved Permanently: .*"),
        ],
    )
    async def test_api_error_status(self, status: int, body: str, expected_error: str) -> None:
        """Test that every non-2xx status raises `APIError` with the response body."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                body=body,
                headers={"Content-Type": "text/html"},
                status=status,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match=expected_error):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("body", "content_type"),
        [
            ("not json", "application/json"),
            ("<html></html>", "text/html"),
        ],
    )
    async def test_api_invalid_json(self, body: str, content_type: str) -> None:
        """Test that an invalid JSON response raises `InvalidJsonError`."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                body=body,
                headers={"Content-Type": content_type},
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(InvalidJsonError, match="Invalid JSON response!"):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_api_timeout(self) -> None:
        """Test that a timeout raises `APITimeoutError`, which is also an `APIError` and a `TimeoutError`."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                exception=TimeoutError(),
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APITimeoutError, match="Request timed out!") as error:
                await client.system.get_outdoor_temperature()

            assert isinstance(error.value, APIError)
            assert isinstance(error.value, TimeoutError)

    @pytest.mark.asyncio
    async def test_extra_attributes_with_unknown_heating_curve(self) -> None:
        """Test that `read_data()` adds no points for an unknown heating curve."""
        with (
            aioresponses() as mock_keenergy_api,
            patch.object(HeatCircuitEndpoints, "get_heating_curve_points", AsyncMock(return_value={})),
        ):
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName",
                        "attributes": {},
                        "value": "HC9",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: dict[str, ValueResponse] = await client.read_data(
                request=HeatCircuit.HEATING_CURVE,
                position=1,
            )

        assert response["heat_circuit"] == {"heating_curve": [{"value": "HC9", "attributes": {"points": []}}]}
