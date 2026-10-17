# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the buffer tank endpoints."""

import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import BoolEnum
from keba_keenergy_api.constants import BufferTankExcessEnergyMode
from keba_keenergy_api.constants import BufferTankOperatingMode
from keba_keenergy_api.error import APIError


class TestHappyPathBufferTankSection:
    """Tests for the buffer tank endpoints with valid responses and input."""

    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
        """Test that `get_name()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.name",
                        "attributes": {
                            "longText": "Name",
                        },
                        "value": "Puffer1",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.buffer_tank.get_name()

            assert isinstance(data, str)
            assert data == "Puffer1"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.name", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_current_top_temperature(self) -> None:
        """Test that `get_current_top_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].topTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. top act.",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "5",
                        },
                        "value": "45.0273",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_current_top_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(45.03)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].topTemp.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_current_bottom_temperature(self) -> None:
        """Test that `get_current_bottom_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].midTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. bottom act.",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "5",
                        },
                        "value": "33.094",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_current_bottom_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(33.09)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].midTemp.values.actValue", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 2, "heat_up"), (False, 2, 2)],
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtBufferMode",
                            "longText": "Oper. mode",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                            "lowerLimit": "0",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.buffer_tank.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("off", 0), ("ON", 1), (BufferTankOperatingMode.HEAT_UP.value, 2)],
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
            await client.buffer_tank.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode", '
                    f'"value": "{expected_value}"}}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_standby_temperature(self) -> None:
        """Test that `get_standby_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.backupTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Backup temp.",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "10",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_standby_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(10.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.backupTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_standby_temperature(self) -> None:
        """Test that `set_standby_temperature()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.buffer_tank.set_standby_temperature(10)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.backupTemp", "value": "10"}]',
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].values.setTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Set temp.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "37.75",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_target_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(37.75)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].values.setTemp", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_excess_energy_target_temperature(self) -> None:
        """Test that `get_excess_energy_target_temperature()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Set heat temp.",
                            "unitId": "Temp",
                            "upperLimit": "95",
                            "lowerLimit": "0",
                        },
                        "value": "55",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_excess_energy_target_temperature()

            assert isinstance(data, float)
            assert data == pytest.approx(55.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.value", "attr": "1"}]',
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
            await client.buffer_tank.set_excess_energy_target_temperature(43)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.value", "value": "43"}]',
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.hyst",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Hyst. heat temp.",
                            "unitId": "TempRel",
                            "upperLimit": "5",
                            "lowerLimit": "0",
                        },
                        "value": "2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_excess_energy_target_temperature_hysteresis()

            assert isinstance(data, float)
            assert data == pytest.approx(2.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.hyst", "attr": "1"}]',
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
            await client.buffer_tank.set_excess_energy_target_temperature_hysteresis(3)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.excessEnergyTemp.hyst", "value": "3"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_outdoor_temperature_excess_energy_limit(self) -> None:
        """Test that `get_outdoor_temperature_excess_energy_limit()` returns the value from the response."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.thresholdOutTempExcessEnergy.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Außentemp. ÜE Grenze",
                            "unitId": "Temp",
                            "upperLimit": "50.0",
                            "lowerLimit": "0",
                        },
                        "value": "25",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.buffer_tank.get_outdoor_temperature_excess_energy_limit()

            assert isinstance(data, float)
            assert data == pytest.approx(25.0)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.thresholdOutTempExcessEnergy.value", '
                    '"attr": "1"}]'
                ),
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_outdoor_temperature_excess_energy_limit(self) -> None:
        """Test that `set_outdoor_temperature_excess_energy_limit()` sends the expected payload."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.buffer_tank.set_outdoor_temperature_excess_energy_limit(22)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.thresholdOutTempExcessEnergy.value", '
                    '"value": "22"}]'
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy",
                        "attributes": {
                            "longText": "Use excess en.",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.buffer_tank.get_use_excess_energy(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy", "attr": "1"}]',
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
            await client.buffer_tank.set_use_excess_energy(mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.useExcessEnergy", '
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
                await client.buffer_tank.set_use_excess_energy(mode)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, 2, "cooling"),
            (False, BufferTankExcessEnergyMode.HEATING.value, 1),
            (True, BufferTankExcessEnergyMode.OFF.value, "off"),
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].values.useExcessEnergy",
                        "attributes": {
                            "formatId": "fmtExcessEnergyInfo",
                            "longText": "Excess energy buffer 1",
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
            data: int | str = await client.buffer_tank.get_excess_energy_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].values.useExcessEnergy", "attr": "1"}]',
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].values.heatRequestTop",
                        "attributes": {},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.buffer_tank.get_heat_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].values.heatRequestTop", "attr": "1"}]',
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
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].values.coolRequestBot",
                        "attributes": {},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.buffer_tank.get_cool_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].values.coolRequestBot", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )


class TestUnhappyPathBufferTankSection:
    """Tests for the buffer tank endpoints with invalid responses and input."""

    @pytest.mark.asyncio
    async def test_get_invalid_type_operating_mode(self) -> None:
        """Test that `get_operating_mode()` raises `APIError` for a value that is not an integer."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtBufferMode",
                            "longText": "Oper. mode",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                            "lowerLimit": "0",
                        },
                        "value": "-0.010321236",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    'Can\'t convert value to type "int"! '
                    r"{'name': 'APPL\.CtrlAppl\.sParam\.bufferTank\[0]\.param\.operatingMode', "
                    r"'attributes': {'formatId': 'fmtBufferMode', 'longText': 'Oper\. mode', "
                    "'unitId': 'Enum', 'upperLimit': '32767', 'lowerLimit': '0'}, 'value': '-0.010321236'}"
                ),
            ):
                await client.buffer_tank.get_operating_mode(human_readable=False)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value"),
        [(True, 10)],
    )
    async def test_get_invalid_human_readable_operating_mode(
        self,
        *,
        human_readable: bool,
        payload_value: int,
    ) -> None:
        """Test that `get_operating_mode()` raises `APIError` for an unknown value."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtBufferMode",
                            "longText": "Oper. mode",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                            "lowerLimit": "0",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(
                APIError,
                match=(
                    "Can't convert value to human readable value! "
                    r"{'name': 'APPL\.CtrlAppl\.sParam\.bufferTank\[0]\.param\.operatingMode', "
                    r"'attributes': {'formatId': 'fmtBufferMode', 'longText': 'Oper\. mode', "
                    "'unitId': 'Enum', 'upperLimit': '32767', 'lowerLimit': '0'}, 'value': '10'}"
                ),
            ):
                await client.buffer_tank.get_operating_mode(human_readable=human_readable)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                headers={},
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_operating_mode(
        self,
        operating_mode: int | str,
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
                APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1', 'HEAT_UP', '2']"
            ):
                await client.buffer_tank.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_not_called()
