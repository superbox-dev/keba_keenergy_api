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

from keba_keenergy_api.client import KebaKeEnergyAPI
from keba_keenergy_api.enums import BufferTankOperatingMode
from keba_keenergy_api.enums import HeatingCircuitOperatingMode
from keba_keenergy_api.enums import MessageIdKind
from keba_keenergy_api.enums import SystemOperatingMode
from keba_keenergy_api.exceptions import APIError
from keba_keenergy_api.exceptions import APITimeoutError
from keba_keenergy_api.exceptions import AuthenticationError
from keba_keenergy_api.exceptions import InvalidResponseError
from keba_keenergy_api.exceptions import UnsupportedVariableError
from keba_keenergy_api.models import CurvePoint
from keba_keenergy_api.models import CurveTable
from keba_keenergy_api.models import DeviceCounts
from keba_keenergy_api.models import Limits
from keba_keenergy_api.models import MessageId
from keba_keenergy_api.models import Reading
from keba_keenergy_api.models import Readings
from keba_keenergy_api.models import WriteValue
from keba_keenergy_api.sections import BufferTank
from keba_keenergy_api.sections import DHWTank
from keba_keenergy_api.sections import HeatingCircuit
from keba_keenergy_api.sections import HeatPump
from keba_keenergy_api.sections import Section
from keba_keenergy_api.sections import SolarCircuit
from keba_keenergy_api.sections import System
from tests.conftest import READ_URL
from tests.conftest import TIMEOUT
from tests.conftest import WRITE_URL
from tests.conftest import SentRequests
from tests.test_client_data import CURVE_TABLE_MAX_POINTS
from tests.test_client_data import CURVE_TABLE_NAMES_RESPONSE
from tests.test_client_data import CURVE_TABLE_POINTS
from tests.test_client_data import DEVICE_COUNTS_RESPONSE
from tests.test_client_data import FILTER_COUNTS
from tests.test_client_data import LOGIN
from tests.test_client_data import READ_RESPONSE
from tests.test_client_data import READ_SECTIONS
from tests.test_client_data import READ_WITH_MESSAGE_IDS_RESPONSE
from tests.test_client_data import READ_WITHOUT_UNKNOWN_MESSAGE_ID_RESPONSE
from tests.test_client_data import TIMEZONE_RESPONSE
from tests.test_client_data import UNKNOWN_MESSAGE_ID
from tests.test_client_data import curve_table_response

if TYPE_CHECKING:
    from aioresponses import aioresponses
    from syrupy.assertion import SnapshotAssertion

TIMEZONE_URL = "http://mocked-host/dateTime?action=getTimeZone"


async def test_client_creates_own_session(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that the client opens one session for all requests and closes it with `close()`."""
    mock_api.post(TIMEZONE_URL, payload=TIMEZONE_RESPONSE, repeat=True)
    sessions: list[ClientSession] = []

    def create_session(*, timeout: ClientTimeout) -> ClientSession:
        sessions.append(ClientSession(timeout=timeout))
        return sessions[-1]

    with patch("keba_keenergy_api.client.ClientSession", side_effect=create_session):
        assert await client.get_timezone() == "Europe/Vienna"
        assert await client.get_timezone() == "Europe/Vienna"
        await client.close()

        assert len(sessions) == 1
        assert sessions[0].closed

        # A request after close() opens a new session.
        assert await client.get_timezone() == "Europe/Vienna"
        await client.close()

    assert [session.closed for session in sessions] == [True, True]
    mock_api.assert_called_with(url=TIMEZONE_URL, method="POST", headers={}, ssl=False, data=None, timeout=TIMEOUT)


async def test_client_uses_passed_session(mock_api: aioresponses) -> None:
    """Test that a passed session is used and not closed, also not by `async with`."""
    mock_api.post(TIMEZONE_URL, payload=TIMEZONE_RESPONSE)

    async with ClientSession() as session:
        with patch("keba_keenergy_api.client.ClientSession", side_effect=AssertionError):
            async with KebaKeEnergyAPI(host="mocked-host", session=session) as client:
                assert await client.get_timezone() == "Europe/Vienna"

        assert not session.closed


async def test_context_manager_closes_own_session(mock_api: aioresponses) -> None:
    """Test that `async with` closes the session opened by the client."""
    mock_api.post(TIMEZONE_URL, payload=TIMEZONE_RESPONSE)
    sessions: list[ClientSession] = []

    def create_session(*, timeout: ClientTimeout) -> ClientSession:
        sessions.append(ClientSession(timeout=timeout))
        return sessions[-1]

    with patch("keba_keenergy_api.client.ClientSession", side_effect=create_session):
        async with KebaKeEnergyAPI(host="mocked-host") as client:
            assert await client.get_timezone() == "Europe/Vienna"

    assert len(sessions) == 1
    assert sessions[0].closed


async def test_close_without_session(client: KebaKeEnergyAPI) -> None:
    """Test that `close()` does nothing if the client opened no session."""
    await client.close()


async def test_request_closed_session(mock_api: aioresponses) -> None:
    """Test that a closed passed session raises `APIError` without a request."""
    session: ClientSession = ClientSession()
    await session.close()
    client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)

    with pytest.raises(APIError, match=r"^The session is closed$"):
        await client.get_timezone()

    mock_api.assert_not_called()


@pytest.mark.parametrize(
    ("verify_ssl", "expected_ssl"),
    [(True, True), (False, False)],
    ids=["verify_ssl", "skip_ssl_verification"],
)
async def test_request_https_and_basic_auth(mock_api: aioresponses, *, verify_ssl: bool, expected_ssl: bool) -> None:
    """Test a request with HTTPS and HTTP Basic authentication."""
    url: str = "https://mocked-host/dateTime?action=getTimeZone"
    mock_api.post(url, payload=TIMEZONE_RESPONSE)
    client: KebaKeEnergyAPI = KebaKeEnergyAPI(
        host="mocked-host", username=LOGIN, password=LOGIN, ssl=True, verify_ssl=verify_ssl
    )

    assert client.device_url == "https://mocked-host"
    assert await client.get_timezone() == "Europe/Vienna"
    await client.close()

    mock_api.assert_called_once_with(
        url=url,
        method="POST",
        headers={"Authorization": encode_basic_auth(LOGIN, LOGIN)},
        ssl=expected_ssl,
        data=None,
        timeout=TIMEOUT,
    )


async def test_request_invalid_credentials(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that a `401` response raises `AuthenticationError`."""
    mock_api.post(TIMEZONE_URL, status=401)

    with pytest.raises(AuthenticationError, match=r"^401 Unauthorized: No permission -- see authorization schemes$"):
        await client.get_timezone()

    await client.close()


@pytest.mark.parametrize(
    ("status", "body", "expected_error"),
    [
        (500, '{"developerMessage": "mocked-error"}', "^500 Internal Server Error: .* - mocked-error$"),
        (500, "[]", r"^500 Internal Server Error: .* - \[]$"),
        (500, "<html>Error</html>", "^500 Internal Server Error: .* - <html>Error</html>$"),
        (400, '{"developerMessage": "mocked-error"}', r'^400 Bad Request: .* - \{"developerMessage": "mocked-error"}$'),
        (502, "<html>Bad Gateway</html>", "^502 Bad Gateway: .* - <html>Bad Gateway</html>$"),
        (301, "", "^301 Moved Permanently: .*$"),
    ],
    ids=["json_message", "json_list", "html", "bad_request", "bad_gateway", "redirect"],
)
async def test_request_error_status(
    client: KebaKeEnergyAPI, mock_api: aioresponses, status: int, body: str, expected_error: str
) -> None:
    """Test that every non-2xx status raises `APIError` with the response body or the developer message."""
    mock_api.post(TIMEZONE_URL, body=body, headers={"Content-Type": "text/html"}, status=status)

    with pytest.raises(APIError, match=expected_error) as error:
        await client.get_timezone()

    assert type(error.value) is APIError
    await client.close()


async def test_request_unsupported_variable(
    client: KebaKeEnergyAPI, mock_api: aioresponses, counts: DeviceCounts
) -> None:
    """Test that a rejected variable raises `UnsupportedVariableError` with the variable name."""
    variable: str = "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue"
    mock_api.post(
        READ_URL,
        status=500,
        body=json.dumps({"developerMessage": f"Reading variable: {variable} failed (-1)", "status": 500}),
    )

    with pytest.raises(UnsupportedVariableError, match=r"^500 Internal Server Error: .* - Reading variable: ") as error:
        await client.read([System.OUTDOOR_TEMPERATURE], counts=counts)

    assert error.value.variable == variable

    await client.close()


async def test_request_client_error(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that an `aiohttp` client error raises `APIError`."""
    mock_api.post(TIMEZONE_URL, exception=ClientConnectionError("mocked-error"))

    with pytest.raises(APIError, match=r"^mocked-error$") as error:
        await client.get_timezone()

    assert not isinstance(error.value, APITimeoutError)
    await client.close()


@pytest.mark.parametrize(
    ("body", "content_type"),
    [("not json", "application/json"), ("<html></html>", "text/html")],
    ids=["invalid_json", "html"],
)
async def test_request_invalid_json(
    client: KebaKeEnergyAPI, mock_api: aioresponses, body: str, content_type: str
) -> None:
    """Test that an invalid JSON response raises `InvalidResponseError`."""
    mock_api.post(TIMEZONE_URL, body=body, headers={"Content-Type": content_type})

    with pytest.raises(InvalidResponseError, match=r"^Invalid JSON response!"):
        await client.get_timezone()

    await client.close()


@pytest.mark.parametrize(
    ("exception", "expected_message"),
    [
        (TimeoutError(), "^Request timed out!$"),
        (ServerTimeoutError("mocked-error"), "^Request timed out! mocked-error$"),
        (ConnectionTimeoutError("mocked-error"), "^Request timed out! mocked-error$"),
        (SocketTimeoutError("mocked-error"), "^Request timed out! mocked-error$"),
    ],
    ids=["timeout", "server_timeout", "connection_timeout", "socket_timeout"],
)
async def test_request_timeout(
    client: KebaKeEnergyAPI, mock_api: aioresponses, exception: TimeoutError, expected_message: str
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
    mock_api.post(TIMEZONE_URL, exception=exception)

    with pytest.raises(APITimeoutError, match=expected_message) as error:
        await client.get_timezone()

    assert isinstance(error.value, TimeoutError)
    await client.close()


async def test_get_device_counts(client: KebaKeEnergyAPI, mock_api: aioresponses, counts: DeviceCounts) -> None:
    """Test that the device counts are read once."""
    mock_api.post(READ_URL, payload=DEVICE_COUNTS_RESPONSE)

    assert await client.get_device_counts() == counts
    assert await client.get_device_counts() == counts

    mock_api.assert_called_once()
    await client.close()


@pytest.mark.parametrize(
    ("method", "endpoint", "payload", "expected"),
    [
        (
            "get_system_info",
            "swupdate?action=getSystemInstalled",
            [{"ret": "OK", "name": "KeEnergy.MTec", "version": "2.2.2"}],
            {"name": "KeEnergy.MTec", "version": "2.2.2"},
        ),
        (
            "get_system_info",
            "swupdate?action=getSystemInstalled",
            [{"name": "KeEnergy.MTec"}],
            {"name": "KeEnergy.MTec"},
        ),
        (
            "get_hmi_info",
            "swupdate?action=getHmiInstalled",
            {"ret": "OK", "name": "KeEnergy.WebHmi_2.2.0.0"},
            {"name": "KeEnergy.WebHmi_2.2.0.0"},
        ),
        (
            "get_device_info",
            "deviceControl?action=getDeviceInfo",
            [{"ret": "OK", "revNo": 2, "orderNo": 12345678, "serNo": 12345678, "name": "MOCKED-NAME", "variantNo": 0}],
            {"revNo": 2, "orderNo": 12345678, "serNo": 12345678, "name": "MOCKED-NAME", "variantNo": 0},
        ),
        ("get_timezone", "dateTime?action=getTimeZone", TIMEZONE_RESPONSE, "Europe/Vienna"),
    ],
    ids=["get_system_info", "get_system_info_without_version", "get_hmi_info", "get_device_info", "get_timezone"],
)
async def test_get_info(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    endpoint: str,
    payload: dict[str, Any] | list[dict[str, Any]],
    expected: dict[str, Any] | str,
) -> None:
    """Test that the info methods return the known keys of the response."""
    mock_api.post(f"http://mocked-host/{endpoint}", payload=payload)

    assert await getattr(client, method)() == expected

    await client.close()


async def test_read(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `read()` reads the device counts first and converts the values to the endpoint types."""
    mock_api.post(READ_URL, payload=DEVICE_COUNTS_RESPONSE)
    mock_api.post(READ_URL, payload=READ_RESPONSE)

    readings: Readings = await client.read(READ_SECTIONS)

    assert readings == snapshot(name="readings")
    assert readings[System.OPERATING_MODE][0].value is SystemOperatingMode.AUTO
    assert readings[HeatingCircuit.PUMP_ACTIVE][0].value is True
    assert sent_requests(mock_api) == snapshot(name="requests")
    await client.close()


async def test_read_without_variables(client: KebaKeEnergyAPI, mock_api: aioresponses, counts: DeviceCounts) -> None:
    """Test that `read()` sends no request if no device of the sections is installed."""
    assert await client.read([BufferTank.TOP_TEMPERATURE], counts=counts) == {BufferTank.TOP_TEMPERATURE: []}
    mock_api.assert_not_called()


@pytest.mark.parametrize(
    ("limits", "expected_attrs"),
    [
        ("all", ["1", "1"]),
        ("none", ["0", "0"]),
        ("read_only", ["1", "0"]),
        ("writable", ["0", "1"]),
    ],
    ids=["all", "none", "read_only", "writable"],
)
async def test_read_limits(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    counts: DeviceCounts,
    sent_requests: SentRequests,
    limits: Limits,
    expected_attrs: list[str],
) -> None:
    """Test that `read(limits=...)` reads the limits of the chosen endpoints only."""
    mock_api.post(READ_URL, payload=[{"name": "mocked-name", "value": "10.5"}, {"name": "mocked-name", "value": "2"}])

    await client.read([System.OUTDOOR_TEMPERATURE, System.OPERATING_MODE], counts=counts, limits=limits)

    assert [item["attr"] for item in sent_requests(mock_api)[0]["data"]] == expected_attrs
    await client.close()


async def test_read_invalid_limits(client: KebaKeEnergyAPI, counts: DeviceCounts) -> None:
    """Test that an invalid `limits` value raises `APIError`."""
    # Typed as Any, as a type checker would reject the invalid value.
    limits: Any = "some"

    with pytest.raises(
        APIError, match=r"^Invalid limits 'some'! Allowed values are 'all', 'none', 'read_only' and 'writable'$"
    ):
        await client.read([System.OUTDOOR_TEMPERATURE], counts=counts, limits=limits)

    await client.close()


async def test_read_invalid_limits_without_variables(
    client: KebaKeEnergyAPI, mock_api: aioresponses, counts: DeviceCounts
) -> None:
    """Test that an invalid `limits` value raises `APIError` also if no variable is read."""
    # Typed as Any, as a type checker would reject the invalid value.
    limits: Any = "some"

    with pytest.raises(APIError, match=r"^Invalid limits 'some'!"):
        await client.read([BufferTank.TOP_TEMPERATURE], counts=counts, limits=limits)

    mock_api.assert_not_called()


@pytest.mark.parametrize(
    ("section", "value", "expected_error"),
    [
        (HeatingCircuit.PUMP_ACTIVE, "maybe", "^Can't convert 'maybe' of HeatingCircuit.PUMP_ACTIVE to bool$"),
        (System.OPERATING_MODE, "9", "^Can't convert '9' of System.OPERATING_MODE to SystemOperatingMode$"),
        (System.OPERATING_MODE, "auto", "^Can't convert 'auto' of System.OPERATING_MODE to SystemOperatingMode$"),
        (System.OUTDOOR_TEMPERATURE, "-", "^Can't convert '-' of System.OUTDOOR_TEMPERATURE to float$"),
    ],
    ids=["bool", "enum_value", "enum_name", "float"],
)
async def test_read_invalid_value(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    counts: DeviceCounts,
    section: Section,
    value: str,
    expected_error: str,
) -> None:
    """Test that a value that can't be converted raises `InvalidResponseError`."""
    mock_api.post(READ_URL, payload=[{"name": "mocked-name", "value": value}])

    with pytest.raises(InvalidResponseError, match=expected_error):
        await client.read([section], counts=counts)

    await client.close()


async def test_read_message_ids(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    counts: DeviceCounts,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `read(message_ids=True)` reads the message id after each value in the same request."""
    mock_api.post(READ_URL, payload=READ_WITH_MESSAGE_IDS_RESPONSE)

    readings: Readings = await client.read(
        [
            System.OUTDOOR_TEMPERATURE,
            HeatPump.STATE,
            HeatingCircuit.ROOM_TEMPERATURE,
            SolarCircuit.CONSUMER_TEMPERATURE,
        ],
        counts=counts,
        message_ids=True,
    )

    assert [reading.message_id for reading in readings[HeatingCircuit.ROOM_TEMPERATURE]] == [
        MessageId(value=10, kind=MessageIdKind.DEACTIVATED),
        MessageId(value=0, kind=MessageIdKind.OK),
    ]
    assert readings[HeatPump.STATE][0].message_id is None
    assert readings == snapshot(name="readings")
    assert sent_requests(mock_api) == snapshot(name="requests")
    await client.close()


async def test_read_unknown_message_id(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    counts: DeviceCounts,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that an unknown message id is left out, also in later reads, and the value is still read."""
    mock_api.post(
        READ_URL,
        status=500,
        body=json.dumps({"developerMessage": f"Reading variable: {UNKNOWN_MESSAGE_ID} failed (-1)", "status": 500}),
    )
    mock_api.post(READ_URL, payload=READ_WITHOUT_UNKNOWN_MESSAGE_ID_RESPONSE, repeat=True)
    sections: list[Section] = [System.OUTDOOR_TEMPERATURE, HeatingCircuit.ROOM_TEMPERATURE]

    readings: Readings = await client.read(sections, counts=counts, message_ids=True)

    assert readings[System.OUTDOOR_TEMPERATURE] == [Reading(value=10.5, position=1, unit="°C")]
    assert readings[HeatingCircuit.ROOM_TEMPERATURE][0].message_id == MessageId(
        value=10, kind=MessageIdKind.DEACTIVATED
    )
    assert await client.read(sections, counts=counts, message_ids=True) == readings
    assert sent_requests(mock_api) == snapshot(name="requests")
    await client.close()


async def test_read_unknown_value_with_message_ids(
    client: KebaKeEnergyAPI, mock_api: aioresponses, counts: DeviceCounts
) -> None:
    """Test that an unknown value variable raises `UnsupportedVariableError`, also with message ids."""
    variable: str = "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue"
    mock_api.post(
        READ_URL,
        status=500,
        body=json.dumps({"developerMessage": f"Reading variable: {variable} failed (-1)", "status": 500}),
    )

    with pytest.raises(UnsupportedVariableError, match=r"^500 Internal Server Error: .* - Reading variable: ") as error:
        await client.read([System.OUTDOOR_TEMPERATURE], counts=counts, message_ids=True)

    assert error.value.variable == variable
    await client.close()


async def test_write(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `write()` writes all values with one request, including the consumer priorities."""
    mock_api.post(WRITE_URL, payload=[])

    await client.write(
        {
            System.OPERATING_MODE: [SystemOperatingMode.AUTO_HEAT],
            BufferTank.OPERATING_MODE: [None, BufferTankOperatingMode.MANUAL_CHARGE],
            HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL: [20, None, 21.5],
            HeatingCircuit.USE_EXCESS_ENERGY: [True, False],
            HeatingCircuit.HEATING_CURVE: ["HC1"],
            HeatingCircuit.VACATION_START: [1767225600],
            SolarCircuit.CONSUMER_1_PRIORITY: [True, None, False],
            DHWTank.TARGET_TEMPERATURE: [],
        }
    )

    assert sent_requests(mock_api) == snapshot
    await client.close()


async def test_write_nothing(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that `write()` sends no request without values."""
    await client.write({HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL: [None, None]})
    mock_api.assert_not_called()


@pytest.mark.parametrize(
    ("section", "values", "expected_error"),
    [
        (HeatPump.STATE, [1], "^HeatPump.STATE is read-only$"),
        (
            HeatingCircuit.HEATING_CURVE,
            "HC1",
            "^HeatingCircuit.HEATING_CURVE needs a sequence of values, not a string$",
        ),
        (System.OPERATING_MODE, [None, None], "^System.OPERATING_MODE is system wide, only one value can be written$"),
        (
            HeatingCircuit.USE_EXCESS_ENERGY,
            [1],
            "^Invalid value 1 for HeatingCircuit.USE_EXCESS_ENERGY, expected bool$",
        ),
        (
            HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL,
            [True],
            "^Invalid value True for HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL, expected float$",
        ),
        (
            HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL,
            ["20"],
            "^Invalid value '20' for HeatingCircuit.TARGET_ROOM_TEMPERATURE_NORMAL, expected float$",
        ),
        (HeatingCircuit.VACATION_START, [1.5], "^Invalid value 1.5 for HeatingCircuit.VACATION_START, expected int$"),
        (HeatingCircuit.HEATING_CURVE, [1], "^Invalid value 1 for HeatingCircuit.HEATING_CURVE, expected str$"),
        (
            BufferTank.OPERATING_MODE,
            [HeatingCircuitOperatingMode.AUTO],
            (
                "^Invalid value <HeatingCircuitOperatingMode.AUTO: 1> for BufferTank.OPERATING_MODE, "
                "expected BufferTankOperatingMode$"
            ),
        ),
        (
            BufferTank.OPERATING_MODE,
            [1],
            "^Invalid value 1 for BufferTank.OPERATING_MODE, expected BufferTankOperatingMode$",
        ),
    ],
    ids=[
        "read_only",
        "string",
        "system_wide",
        "int_for_bool",
        "bool_for_float",
        "str_for_float",
        "float_for_int",
        "int_for_str",
        "other_enum",
        "int_for_enum",
    ],
)
async def test_write_invalid(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    section: Section,
    values: list[WriteValue | None],
    expected_error: str,
) -> None:
    """Test that `write()` raises `APIError` for invalid values without a request."""
    with pytest.raises(APIError, match=expected_error):
        await client.write({section: values})

    mock_api.assert_not_called()


@pytest.mark.parametrize(
    ("sections", "unknown"),
    [
        ([HeatPump.STATE, HeatPump.COP], []),
        (
            [HeatPump.COP, HeatPump.STATE, HeatingCircuit.NAME, HeatingCircuit.TYPE, HeatPump.COP],
            ["APPL.CtrlAppl.sParam.heatpump[0].values.COP", "APPL.CtrlAppl.sParam.heatCircuit[1].param.name"],
        ),
        ([HeatPump.COP, BufferTank.NAME], ["APPL.CtrlAppl.sParam.heatpump[0].values.COP"]),
    ],
    ids=["all_supported", "unknown_variables", "none_supported"],
)
async def test_filter_supported(
    mock_api: aioresponses,
    sections: list[Section],
    unknown: list[str],
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `filter_supported()` drops the sections with a variable the Web HMI rejects."""
    for name in unknown:
        mock_api.post(
            READ_URL,
            status=500,
            body=json.dumps({"developerMessage": f"Reading variable: {name} failed (-1)", "status": 500}),
        )

    mock_api.post(READ_URL, payload=[])

    async with KebaKeEnergyAPI(host="mocked-host") as client:
        supported: list[Section] = await client.filter_supported(sections, counts=FILTER_COUNTS)

    assert supported == snapshot(name="supported")
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
    ids=["other_status", "unknown_message", "variable_not_requested"],
)
async def test_filter_supported_api_error(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    counts: DeviceCounts,
    status: int,
    body: str,
    expected_error: str,
) -> None:
    """Test that `filter_supported()` raises errors that don't name a requested variable."""
    mock_api.post(READ_URL, status=status, body=body)

    with pytest.raises(APIError, match=expected_error):
        await client.filter_supported([DHWTank.TEMPERATURE, HeatPump.STATE], counts=counts)

    await client.close()


async def test_filter_supported_empty(client: KebaKeEnergyAPI, mock_api: aioresponses, counts: DeviceCounts) -> None:
    """Test that `filter_supported()` sends no request without sections."""
    assert await client.filter_supported([], counts=counts) == []
    mock_api.assert_not_called()


async def test_get_curve_tables(
    client: KebaKeEnergyAPI, mock_api: aioresponses, snapshot: SnapshotAssertion, sent_requests: SentRequests
) -> None:
    """Test that `get_curve_tables()` reads the names and the points of the curves in use."""
    mock_api.post(READ_URL, payload=CURVE_TABLE_NAMES_RESPONSE)
    mock_api.post(
        READ_URL,
        payload=[
            *curve_table_response("7", CURVE_TABLE_POINTS),
            # A number of points above the maximum is limited to the maximum.
            *curve_table_response("20", CURVE_TABLE_MAX_POINTS),
        ],
    )

    curves: dict[str, CurveTable] = await client.get_curve_tables()

    assert curves == {
        "HC1": CurveTable(name="HC1", points=tuple(CURVE_TABLE_POINTS)),
        "HC2": CurveTable(name="HC2", points=tuple(CURVE_TABLE_MAX_POINTS)),
    }
    assert sent_requests(mock_api) == snapshot(name="requests")
    await client.close()


async def test_get_curve_tables_without_curves(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that `get_curve_tables()` reads no points without curves."""
    mock_api.post(READ_URL, payload=[{"value": ""} for _ in range(30)])

    assert await client.get_curve_tables() == {}

    mock_api.assert_called_once()
    await client.close()


async def test_set_curve_table_points(
    client: KebaKeEnergyAPI, mock_api: aioresponses, snapshot: SnapshotAssertion, sent_requests: SentRequests
) -> None:
    """Test that `set_curve_table_points()` writes the points, resets the unused ones and saves the curve."""
    mock_api.post(READ_URL, payload=CURVE_TABLE_NAMES_RESPONSE)
    mock_api.post(WRITE_URL, payload=[])

    await client.set_curve_table_points("HC2", CURVE_TABLE_POINTS)

    assert sent_requests(mock_api) == snapshot(name="requests")
    await client.close()


async def test_set_curve_table_points_unknown_curve(client: KebaKeEnergyAPI, mock_api: aioresponses) -> None:
    """Test that an unknown curve raises `APIError` without a write."""
    mock_api.post(READ_URL, payload=CURVE_TABLE_NAMES_RESPONSE)

    with pytest.raises(APIError, match=r"^Invalid curve table 'HC3'! Allowed values are \['HC1', 'HC2'\]$"):
        await client.set_curve_table_points("HC3", CURVE_TABLE_POINTS)

    mock_api.assert_called_once()
    await client.close()


@pytest.mark.parametrize("number_of_points", [6, 17], ids=["too_few", "too_many"])
async def test_set_curve_table_points_invalid_number(
    client: KebaKeEnergyAPI, mock_api: aioresponses, number_of_points: int
) -> None:
    """Test that an invalid number of points raises `APIError` without a request."""
    points: list[CurvePoint] = [CurvePoint(outdoor=0, flow=30)] * number_of_points

    with pytest.raises(APIError, match=f"^A curve table needs 7 to 16 points, not {number_of_points}$"):
        await client.set_curve_table_points("HC1", points)

    mock_api.assert_not_called()
