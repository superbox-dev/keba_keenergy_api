# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the `KebaKeEnergyAPI` client."""

import json
from typing import TYPE_CHECKING
from typing import Any
from unittest.mock import patch

import pytest
from aiohttp import ClientConnectionError
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import ConnectionTimeoutError
from aiohttp import ServerTimeoutError
from aiohttp import SocketTimeoutError
from aiohttp import encode_basic_auth
from aioresponses import aioresponses
from syrupy.assertion import SnapshotAssertion

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
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import APITimeoutError
from keba_keenergy_api.error import AuthenticationError
from keba_keenergy_api.error import InvalidJsonError
from tests.conftest import READ_URL
from tests.conftest import WRITE_URL
from tests.conftest import SentRequests
from tests.test_api_data import positions_payload
from tests.test_api_data import read_data_extra_attributes_payload_3
from tests.test_api_data import read_data_option_payload_3
from tests.test_api_data import read_data_option_payload_4
from tests.test_api_data import read_data_payload_1
from tests.test_api_data import read_data_payload_2
from tests.test_api_data import read_data_payload_3
from tests.test_api_data import read_data_payload_4
from tests.test_api_data import read_message_ids_payload
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_names_payload

LOGIN: str = "test"
INVALID_LOGIN: str = "invalid"

if TYPE_CHECKING:
    from keba_keenergy_api.endpoints import ValueResponse


class TestApi:
    """Tests for `KebaKeEnergyAPI`, its requests and the error handling."""

    async def test_api(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test a request with a client that creates its own session."""
        mock_api.post(
            READ_URL,
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
        )

        response: float = await client.system.get_outdoor_temperature()

        assert isinstance(response, float)
        assert response == pytest.approx(10.81)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
            method="POST",
            headers={},
            ssl=False,
        )

    async def test_api_with_session(self, mock_api: aioresponses) -> None:
        """Test that a passed session is used and not closed."""
        mock_api.post(
            READ_URL,
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
        )

        session: ClientSession = ClientSession()
        client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)
        data: float = await client.system.get_outdoor_temperature()

        assert not session.closed
        await session.close()
        assert session.closed

        assert isinstance(data, float)
        assert data == pytest.approx(10.81)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
            method="POST",
            headers={},
            ssl=False,
        )

    async def test_api_as_context_manager(self, mock_api: aioresponses) -> None:
        """Test that `async with` shares one session between all requests and closes it afterwards."""
        mock_api.post(
            READ_URL,
            payload=[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}],
            repeat=2,
        )

        # The endpoint clients would create a session per request without the shared session
        with patch("keba_keenergy_api.endpoints.ClientSession", side_effect=AssertionError):
            async with KebaKeEnergyAPI(host="mocked-host") as client:
                session: ClientSession | None = client.session

                assert isinstance(session, ClientSession)
                assert await client.system.get_outdoor_temperature() == pytest.approx(10.81)
                assert await client.system.get_outdoor_temperature() == pytest.approx(10.81)

        assert session.closed
        assert client.session is None

    async def test_api_after_context_manager(self, mock_api: aioresponses) -> None:
        """Test that an endpoint client used after `async with` closes the session it opens per request."""
        mock_api.post(
            READ_URL,
            payload=[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}],
        )

        async with KebaKeEnergyAPI(host="mocked-host") as client:
            system = client.system

        sessions: list[ClientSession] = []

        def create_session(*, timeout: ClientTimeout) -> ClientSession:
            sessions.append(ClientSession(timeout=timeout))
            return sessions[-1]

        with patch("keba_keenergy_api.endpoints.ClientSession", side_effect=create_session):
            assert await system.get_outdoor_temperature() == pytest.approx(10.81)

        assert len(sessions) == 1
        assert sessions[0].closed

    async def test_api_as_context_manager_with_session(self) -> None:
        """Test that `async with` keeps a passed session open."""
        async with ClientSession() as session:
            async with KebaKeEnergyAPI(host="mocked-host", session=session) as client:
                assert client.session is session

            assert not session.closed
            assert client.session is session

    async def test_close_without_context_manager(self, client: KebaKeEnergyAPI) -> None:
        """Test that `close()` does nothing if no session was opened by the client."""
        await client.close()

        assert client.session is None

    async def test_api_with_basic_auth(self, mock_api: aioresponses) -> None:
        """Test that the credentials are sent as basic auth header."""
        mock_api.post(
            READ_URL,
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
        )

        client: KebaKeEnergyAPI = KebaKeEnergyAPI(
            host="mocked-host",
            username=LOGIN,
            password=LOGIN,
        )
        response: float = await client.system.get_outdoor_temperature()

        assert isinstance(response, float)
        assert response == pytest.approx(10.81)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
            method="POST",
            headers={
                "Authorization": encode_basic_auth(LOGIN, LOGIN),
            },
            ssl=False,
        )

    @pytest.mark.parametrize(
        (
            "section",
            "position",
            "payloads",
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
            ),
            (
                [HeatCircuit.TARGET_TEMPERATURE, HeatPump.FLOW_TEMPERATURE],
                [0, 1, 3],
                (None, read_data_payload_2, None),
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
            ),
        ],
        ids=["position", "positions", "options-and-extra-attributes", "options"],
    )
    async def test_read_data(
        self,
        mock_api: aioresponses,
        section: Section,
        position: int | list[int] | None,
        payloads: tuple[list[dict[str, Any]] | None, list[dict[str, Any]], list[dict[str, Any]] | None],
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `read_data()` returns the values grouped by section."""
        option_payload, payload, extra_attributes_payload = payloads

        if option_payload is not None:
            mock_api.post(
                READ_URL,
                payload=option_payload,
            )

        mock_api.post(
            READ_URL,
            payload=payload,
        )

        if extra_attributes_payload:
            mock_api.post(
                READ_URL,
                payload=heating_curve_names_payload,
            )

            mock_api.post(
                READ_URL,
                payload=extra_attributes_payload,
            )

        client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
        response: dict[str, ValueResponse] = await client.read_data(
            request=section,
            position=position,
        )

        assert response == snapshot(name="response")
        assert sent_requests(mock_api) == snapshot(name="requests")

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
    async def test_write_data(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, section: dict[Section, Any], expected_data: str
    ) -> None:
        """Test that `write_data()` sends the values, skips `None` and adds the extra writes."""
        mock_api.post(
            WRITE_URL,
            payload=[{}],
        )

        await client.write_data(request=section)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=expected_data,
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize(
        ("section", "position", "expected"),
        [
            (BufferTank.NAME, 1, [BufferTank.NAME]),
            (SolarCircuit.PRIORITY_1_BEFORE_2, None, [SolarCircuit.PRIORITY_1_BEFORE_2]),
            (SolarCircuit.HEAT_REQUEST, None, [SolarCircuit.HEAT_REQUEST]),
            (
                [HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE, HotWaterTank.CURRENT_TEMPERATURE],
                None,
                [HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE],
            ),
        ],
        ids=["position", "system-wide", "quantity", "duplicate-sections"],
    )
    async def test_filter_request(
        self,
        mock_api: aioresponses,
        section: Section | list[Section],
        position: int | None,
        expected: list[Section],
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `filter_request()` checks all variables with one read request."""
        if position is None:
            mock_api.post(
                READ_URL,
                payload=positions_payload,
            )

        mock_api.post(
            READ_URL,
            payload=[],
        )

        client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
        data: list[Section] = await client.filter_request(request=section, position=position)

        assert data == expected
        assert sent_requests(mock_api) == snapshot(name="requests")

    @pytest.mark.parametrize(
        ("section", "unknown", "expected"),
        [
            (BufferTank.NAME, ["APPL.CtrlAppl.sParam.bufferTank[0].param.name"], []),
            (
                [HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE, BufferTank.NAME],
                [
                    "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState",
                    "APPL.CtrlAppl.sParam.bufferTank[0].param.name",
                ],
                [HotWaterTank.CURRENT_TEMPERATURE],
            ),
        ],
        ids=["all-unknown", "some-unknown"],
    )
    async def test_filter_request_with_unknown_variables(
        self,
        mock_api: aioresponses,
        section: Section | list[Section],
        unknown: list[str],
        expected: list[Section],
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `filter_request()` drops each variable the control unit rejects and reads the rest again."""
        for name in unknown:
            mock_api.post(
                READ_URL,
                status=500,
                body=json.dumps({"developerMessage": f"Reading variable: {name} failed (-1)", "status": 500}),
            )

        mock_api.post(
            READ_URL,
            payload=[],
        )

        client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
        data: list[Section] = await client.filter_request(request=section, position=1)

        assert data == expected
        assert sent_requests(mock_api) == snapshot(name="requests")

    @pytest.mark.parametrize(
        ("status", "body", "expected_error"),
        [
            (503, "Service Unavailable", "503 Service Unavailable"),
            (500, json.dumps({"developerMessage": "Unexpected error", "status": 500}), "Unexpected error"),
            (
                500,
                json.dumps({"developerMessage": "Reading variable: APPL.CtrlAppl.sParam.notRequested failed (-1)"}),
                "notRequested",
            ),
        ],
        ids=["other-status", "unknown-message", "variable-not-requested"],
    )
    async def test_filter_request_with_api_error(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, status: int, body: str, expected_error: str
    ) -> None:
        """Test that `filter_request()` raises errors that do not name a requested variable."""
        mock_api.post(READ_URL, status=status, body=body)

        with pytest.raises(APIError, match=expected_error):
            await client.filter_request(request=[HotWaterTank.CURRENT_TEMPERATURE, HeatPump.STATE], position=1)

    async def test_filter_request_without_sections(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test that `filter_request()` sends no request for an empty request."""
        assert await client.filter_request(request=[], position=1) == []
        mock_api.assert_not_called()

    async def test_positions_are_read_once(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, sent_requests: SentRequests
    ) -> None:
        """Test that the installed devices are read on the first call only and reused afterwards."""
        mock_api.post(
            READ_URL,
            payload=positions_payload,
        )
        mock_api.post(
            READ_URL,
            payload=[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "13.5"}],
            repeat=2,
        )
        mock_api.post(
            READ_URL,
            payload=[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.state.msgId", "value": "0"}],
        )

        for _ in range(2):
            response: dict[str, ValueResponse] = await client.read_data(request=System.OUTDOOR_TEMPERATURE)
            assert response["system"] == {"outdoor_temperature": {"value": 13.5, "attributes": {}}}

        assert await client.read_message_ids(request=System.OUTDOOR_TEMPERATURE) == {
            System.OUTDOOR_TEMPERATURE: [0],
        }

        # One request for the positions, two for the values and one for the message ids
        assert [request["data"][0]["name"] for request in sent_requests(mock_api)] == [
            "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
            "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
            "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
            "APPL.CtrlAppl.sParam.outdoorTemp.state.msgId",
        ]

    async def test_invalid_credentials(self, mock_api: aioresponses) -> None:
        """Test that a `401` response raises `AuthenticationError`."""
        mock_api.post(
            READ_URL,
            payload={},
            headers={"Content-Type": "text/html"},
            status=401,
        )
        client: KebaKeEnergyAPI = KebaKeEnergyAPI(
            host="mocked-host",
            username=LOGIN,
            password=INVALID_LOGIN,
        )

        with pytest.raises(AuthenticationError, match="401 Unauthorized: No permission -- see authorization schemes"):
            await client.system.get_outdoor_temperature()

    async def test_api_status_4xx(self, mock_api: aioresponses) -> None:
        """Test that a `405` response raises `APIError`."""
        mock_api.post(
            READ_URL,
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

    async def test_api_client_error(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test that an `aiohttp` client error raises `APIError`."""
        mock_api.post(
            READ_URL,
            exception=ClientConnectionError("mocked-error"),
        )

        with pytest.raises(APIError, match="mocked-error") as error:
            await client.system.get_outdoor_temperature()

        assert not isinstance(error.value, APITimeoutError)

    async def test_api_error(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test that a `500` response raises `APIError` with the developer message."""
        mock_api.post(
            READ_URL,
            payload={"developerMessage": "mocked-error"},
            status=500,
        )

        with pytest.raises(APIError, match="500 Internal Server Error: Server got itself in trouble - mocked-error"):
            await client.system.get_outdoor_temperature()

    async def test_write_data_ignores_invalid_and_read_only_sections(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses
    ) -> None:
        """Test that `write_data()` skips unknown keys and read-only sections."""
        mock_api.post(
            WRITE_URL,
            payload=[{}],
        )

        request: dict[Any, Any] = {
            "invalid": 1,
            HeatPump.STATE: (1,),
            System.OPERATING_MODE: 1,
        }

        await client.write_data(request=request)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data='[{"name": "APPL.CtrlAppl.sParam.param.operatingMode", "value": "1"}]',
            method="POST",
            headers={},
            ssl=False,
        )

    async def test_read_message_ids(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, snapshot: SnapshotAssertion, sent_requests: SentRequests
    ) -> None:
        """Test that `read_message_ids()` returns the message ids of all positions."""
        mock_api.post(
            READ_URL,
            payload=read_data_option_payload_4,
        )
        mock_api.post(
            READ_URL,
            payload=read_message_ids_payload,
        )

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

        assert sent_requests(mock_api) == snapshot

    async def test_read_message_ids_with_position(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test `read_message_ids()` for a single position."""
        mock_api.post(
            READ_URL,
            payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[1].FailureVFD.state.msgId", "value": "10"}],
        )

        data: dict[Section, list[int]] = await client.read_message_ids(request=HeatPump.HAS_VFD_FAILURE, position=2)

        assert data == {HeatPump.HAS_VFD_FAILURE: [10]}

        mock_api.assert_called_once_with(
            url=READ_URL,
            data='[{"name": "APPL.CtrlAppl.sParam.heatpump[1].FailureVFD.state.msgId", "attr": "0"}]',
            method="POST",
            headers={},
            ssl=False,
        )

    async def test_read_message_ids_without_message_id(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test that `read_message_ids()` sends no request for sections without a message id."""
        data: dict[Section, list[int]] = await client.read_message_ids(request=[HeatPump.STATE], position=1)

        assert data == {}
        mock_api.assert_not_called()

    async def test_write_data_with_multiple_values_for_system_section(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses
    ) -> None:
        """Test that `write_data()` raises `APIError` for more than one value of a system-wide section."""
        with pytest.raises(
            APIError,
            match=r'"APPL\.CtrlAppl\.sParam\.param\.operatingMode" is system wide, only one value can be written!',
        ):
            await client.write_data(request={System.OPERATING_MODE: (1, 2)})

        mock_api.assert_not_called()

    async def test_write_data_without_writable_sections(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test that `write_data()` sends no request if there is nothing to write."""
        await client.write_data(request={HeatPump.STATE: (1,), HeatCircuit.TARGET_TEMPERATURE_DAY: (None,)})

        mock_api.assert_not_called()

    async def test_get_value_with_invalid_position(self, client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
        """Test that a getter raises `APIError` for position `0` and sends no request."""
        with pytest.raises(APIError, match="Invalid position 0! Positions start at 1"):
            await client.heat_circuit.get_target_temperature_day(position=0)

        mock_api.assert_not_called()

    async def test_set_value_with_position_0_writes_nothing(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses
    ) -> None:
        """Test that a setter with position `0` sends no request."""
        await client.heat_circuit.set_target_temperature_day(20, position=0)

        mock_api.assert_not_called()

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
    async def test_api_error_status(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, status: int, body: str, expected_error: str
    ) -> None:
        """Test that every non-2xx status raises `APIError` with the response body."""
        mock_api.post(
            READ_URL,
            body=body,
            headers={"Content-Type": "text/html"},
            status=status,
        )

        with pytest.raises(APIError, match=expected_error):
            await client.system.get_outdoor_temperature()

    @pytest.mark.parametrize(
        ("body", "content_type"),
        [
            ("not json", "application/json"),
            ("<html></html>", "text/html"),
        ],
    )
    async def test_api_invalid_json(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, body: str, content_type: str
    ) -> None:
        """Test that an invalid JSON response raises `InvalidJsonError`."""
        mock_api.post(
            READ_URL,
            body=body,
            headers={"Content-Type": content_type},
        )

        with pytest.raises(InvalidJsonError, match="Invalid JSON response!"):
            await client.system.get_outdoor_temperature()

    @pytest.mark.parametrize(
        ("exception", "expected_message"),
        [
            (TimeoutError(), "^Request timed out!$"),
            (ServerTimeoutError("mocked-error"), "^Request timed out! mocked-error$"),
            (ConnectionTimeoutError("mocked-error"), "^Request timed out! mocked-error$"),
            (SocketTimeoutError("mocked-error"), "^Request timed out! mocked-error$"),
        ],
    )
    async def test_api_timeout(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, exception: TimeoutError, expected_message: str
    ) -> None:
        """Test that a timeout raises `APITimeoutError`, which is also an `APIError` and a `TimeoutError`.

        The timeouts of `aiohttp` are also a `ClientError` and must not be raised as a plain `APIError`.

        Parameters
        ----------
        client
            Client for the mocked host.
        mock_api
            Mock for the requests.
        exception
            The timeout raised by the request.
        expected_message
            The expected error message.

        """
        mock_api.post(
            READ_URL,
            exception=exception,
        )

        with pytest.raises(APITimeoutError, match=expected_message) as error:
            await client.system.get_outdoor_temperature()

        assert isinstance(error.value, APIError)
        assert isinstance(error.value, TimeoutError)

    async def test_extra_attributes_with_unknown_heating_curve(
        self, client: KebaKeEnergyAPI, mock_api: aioresponses, sent_requests: SentRequests
    ) -> None:
        """Test that `read_data()` adds no points and reads none for an unknown heating curve."""
        mock_api.post(
            READ_URL,
            payload=[
                {
                    "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName",
                    "attributes": {},
                    "value": "HC9",
                },
            ],
        )

        mock_api.post(
            READ_URL,
            payload=heating_curve_names_payload,
        )

        response: dict[str, ValueResponse] = await client.read_data(
            request=HeatCircuit.HEATING_CURVE,
            position=1,
        )

        # One request for the values and one for the heating curve names, none for the points
        assert [request["data"][0]["name"] for request in sent_requests(mock_api)] == [
            "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName",
            "APPL.CtrlAppl.sParam.linTabPool[0].name",
        ]

        assert response["heat_circuit"] == {"heating_curve": [{"value": "HC9", "attributes": {"points": []}}]}
