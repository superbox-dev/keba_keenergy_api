# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the heating circuit endpoints."""

from copy import deepcopy
from typing import Any

import pytest
from aioresponses.core import aioresponses
from syrupy.assertion import SnapshotAssertion

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import BoolEnum
from keba_keenergy_api.constants import HeatCircuitExcessEnergyMode
from keba_keenergy_api.constants import HeatCircuitHeatRequest
from keba_keenergy_api.constants import HeatCircuitMode
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.endpoints import HeatingCurvePoint
from keba_keenergy_api.endpoints import HeatingCurves
from keba_keenergy_api.error import APIError
from tests.conftest import SentRequests
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_names_payload
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_payload


class TestHappyPathHeatCircuitSection:
    """Tests for the heating circuit endpoints with valid responses and input."""

    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
        """Test that `get_name()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.name",
                        "attributes": {
                            "longText": "Designation",
                        },
                        "value": "FBH",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.heat_circuit.get_name()

            assert isinstance(data, str)
            assert data == "FBH"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.name", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "0", "heating"),
            (False, HeatCircuitMode.HEATING.value, 0),
            (True, "1", "cooling"),
            (False, HeatCircuitMode.COOLING.value, 1),
            (True, "2", "heating_and_cooling"),
            (False, HeatCircuitMode.HEATING_AND_COOLING.value, 2),
            (True, "3", "heating_and_active_cooling"),
            (False, HeatCircuitMode.HEATING_AND_ACTIVE_COOLING.value, 3),
        ],
    )
    async def test_get_mode(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `get_mode()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].type",
                        "attributes": {
                            "formatId": "fmtHeatCircuitMode",
                            "longText": "Mode",
                            "unitId": "Enum",
                            "upperLimit": "3",
                            "lowerLimit": "0",
                        },
                        "value": payload_value,
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].type", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_has_room_temperature(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `has_room_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomTemp",
                        "attributes": {"longText": "With room temp. sensor"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_room_temperature(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_room_temperature(self) -> None:
        """Test that `get_room_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. act.",
                            "unitId": "Temp",
                            "upperLimit": "80",
                            "lowerLimit": "0",
                        },
                        "value": "22.426912",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_room_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(22.43)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_has_room_humidity(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `has_room_humidity()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomHumidity",
                        "attributes": {"longText": "With room humidity sensor"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_room_humidity(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomHumidity", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_room_humidity(self) -> None:
        """Test that `get_room_humidity()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].humidityRoom.values.actValue",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Room humidity act.",
                            "unitId": "Pct",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "53",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_room_humidity()

            assert isinstance(data, float)
            expected: int = 53
            assert data == expected

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].humidityRoom.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_dew_point(self) -> None:
        """Test that `get_dew_point()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].dewPoint.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Dew Point",
                            "unitId": "Temp",
                            "upperLimit": "50.0",
                            "lowerLimit": "-20.0",
                        },
                        "value": "13.100544",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_dew_point()

            assert isinstance(data, float)
            assert data == pytest.approx(13.10)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].dewPoint.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_flow_temperature_setpoint(self) -> None:
        """Test that `get_flow_temperature_setpoint()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.flowSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Nominal temp.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "26.254391",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_flow_temperature_setpoint()

            assert isinstance(data, float)
            assert data == pytest.approx(26.25)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.flowSetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_has_mixer(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `has_mixer()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasMixer",
                        "attributes": {
                            "longText": "HC mixer",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_mixer(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasMixer", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_mixer_flow_temperature(self) -> None:
        """Test that `get_mixer_flow_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.flowTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp. act.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "26.254391",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_mixer_flow_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(26.25)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.flowTemp.values.'
                    'actValue", "attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_mixer_return_flow_temperature(self) -> None:
        """Test that `get_mixer_return_flow_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.refluxTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Reflux temp. act.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "31.254391",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_mixer_return_flow_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(31.25)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.refluxTemp.values.'
                    'actValue", "attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, -1, "closed"),
            (False, 0, 0),
            (True, 1, "open"),
            (True, "-0.045793723", "off"),
            (True, "0.045793723", "off"),
        ],
    )
    async def test_get_mixer_position(
        self,
        *,
        human_readable: bool,
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test that `get_mixer_position()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Mixer nom. value",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "-1",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_mixer_position(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled", '
                    '"attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_get_pump_state(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `get_pump_state()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB",
                        "attributes": {
                            "longText": "Pump nom.value",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_pump_state(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=('[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB", "attr": "1"}]'),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_has_return_flow_temperature(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `has_return_flow_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRefluxTemp",
                        "attributes": {
                            "longText": "With reflux sensor",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_return_flow_temperature(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRefluxTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_return_flow_temperature(self) -> None:
        """Test that `get_return_flow_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempReflux.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Reflux temp. act.",
                            "unitId": "Temp",
                        },
                        "value": "19",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_return_flow_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(19.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempReflux.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature(self) -> None:
        """Test that `get_target_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "22",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_target_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(22.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (True, "false", "off"),
            (False, "true", 1),
            (False, "false", 0),
        ],
    )
    async def test_get_use_excess_energy(
        self,
        *,
        human_readable: bool,
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test that `get_use_excess_energy()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy",
                        "attributes": {
                            "longText": "Use excess en.",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_use_excess_energy(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy", "attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, 2, "cooling"),
            (False, HeatCircuitExcessEnergyMode.OFF.value, 0),
            (False, HeatCircuitExcessEnergyMode.HEATING.value, 1),
        ],
    )
    async def test_get_excess_energy_mode(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `get_excess_energy_mode()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.useExcessEnergy",
                        "attributes": {
                            "formatId": "fmtExcessEnergyInfo",
                            "longText": "Excess energy HC 1",
                            "unitId": "Enum",
                            "upperLimit": "2",
                            "lowerLimit": "0",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_excess_energy_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.useExcessEnergy", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("mode", "expected_value"),
        [
            ("off", "0"),
            ("ON", "1"),
            (BoolEnum.ON.value, "1"),
            (BoolEnum.OFF.value, "0"),
        ],
    )
    async def test_set_use_excess_energy(
        self,
        mode: int | str,
        expected_value: str,
    ) -> None:
        """Test that `set_use_excess_energy()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_use_excess_energy(mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy", '
                    f'"value": "{expected_value}"}}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "mode",
        ["INVALID"],
    )
    async def test_set_invalid_use_excess_energy(self, mode: int | str) -> None:
        """Test that `set_use_excess_energy()` raises `APIError` for invalid values and sends no request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1']"):
                await client.heat_circuit.set_use_excess_energy(mode)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_excess_energy_target_temperature(self) -> None:
        """Test that `get_excess_energy_target_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Set heat temp.",
                            "unitId": "Temp",
                            "upperLimit": "30",
                            "lowerLimit": "10",
                        },
                        "value": "23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_excess_energy_target_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(23.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.value", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_target_temperature(self) -> None:
        """Test that `set_excess_energy_target_temperature()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_target_temperature(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.value", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_target_temperature_hysteresis(self) -> None:
        """Test that `get_excess_energy_target_temperature_hysteresis()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.hyst",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Hyst. heat temp.",
                            "unitId": "TempRel",
                            "upperLimit": "2",
                            "lowerLimit": "0",
                        },
                        "value": "0.2",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_excess_energy_target_temperature_hysteresis()

            assert isinstance(data, float)
            assert data == pytest.approx(0.2)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.hyst", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_target_temperature_hysteresis(self) -> None:
        """Test that `set_excess_energy_target_temperature_hysteresis()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_target_temperature_hysteresis(3)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.hyst", "value": "3"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_target_cooling_temperature(self) -> None:
        """Test that `get_excess_energy_target_cooling_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Set cool temp.",
                            "unitId": "Temp",
                            "upperLimit": "30",
                            "lowerLimit": "10",
                        },
                        "value": "23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_excess_energy_target_cooling_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(23.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.value", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_target_cooling_temperature(self) -> None:
        """Test that `set_excess_energy_target_cooling_temperature()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_target_cooling_temperature(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.value", "value": "23"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_target_cooling_temperature_hysteresis(self) -> None:
        """Test that `get_excess_energy_target_cooling_temperature_hysteresis()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.hyst",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Hyst. cool temp.",
                            "unitId": "TempRel",
                            "upperLimit": "2",
                            "lowerLimit": "0",
                        },
                        "value": "0.2",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_excess_energy_target_cooling_temperature_hysteresis()

            assert isinstance(data, float)
            assert data == pytest.approx(0.2)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.hyst", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_target_cooling_temperature_hysteresis(self) -> None:
        """Test that `set_excess_energy_target_cooling_temperature_hysteresis()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_target_cooling_temperature_hysteresis(3)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.hyst", "value": "3"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_selected_target_temperature(self) -> None:
        """Test that `get_selected_target_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.selectedSetTemp",
                        "attributes": {},
                        "value": "21.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_selected_target_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(21.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.selectedSetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_day(self) -> None:
        """Test that `get_target_temperature_day()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Day",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "30",
                        },
                        "value": "23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_target_temperature_day()

            assert isinstance(data, float)
            assert data == pytest.approx(23.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_day(self) -> None:
        """Test that `set_target_temperature_day()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_temperature_day(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_cooling_temperature_day(self) -> None:
        """Test that `get_target_cooling_temperature_day()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalCoolSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Day",
                            "unitId": "Temp",
                            "upperLimit": "30",
                            "lowerLimit": "10",
                        },
                        "value": "22",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_target_cooling_temperature_day()

            assert isinstance(data, float)
            assert data == pytest.approx(22.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalCoolSetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_cooling_temperature_day(self) -> None:
        """Test that `set_target_cooling_temperature_day()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_cooling_temperature_day(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalCoolSetTemp", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_limit_day(self) -> None:
        """Test that `get_heating_limit_day()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Heating limit Day",
                            "lowerLimit": "-20",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "16",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_heating_limit_day()

            assert isinstance(data, float)
            assert data == pytest.approx(16.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_limit_day(self) -> None:
        """Test that `set_heating_limit_day()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_limit_day(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_limit_day(self) -> None:
        """Test that `get_cooling_limit_day()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayCoolTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cooling limit Day",
                            "unitId": "Temp",
                            "upperLimit": "40",
                            "lowerLimit": "-20",
                        },
                        "value": "24",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_cooling_limit_day()

            assert isinstance(data, float)
            assert data == pytest.approx(24.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayCoolTemp.value", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_cooling_limit_day(self) -> None:
        """Test that `set_cooling_limit_day()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_cooling_limit_day(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayCoolTemp.value", "value": "23"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_heating_limit_day(self) -> None:
        """Test that `get_excess_energy_heating_limit_day()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Heating limit day",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "-20",
                        },
                        "value": "25",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_excess_energy_heating_limit_day()

            assert isinstance(data, float)
            assert data == pytest.approx(25.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayTemp", "attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_heating_limit_day(self) -> None:
        """Test that `set_excess_energy_heating_limit_day()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_heating_limit_day(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayTemp", '
                    '"value": "23"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_cooling_limit_day(self) -> None:
        """Test that `get_excess_energy_cooling_limit_day()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayCoolTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cooling limit day",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "-20",
                        },
                        "value": "10",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_excess_energy_cooling_limit_day()

            assert isinstance(data, float)
            assert data == pytest.approx(10.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayCoolTemp", '
                    '"attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_cooling_limit_day(self) -> None:
        """Test that `set_excess_energy_cooling_limit_day()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_cooling_limit_day(11)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayCoolTemp", '
                    '"value": "11"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_night(self) -> None:
        """Test that `get_target_temperature_night()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. night",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "30",
                        },
                        "value": "23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_target_temperature_night()

            assert isinstance(data, float)
            assert data == pytest.approx(23.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_night(self) -> None:
        """Test that `set_target_temperature_night()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_temperature_night(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_cooling_temperature_night(self) -> None:
        """Test that `get_target_cooling_temperature_night()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedCoolSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Night",
                            "unitId": "Temp",
                            "upperLimit": "30",
                            "lowerLimit": "10",
                        },
                        "value": "22",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_target_cooling_temperature_night()

            assert isinstance(data, float)
            assert data == pytest.approx(22.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedCoolSetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_cooling_temperature_night(self) -> None:
        """Test that `set_target_cooling_temperature_night()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_cooling_temperature_night(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedCoolSetTemp", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_limit_night(self) -> None:
        """Test that `get_heating_limit_night()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Heat limit Night",
                            "lowerLimit": "-20",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "16",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_heating_limit_night()

            assert isinstance(data, float)
            assert data == pytest.approx(16.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_limit_night(self) -> None:
        """Test that `set_heating_limit_night()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_limit_night(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value", "value": "23"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_limit_night(self) -> None:
        """Test that `get_cooling_limit_night()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightCoolTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cooling limit night",
                            "unitId": "Temp",
                            "upperLimit": "40",
                            "lowerLimit": "-20",
                        },
                        "value": "24",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_cooling_limit_night()

            assert isinstance(data, float)
            assert data == pytest.approx(24.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightCoolTemp.value", "attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_cooling_limit_night(self) -> None:
        """Test that `set_cooling_limit_night()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_cooling_limit_night(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightCoolTemp.value", '
                    '"value": "23"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_heating_limit_night(self) -> None:
        """Test that `get_excess_energy_heating_limit_night()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cooling limit night",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "-20",
                        },
                        "value": "25",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_excess_energy_heating_limit_night()

            assert isinstance(data, float)
            assert data == pytest.approx(25.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightTemp", '
                    '"attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_heating_limit_night(self) -> None:
        """Test that `set_excess_energy_heating_limit_night()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_heating_limit_night(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightTemp", '
                    '"value": "23"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_cooling_limit_night(self) -> None:
        """Test that `get_excess_energy_cooling_limit_night()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightCoolTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cooling limit night",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "-20",
                        },
                        "value": "25",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_excess_energy_cooling_limit_night()

            assert isinstance(data, float)
            assert data == pytest.approx(25.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightCoolTemp", '
                    '"attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_excess_energy_cooling_limit_night(self) -> None:
        """Test that `set_excess_energy_cooling_limit_night()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_excess_energy_cooling_limit_night(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightCoolTemp", '
                    '"value": "23"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_away(self) -> None:
        """Test that `get_target_temperature_away()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Vacation",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "30",
                        },
                        "value": "14",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_target_temperature_away()

            assert isinstance(data, float)
            assert data == pytest.approx(14.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_away(self) -> None:
        """Test that `set_target_temperature_away()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_temperature_away(14)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp", "value": "14"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_offset(self) -> None:
        """Test that `get_target_temperature_offset()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Offset",
                            "lowerLimit": "-2.5",
                            "unitId": "TempRel",
                            "upperLimit": "2.5",
                        },
                        "value": "2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_target_temperature_offset()

            assert isinstance(data, float)
            assert data == pytest.approx(2.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_offset(self) -> None:
        """Test that `set_target_temperature_offset()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_target_temperature_offset(2)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "value": "2"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 3, "night"), (False, 3, 3)],
    )
    async def test_get_operating_mode(
        self,
        *,
        human_readable: bool,
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test that `get_operating_mode()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHcMode",
                            "longText": "Operating mode",
                            "lowerLimit": "0",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [
            ("OFF", 0),
            ("AUTO", 1),
            (HeatCircuitOperatingMode.DAY.value, 2),
            (HeatCircuitOperatingMode.NIGHT.value, 3),
        ],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int | str,
        expected_value: int,
    ) -> None:
        """Test that `set_operating_mode()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", '
                    f'"value": "{expected_value}"}}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "0", "off"),
            (False, HeatCircuitHeatRequest.OFF.value, 0),
            (True, "1", "on"),
            (False, HeatCircuitHeatRequest.ON.value, 1),
            (True, "2", "flow_off"),
            (False, HeatCircuitHeatRequest.FLOW_OFF.value, 2),
            (True, "3", "temporary_off"),
            (False, HeatCircuitHeatRequest.TEMPORARY_OFF.value, 3),
            (True, "4", "room_off"),
            (False, HeatCircuitHeatRequest.ROOM_OFF.value, 4),
            (True, "5", "outdoor_off"),
            (False, HeatCircuitHeatRequest.OUTDOOR_OFF.value, 5),
            (True, "6", "inflow_off"),
            (False, HeatCircuitHeatRequest.INFLOW_OFF.value, 6),
        ],
    )
    async def test_get_heat_request(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `get_heat_request()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest",
                        "attributes": {
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_heat_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "0", "off"),
            (False, HeatCircuitHeatRequest.OFF.value, 0),
            (True, "1", "on"),
            (False, HeatCircuitHeatRequest.ON.value, 1),
            (True, "2", "flow_off"),
            (False, HeatCircuitHeatRequest.FLOW_OFF.value, 2),
            (True, "3", "temporary_off"),
            (False, HeatCircuitHeatRequest.TEMPORARY_OFF.value, 3),
            (True, "4", "room_off"),
            (False, HeatCircuitHeatRequest.ROOM_OFF.value, 4),
            (True, "5", "outdoor_off"),
            (False, HeatCircuitHeatRequest.OUTDOOR_OFF.value, 5),
            (True, "6", "inflow_off"),
            (False, HeatCircuitHeatRequest.INFLOW_OFF.value, 6),
        ],
    )
    async def test_get_cool_request(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `get_cool_request()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest",
                        "attributes": {
                            "formatId": "fmtReqInfo",
                            "longText": "Cool request",
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_cool_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_away_start_date(self) -> None:
        """Test that `get_away_start_date()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.start",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "unitId": "TimeHour",
                            "upperLimit": "86400",
                            "lowerLimit": "0",
                        },
                        "value": "1768690800",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_circuit.get_away_start_date()

            assert isinstance(data, int)
            expected: int = 1768690800
            assert data == expected

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.start", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_away_start_date(self) -> None:
        """Test that `set_away_start_date()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_away_start_date(1768690800)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.start", "value": "1768690800"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_away_end_date(self) -> None:
        """Test that `get_away_end_date()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.stop",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "unitId": "TimeHour",
                            "upperLimit": "86400",
                            "lowerLimit": "0",
                        },
                        "value": "1769036400",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_circuit.get_away_end_date()

            assert isinstance(data, int)
            expected: int = 1769036400
            assert data == expected

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.stop", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_away_end_date(self) -> None:
        """Test that `set_away_end_date()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_away_end_date(1768690800)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.stop", "value": "1768690800"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_curve_offset(self) -> None:
        """Test that `get_heating_curve_offset()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveOffset",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Heat curve offset",
                            "unitId": "TempRel",
                            "upperLimit": "10",
                            "lowerLimit": "-10",
                        },
                        "value": "3.5",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_heating_curve_offset()

            assert isinstance(data, float)
            assert data == pytest.approx(3.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveOffset", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_curve_offset(self) -> None:
        """Test that `set_heating_curve_offset()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_curve_offset(3.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveOffset", "value": "3.5"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_curve_offset(self) -> None:
        """Test that `get_cooling_curve_offset()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveOffset",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cool curve offset",
                            "unitId": "TempRel",
                            "upperLimit": "10",
                            "lowerLimit": "-10",
                        },
                        "value": "3.5",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_cooling_curve_offset()

            assert isinstance(data, float)
            assert data == pytest.approx(3.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveOffset", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_cooling_curve_offset(self) -> None:
        """Test that `set_cooling_curve_offset()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_cooling_curve_offset(3.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveOffset", "value": "3.5"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_curve_slope(self) -> None:
        """Test that `get_heating_curve_slope()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveGradient",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Heat curve grad.",
                            "upperLimit": "5",
                            "lowerLimit": "0",
                        },
                        "value": "0.25",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_heating_curve_slope()

            assert isinstance(data, float)
            assert data == pytest.approx(0.25)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveGradient", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_curve_slope(self) -> None:
        """Test that `set_heating_curve_slope()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_curve_slope(0.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveGradient", "value": "0.5"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_curve_slope(self) -> None:
        """Test that `get_cooling_curve_slope()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveGradient",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Cool curve grad.",
                            "upperLimit": "5",
                            "lowerLimit": "0",
                        },
                        "value": "0.5",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_cooling_curve_slope()

            assert isinstance(data, float)
            assert data == pytest.approx(0.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveGradient", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_cooling_curve_slope(self) -> None:
        """Test that `set_cooling_curve_slope()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_cooling_curve_slope(0.5)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveGradient", "value": "0.5"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (True, "false", "off"),
            (False, "true", 1),
            (False, "false", 0),
        ],
    )
    async def test_get_use_heating_curve(
        self,
        *,
        human_readable: bool,
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test that `get_use_heating_curve()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab",
                        "attributes": {},
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_use_heating_curve(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("mode", "expected_value"),
        [
            ("off", "0"),
            ("ON", "1"),
            (BoolEnum.ON.value, "1"),
            (BoolEnum.OFF.value, "0"),
        ],
    )
    async def test_set_use_heating_curve(
        self,
        mode: int | str,
        expected_value: str,
    ) -> None:
        """Test that `set_use_heating_curve()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_use_heating_curve(mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab", '
                    f'"value": "{expected_value}"}}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_curve(self) -> None:
        """Test that `get_heating_curve()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName",
                        "attributes": {
                            "longText": "Heat curve",
                        },
                        "value": "HC4",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.heat_circuit.get_heating_curve()

            assert isinstance(data, str)
            assert data == "HC4"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name",
        ["HC1", "HC FBH"],
    )
    async def test_set_heating_curve(self, snapshot: SnapshotAssertion, sent_requests: SentRequests, name: str) -> None:
        """Test that `set_heating_curve()` checks the curve name and writes it."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_curve(name)

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    async def test_get_cooling_curve(self) -> None:
        """Test that `get_cooling_curve()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coollinTab.fileName",
                        "attributes": {"longText": "Name of linTab"},
                        "value": "HC1",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.heat_circuit.get_cooling_curve()

            assert isinstance(data, str)
            assert data == "HC1"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.coollinTab.fileName", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name",
        ["HC1", "HC FBH"],
    )
    async def test_set_cooling_curve(self, snapshot: SnapshotAssertion, sent_requests: SentRequests, name: str) -> None:
        """Test that `set_cooling_curve()` checks the curve name and writes it."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_cooling_curve(name)

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("heating_curve", "points_payload"),
        [
            (None, heating_curve_points_payload),
            # Only the requested heating curve is read (name, number of points and 16 points)
            ("HC1", heating_curve_points_payload[:34]),
        ],
        ids=["all", "HC1"],
    )
    async def test_get_heating_curve_points(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        heating_curve: str | None,
        points_payload: list[dict[str, Any]],
    ) -> None:
        """Test that `get_heating_curve_points()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=points_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: HeatingCurves = await client.heat_circuit.get_heating_curve_points(heating_curve)

            assert isinstance(response, dict)
            assert response == snapshot(name="response")
            assert sent_requests(mock_keenergy_api) == snapshot(name="requests")

    @pytest.mark.asyncio
    async def test_set_heating_curve_points(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `set_heating_curve_points()` reads the curve names and writes the points."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.linTabPool[0].name",
                        "attributes": {"longText": "Table name"},
                        "value": "HC1",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_curve_points(
                "HC1",
                points=(
                    HeatingCurvePoint(outdoor=-20, flow=35),
                    HeatingCurvePoint(outdoor=-10, flow=33),
                    HeatingCurvePoint(outdoor=-5, flow=32),
                    HeatingCurvePoint(outdoor=0, flow=30),
                    HeatingCurvePoint(outdoor=5, flow=28),
                    HeatingCurvePoint(outdoor=10, flow=27),
                    HeatingCurvePoint(outdoor=20, flow=25),
                ),
            )

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    async def test_get_available_heating_curves(self, snapshot: SnapshotAssertion, sent_requests: SentRequests) -> None:
        """Test that `get_available_heating_curves()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: tuple[tuple[int, str], ...] = await client.heat_circuit.get_available_heating_curves()

            assert isinstance(data, tuple)
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

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_has_pump(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `has_pump()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasPump",
                        "attributes": {"longText": "HC pump"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_pump(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasPump", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, BoolEnum.ON.value, 1),
            (True, "false", "off"),
            (False, BoolEnum.OFF.value, 0),
        ],
    )
    async def test_has_var_speed_pump(
        self,
        *,
        human_readable: bool,
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test that `has_var_speed_pump()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasVarSpeedPump",
                        "attributes": {
                            "longText": "Var.speed pump",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_var_speed_pump(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[0].hasVarSpeedPump", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_pump_speed(self) -> None:
        """Test that `get_pump_speed()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].pumpAO.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Pump speed",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0",
                        },
                        "value": "0.4",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_pump_speed()

            assert isinstance(data, float)
            assert data == pytest.approx(0.4)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].pumpAO.values.setValueScaled", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("position", [1, 2, 3])
    async def test_get_room_temperature_with_position(self, position: int) -> None:
        """Test `get_room_temperature()` for different positions."""
        name: str = f"APPL.CtrlAppl.sParam.heatCircuit[{position - 1}].tempRoom.values.actValue"

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": name, "attributes": {}, "value": "21.456"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_room_temperature(position=position)

            assert isinstance(data, float)
            assert data == pytest.approx(21.46)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=f'[{{"name": "{name}", "attr": "1"}}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_has_mixer_with_position(self) -> None:
        """Test `has_mixer()` for the second heating circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatCircuit[1].hasMixer",
                        "attributes": {},
                        "value": "true",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.has_mixer(position=2)

            assert data == "on"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatCircuit[1].hasMixer", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )


class TestUnhappyPathHeatCircuitSection:
    """Tests for the heating circuit endpoints with invalid responses and input."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_operating_mode(
        self,
        operating_mode: int,
    ) -> None:
        """Test that `set_operating_mode()` raises `APIError` for invalid values and sends no request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    r"Invalid value! Allowed values are \['OFF', '0', 'AUTO', '1', 'DAY', '2', 'NIGHT', '3', "
                    "'HOLIDAY', '4', 'PARTY', '5', 'EXTERNAL', '8', 'ROOM_CONTROL', '9']"
                ),
            ):
                await client.heat_circuit.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value"),
        [(True, "16")],
    )
    async def test_get_invalid_heat_request(
        self,
        *,
        human_readable: bool,
        payload_value: str,
    ) -> None:
        """Test that `get_heat_request()` raises `APIError` for an unknown value."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest",
                        "attributes": {
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    "Can't convert value to human readable value! "
                    r"{'name': 'APPL\.CtrlAppl\.sParam\.heatCircuit\[0].values\.heatRequest', "
                    "'attributes': {'unitId': 'Enum', 'upperLimit': '6', 'lowerLimit': '0'}, 'value': '16'}"
                ),
            ):
                await client.heat_circuit.get_heat_request(human_readable=human_readable)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "mode",
        ["INVALID"],
    )
    async def test_set_invalid_use_heating_curve(self, mode: int | str) -> None:
        """Test that `set_use_heating_curve()` raises `APIError` for invalid values and sends no request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1']"):
                await client.heat_circuit.set_use_heating_curve(mode)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name",
        ["INVALID"],
    )
    async def test_set_invalid_heating_curve(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        name: str,
    ) -> None:
        """Test that `set_heating_curve()` raises `APIError` for an unknown heating curve."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    "Invalid value! Allowed values are "
                    r"\['HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC FBH', 'HC HK']"
                ),
            ):
                await client.heat_circuit.set_heating_curve(name)

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name",
        ["INVALID"],
    )
    async def test_set_invalid_cooling_curve(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        name: str,
    ) -> None:
        """Test that `set_cooling_curve()` raises `APIError` for an unknown cooling curve."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    "Invalid value! Allowed values are "
                    r"\['HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC FBH', 'HC HK']"
                ),
            ):
                await client.heat_circuit.set_cooling_curve(name)

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "heating_curve",
        ["HC10"],
    )
    async def test_get_invalid_heating_curve_points(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        heating_curve: str | None,
    ) -> None:
        """Test that `get_heating_curve_points()` raises `APIError` for an unknown curve without reading points."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match='Heating curve "HC10" not found'):
                await client.heat_circuit.get_heating_curve_points(heating_curve)

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    async def test_heating_curve_name_is_invalid_in_set_heating_curve_points(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `set_heating_curve_points()` raises `APIError` for an unknown heating curve."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.linTabPool[0].name",
                        "attributes": {"longText": "Table name"},
                        "value": "HC1",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    "Invalid value! Allowed values are "
                    r"\['HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC FBH', 'HC HK']"
                ),
            ):
                await client.heat_circuit.set_heating_curve_points(
                    "HC_HK",
                    points=(
                        HeatingCurvePoint(outdoor=-20, flow=35),
                        HeatingCurvePoint(outdoor=-10, flow=33),
                        HeatingCurvePoint(outdoor=-5, flow=32),
                        HeatingCurvePoint(outdoor=0, flow=30),
                        HeatingCurvePoint(outdoor=5, flow=28),
                        HeatingCurvePoint(outdoor=10, flow=27),
                        HeatingCurvePoint(outdoor=20, flow=25),
                    ),
                )

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    async def test_heating_curve_name_not_match_in_set_heating_curve_points(
        self,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `set_heating_curve_points()` raises `APIError` if the curve name does not match its index."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.linTabPool[0].name",
                        "attributes": {"longText": "Table name"},
                        "value": "INVALID",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=r'Name of heating curve "HC1" does not match entry with index 0',
            ):
                await client.heat_circuit.set_heating_curve_points(
                    "HC1",
                    points=(
                        HeatingCurvePoint(outdoor=-20, flow=35),
                        HeatingCurvePoint(outdoor=-10, flow=33),
                        HeatingCurvePoint(outdoor=-5, flow=32),
                        HeatingCurvePoint(outdoor=0, flow=30),
                        HeatingCurvePoint(outdoor=5, flow=28),
                        HeatingCurvePoint(outdoor=10, flow=27),
                        HeatingCurvePoint(outdoor=20, flow=25),
                    ),
                )

            assert sent_requests(mock_keenergy_api) == snapshot

    @pytest.mark.asyncio
    async def test_too_many_points_in_get_heating_curve_points(self) -> None:
        """Test that `get_heating_curve_points()` returns at most 16 points."""
        payload: list[dict[str, Any]] = deepcopy(heating_curve_points_payload[:34])
        payload[1]["value"] = "99"

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: HeatingCurves = await client.heat_circuit.get_heating_curve_points("HC1")

            expected: int = 16
            assert len(response["HC1"]) == expected

    @pytest.mark.asyncio
    async def test_get_heating_curve_points_skips_unknown_curve_name(self) -> None:
        """Test that `get_heating_curve_points()` skips the points of unknown heating curves."""
        payload: list[dict[str, Any]] = deepcopy(heating_curve_points_payload)
        payload[0]["value"] = "UNKNOWN"

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=heating_curve_names_payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: HeatingCurves = await client.heat_circuit.get_heating_curve_points()

            assert "UNKNOWN" not in response
            assert "HC1" not in response
            assert "HC2" in response
