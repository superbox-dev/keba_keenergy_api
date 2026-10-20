# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the heating circuit endpoints."""

import json
import re
from copy import deepcopy
from typing import TYPE_CHECKING
from typing import Any

import pytest
from aioresponses import aioresponses
from syrupy.assertion import SnapshotAssertion

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import TIMEOUT
from tests.conftest import WRITE_URL
from tests.conftest import SentRequests
from tests.conftest import case_id
from tests.test_endpoints.test_heat_circuit_section_data import GETTERS
from tests.test_endpoints.test_heat_circuit_section_data import HEATING_CURVE_POINTS
from tests.test_endpoints.test_heat_circuit_section_data import INVALID_CURVE_MESSAGE
from tests.test_endpoints.test_heat_circuit_section_data import INVALID_GETTERS
from tests.test_endpoints.test_heat_circuit_section_data import INVALID_SETTERS
from tests.test_endpoints.test_heat_circuit_section_data import SETTERS
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_names_payload
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_payload

if TYPE_CHECKING:
    from keba_keenergy_api.endpoints import HeatingCurves


@pytest.mark.parametrize(
    ("method", "kwargs", "response", "expected"),
    GETTERS,
    ids=[case_id(method, kwargs, *response.values(), expected) for method, kwargs, response, expected in GETTERS],
)
async def test_getter(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    kwargs: dict[str, Any],
    response: dict[str, Any],
    expected: float | str,
) -> None:
    """Test that a getter reads its variables and returns the converted value."""
    mock_api.post(READ_URL, payload=[{"name": name, "value": value} for name, value in response.items()])

    data: float | str = await getattr(client.heat_circuit, method)(**kwargs)

    assert data == expected
    assert type(data) is type(expected)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in response]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
    )


@pytest.mark.parametrize(
    ("method", "kwargs", "response", "message"),
    INVALID_GETTERS,
    ids=[case_id(method, kwargs, *response.values()) for method, kwargs, response, _ in INVALID_GETTERS],
)
async def test_getter_invalid_value(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    kwargs: dict[str, Any],
    response: dict[str, Any],
    message: str,
) -> None:
    """Test that a getter raises `APIError` for a value that can't be converted."""
    mock_api.post(READ_URL, payload=[{"name": name, "value": value} for name, value in response.items()])

    with pytest.raises(APIError, match=re.escape(message)):
        await getattr(client.heat_circuit, method)(**kwargs)

    mock_api.assert_called_once_with(
        url=READ_URL,
        data=json.dumps([{"name": name, "attr": "1"} for name in response]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
    )


@pytest.mark.parametrize(
    ("method", "value", "kwargs", "expected"),
    SETTERS,
    ids=[case_id(method, kwargs, value) for method, value, kwargs, _ in SETTERS],
)
async def test_setter(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    value: float | str,
    kwargs: dict[str, Any],
    expected: dict[str, str],
) -> None:
    """Test that a setter writes the expected variables."""
    mock_api.post(WRITE_URL, payload={})

    await getattr(client.heat_circuit, method)(value, **kwargs)

    mock_api.assert_called_once_with(
        url=WRITE_URL,
        data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
        method="POST",
        headers={},
        ssl=False,
        timeout=TIMEOUT,
    )


@pytest.mark.parametrize(
    ("method", "value", "kwargs", "message"),
    INVALID_SETTERS,
    ids=[case_id(method, kwargs, value) for method, value, kwargs, _ in INVALID_SETTERS],
)
async def test_setter_invalid_value(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    method: str,
    value: str,
    kwargs: dict[str, Any],
    message: str,
) -> None:
    """Test that a setter raises `APIError` for an invalid value and sends no request."""
    with pytest.raises(APIError, match=re.escape(message)):
        await getattr(client.heat_circuit, method)(value, **kwargs)

    mock_api.assert_not_called()


@pytest.mark.parametrize("name", ["HC1", "HC FBH"], ids=["HC1", "HC_FBH"])
async def test_set_heating_curve(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
    name: str,
) -> None:
    """Test that `set_heating_curve()` checks the curve name and writes it."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(WRITE_URL, payload={})

    await client.heat_circuit.set_heating_curve(name)

    assert sent_requests(mock_api) == snapshot


@pytest.mark.parametrize("name", ["INVALID"], ids=["invalid"])
async def test_set_heating_curve_unknown_curve(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
    name: str,
) -> None:
    """Test that `set_heating_curve()` raises `APIError` for an unknown heating curve."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)

    with pytest.raises(APIError, match=re.escape(INVALID_CURVE_MESSAGE)):
        await client.heat_circuit.set_heating_curve(name)

    assert sent_requests(mock_api) == snapshot


@pytest.mark.parametrize("name", ["HC1", "HC FBH"], ids=["HC1", "HC_FBH"])
async def test_set_cooling_curve(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
    name: str,
) -> None:
    """Test that `set_cooling_curve()` checks the curve name and writes it."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(WRITE_URL, payload={})

    await client.heat_circuit.set_cooling_curve(name)

    assert sent_requests(mock_api) == snapshot


@pytest.mark.parametrize("name", ["INVALID"], ids=["invalid"])
async def test_set_cooling_curve_unknown_curve(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
    name: str,
) -> None:
    """Test that `set_cooling_curve()` raises `APIError` for an unknown cooling curve."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)

    with pytest.raises(APIError, match=re.escape(INVALID_CURVE_MESSAGE)):
        await client.heat_circuit.set_cooling_curve(name)

    assert sent_requests(mock_api) == snapshot


@pytest.mark.parametrize(
    ("heating_curve", "points_payload"),
    [
        (None, heating_curve_points_payload),
        # Only the requested heating curve is read (name, number of points and 16 points).
        ("HC1", heating_curve_points_payload[:34]),
    ],
    ids=["all", "HC1"],
)
async def test_get_heating_curve_points(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
    heating_curve: str | None,
    points_payload: list[dict[str, Any]],
) -> None:
    """Test that `get_heating_curve_points()` returns the value from the response."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(READ_URL, payload=points_payload)

    response: HeatingCurves = await client.heat_circuit.get_heating_curve_points(heating_curve)

    assert response == snapshot(name="response")
    assert sent_requests(mock_api) == snapshot(name="requests")


@pytest.mark.parametrize("heating_curve", ["HC10"], ids=["HC10"])
async def test_get_heating_curve_points_unknown_curve(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
    heating_curve: str,
) -> None:
    """Test that `get_heating_curve_points()` raises `APIError` for an unknown curve without reading points."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)

    with pytest.raises(APIError, match='Heating curve "HC10" not found'):
        await client.heat_circuit.get_heating_curve_points(heating_curve)

    assert sent_requests(mock_api) == snapshot


async def test_get_heating_curve_points_too_many_points(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
) -> None:
    """Test that `get_heating_curve_points()` returns at most 16 points."""
    payload: list[dict[str, Any]] = deepcopy(heating_curve_points_payload[:34])
    payload[1]["value"] = "99"

    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(READ_URL, payload=payload)

    response: HeatingCurves = await client.heat_circuit.get_heating_curve_points("HC1")

    expected: int = 16
    assert len(response["HC1"]) == expected


async def test_get_heating_curve_points_skips_unknown_curve_names(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
) -> None:
    """Test that `get_heating_curve_points()` skips the points of unknown heating curves."""
    payload: list[dict[str, Any]] = deepcopy(heating_curve_points_payload)
    payload[0]["value"] = "UNKNOWN"

    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(READ_URL, payload=payload)

    response: HeatingCurves = await client.heat_circuit.get_heating_curve_points()

    assert "UNKNOWN" not in response
    assert "HC1" not in response
    assert "HC2" in response


async def test_set_heating_curve_points(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `set_heating_curve_points()` reads the curve names and writes the points."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(READ_URL, payload=[{"name": "APPL.CtrlAppl.sParam.linTabPool[0].name", "value": "HC1"}])
    mock_api.post(WRITE_URL, payload={})

    await client.heat_circuit.set_heating_curve_points("HC1", points=HEATING_CURVE_POINTS)

    assert sent_requests(mock_api) == snapshot


async def test_set_heating_curve_points_unknown_curve(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `set_heating_curve_points()` raises `APIError` for an unknown heating curve."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)

    with pytest.raises(APIError, match=re.escape(INVALID_CURVE_MESSAGE)):
        await client.heat_circuit.set_heating_curve_points("HC_HK", points=HEATING_CURVE_POINTS)

    assert sent_requests(mock_api) == snapshot


async def test_set_heating_curve_points_name_mismatch(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `set_heating_curve_points()` raises `APIError` if the curve name does not match its index."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)
    mock_api.post(READ_URL, payload=[{"name": "APPL.CtrlAppl.sParam.linTabPool[0].name", "value": "INVALID"}])

    with pytest.raises(APIError, match='Name of heating curve "HC1" does not match entry with index 0'):
        await client.heat_circuit.set_heating_curve_points("HC1", points=HEATING_CURVE_POINTS)

    assert sent_requests(mock_api) == snapshot


async def test_get_available_heating_curves(
    client: KebaKeEnergyAPI,
    mock_api: aioresponses,
    snapshot: SnapshotAssertion,
    sent_requests: SentRequests,
) -> None:
    """Test that `get_available_heating_curves()` returns the value from the response."""
    mock_api.post(READ_URL, payload=heating_curve_names_payload)

    data: tuple[tuple[int, str], ...] = await client.heat_circuit.get_available_heating_curves()

    assert data == (
        (0, "HC1"),
        (1, "HC2"),
        (2, "HC3"),
        (3, "HC4"),
        (4, "HC5"),
        (5, "HC6"),
        (6, "HC7"),
        (7, "HC8"),
        (12, "HC FBH"),
        (13, "HC HK"),
    )
    assert sent_requests(mock_api) == snapshot
