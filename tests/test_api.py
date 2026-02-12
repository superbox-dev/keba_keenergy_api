from typing import Any

import pytest
from aiohttp import BasicAuth
from aiohttp import ClientSession
from aiohttp import ServerTimeoutError
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import BufferTank
from keba_keenergy_api.constants import ExternalHeatSource
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import Photovoltaic
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SolarCircuit
from keba_keenergy_api.constants import SwitchValve
from keba_keenergy_api.constants import System
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import AuthenticationError
from keba_keenergy_api.version import TYPE_CHECKING
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

if TYPE_CHECKING:
    from keba_keenergy_api.endpoints import ValueResponse


class TestKebaKeEnergyAPI:
    @pytest.mark.asyncio
    async def test_api(self) -> None:
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
            assert response == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_api_with_session(self) -> None:
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
            assert data == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_api_with_basic_auth(self) -> None:
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
                username="test",
                password="test",  # noqa: S106
            )
            response: float = await client.system.get_outdoor_temperature()

            assert isinstance(response, float)
            assert response == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                auth=BasicAuth(login="test", password="test", encoding="utf-8"),  # noqa: S106
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        (
            "section",
            "position",
            "option_payload",
            "payload",
            "extra_attributes_payload",
            "expected_data",
            "expected_extra_attributes",
            "expected_response",
        ),
        [
            (
                [
                    System.HOT_WATER_TANK_NUMBERS,
                    HotWaterTank.CURRENT_TEMPERATURE,
                    ExternalHeatSource.TARGET_TEMPERATURE,
                    Photovoltaic.TOTAL_ENERGY,
                ],
                1,
                None,
                read_data_payload_1,
                None,
                read_data_expected_data_1,
                None,
                read_data_expected_response_1,
            ),
            (
                [HeatCircuit.TARGET_TEMPERATURE, HeatPump.FLOW_TEMPERATURE],
                [0, 1, 3],
                None,
                read_data_payload_2,
                None,
                read_data_expected_data_2,
                None,
                read_data_expected_response_2,
            ),
            (
                [
                    System.OUTDOOR_TEMPERATURE,
                    HeatCircuit.TARGET_TEMPERATURE,
                    HeatCircuit.HEATING_CURVE,
                    HeatPump.FLOW_TEMPERATURE,
                    ExternalHeatSource.TARGET_TEMPERATURE,
                    SwitchValve.POSITION,
                ],
                None,
                read_data_option_payload_3,
                read_data_payload_3,
                read_data_extra_attributes_payload_3,
                read_data_expected_data_3,
                read_data_expected_extra_attributes_3,
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
                read_data_option_payload_4,
                read_data_payload_4,
                None,
                read_data_expected_data_4,
                None,
                read_data_expected_response_4,
            ),
        ],
    )
    async def test_read_data(
        self,
        section: Section,
        position: int | list[int] | None,
        option_payload: list[dict[str, Any]] | None,
        payload: list[dict[str, Any]],
        extra_attributes_payload: list[dict[str, Any]] | None,
        expected_data: str,
        expected_extra_attributes: str,
        expected_response: dict[str, Any],
    ) -> None:
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
                auth=None,
                ssl=False,
            )

            if expected_extra_attributes:
                mock_keenergy_api.assert_any_call(
                    url="http://mocked-host/var/readWriteVars",
                    data=expected_extra_attributes,
                    method="POST",
                    auth=None,
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
                '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "value": "50"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value", "value": "45"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value", "value": "35"}]',
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
        ],
    )
    async def test_write_data(self, section: dict[Section, Any], expected_data: str) -> None:
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
                auth=None,
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
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload={},
                headers={"Content-Type": "text/html"},
                status=401,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(
                host="mocked-host",
                username="test",
                password="invalid",  # noqa: S106
            )

            with pytest.raises(
                AuthenticationError, match="401 Unauthorized: No permission -- see authorization schemes"
            ):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_api_status_4xx(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload={},
                headers={"Content-Type": "text/html"},
                status=405,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(
                host="mocked-host",
                username="test",
                password="test",  # noqa: S106
            )

            with pytest.raises(
                APIError, match=r"405 Method Not Allowed: Specified method is invalid for this resource - \{}"
            ):
                await client.system.get_outdoor_temperature()

    @pytest.mark.asyncio
    async def test_api_client_error(self) -> None:
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
