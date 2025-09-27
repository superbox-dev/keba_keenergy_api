from typing import Any

import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatCircuitExternalCoolRequest
from keba_keenergy_api.constants import HeatCircuitExternalHeatRequest
from keba_keenergy_api.constants import HeatCircuitHasRoomTemperature
from keba_keenergy_api.constants import HeatCircuitHeatRequest
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HeatPumpCompressorUseNightSpeed
from keba_keenergy_api.constants import HeatPumpHasPassiveCooling
from keba_keenergy_api.constants import HeatPumpHeatRequest
from keba_keenergy_api.constants import HeatPumpOperatingMode
from keba_keenergy_api.constants import HotWaterTankHeatRequest
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.constants import SystemOperatingMode
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.error import APIError


class TestSystemSection:
    @pytest.mark.asyncio
    async def test_get_positions(self) -> None:
        """Test get positions for heat pumps, heating circuits and hot water tanks."""
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
                        "value": "2",
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
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: Position = await client.system.get_positions()

            assert isinstance(response, Position)
            assert response.heat_pump == 2  # noqa: PLR2004
            assert response.heat_circuit == 1
            assert response.hot_water_tank == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}]'
                ),
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_info(self) -> None:
        """Test get system information."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/swupdate?action=getSystemInstalled",
                payload=[
                    {
                        "ret": "OK",
                        "name": "KeEnergy.MTec",
                        "version": "2.2.2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: dict[str, Any] = await client.system.get_info()

            assert isinstance(data, dict)
            assert data == {
                "name": "KeEnergy.MTec",
                "version": "2.2.2",
            }

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/swupdate?action=getSystemInstalled",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_device_info(self) -> None:
        """Test get device info from hardware."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/deviceControl?action=getDeviceInfo",
                payload=[
                    {
                        "ret": "OK",
                        "revNo": 2,
                        "orderNo": 12345678,
                        "serNo": 12345678,
                        "name": "MOCKED-NAME",
                        "variantNo": 0,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: dict[str, Any] = await client.system.get_device_info()

            assert isinstance(response, dict)
            assert response == {
                "revNo": 2,
                "orderNo": 12345678,
                "serNo": 12345678,
                "name": "MOCKED-NAME",
                "variantNo": 0,
            }

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/deviceControl?action=getDeviceInfo",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_hot_water_tanks(self) -> None:
        """Test get number of hot water tanks."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                        "value": "2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_number_of_hot_water_tanks()

            assert isinstance(data, int)
            assert data == 2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_heat_pumps(self) -> None:
        """Test get number of heat pumps."""
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
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_number_of_heat_pumps()

            assert isinstance(data, int)
            assert data == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_heating_circuits(self) -> None:
        """Test get number of heating circuits."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                        "value": "3",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_number_of_heating_circuits()

            assert isinstance(data, int)
            assert data == 3  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 1, "summer"), (False, 2, 2)],
    )
    async def test_get_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get operating mode for system."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.param.operatingMode",
                        "attributes": {
                            "formatId": "fmtOperatingMode",
                            "longText": "Operating mode",
                            "lowerLimit": "-1",
                            "unitId": "Enum",
                            "upperLimit": "4",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.system.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("summer", 1), ("AUTO_HEAT", 2), (SystemOperatingMode.AUTO_COOL.value, 3)],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int | str,
        expected_value: int,
    ) -> None:
        """Test set operating mode for system."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.system.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.param.operatingMode", "value": "%s"}]'  # noqa: UP031
                % expected_value,
                method="POST",
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
        """Test set operating mode for system."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.system.set_operating_mode(operating_mode)

            assert str(error.value) == (
                "Invalid value! Allowed values are "
                "['SETUP', '-1', 'STANDBY', '0', 'SUMMER', '1', 'AUTO_HEAT', '2', 'AUTO_COOL', '3', 'AUTO', '4']"
            )

            mock_keenergy_api.assert_not_called()


class TestHotWaterTankSection:
    @pytest.mark.asyncio
    async def test_get_current_temperature(self) -> None:
        """Test get current temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.",
                            "lowerLimit": "20",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "58.900002",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_current_temperature()

            assert isinstance(data, float)
            assert data == 58.9  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 3, "heat_up"), (False, 3, 3)],
    )
    async def test_get_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHotWaterTank",
                            "longText": "Op.mode",
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
            data: int | str = await client.hot_water_tank.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value"),
        [(True, 10)],
    )
    async def test_get_invalid_human_readable_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
    ) -> None:
        """Test get invalid human readable operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHotWaterTank",
                            "longText": "Op.mode",
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

            with pytest.raises(APIError) as error:
                await client.hot_water_tank.get_operating_mode(human_readable=human_readable)

            assert str(error.value) == (
                "Can't convert value to human readable value! "
                "{'name': 'APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode', "
                "'attributes': {'formatId': 'fmtHotWaterTank', 'longText': 'Op.mode', "
                "'lowerLimit': '0', 'unitId': 'Enum', 'upperLimit': '32767'}, 'value': '10'}"
            )

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("off", 0), ("OFF", 0), (HotWaterTankOperatingMode.HEAT_UP.value, 3)],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int | str,
        expected_value: int,
    ) -> None:
        """Test set operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.hot_water_tank.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "value": "%s"}]'  # noqa: UP031
                % expected_value,
                method="POST",
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
        """Test set operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.hot_water_tank.set_operating_mode(operating_mode)

            assert str(error.value) == (
                "Invalid value! Allowed values are ['OFF', '0', 'AUTO', '1', 'ON', '2', 'HEAT_UP', '3']"
            )

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_min_target_temperature(self) -> None:
        """Test get min target temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "50",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.hot_water_tank.get_min_target_temperature()

            assert isinstance(data, int)
            assert data == 0

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_max_target_temperature(self) -> None:
        """Test get max target temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "50",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.hot_water_tank.get_max_target_temperature()

            assert isinstance(data, int)
            assert data == 52  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_standby_temperature(self) -> None:
        """Test get standby temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Sup.temp.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "0",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_standby_temperature()

            assert isinstance(data, float)
            assert data == 0.0

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_standby_temperature(self) -> None:
        """Test set standby temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.hot_water_tank.set_standby_temperature(10)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "10"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature(self) -> None:
        """Test get target temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "47",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_target_temperature()

            assert isinstance(data, float)
            assert data == 47.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature(self) -> None:
        """Test set target temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.hot_water_tank.set_target_temperature(47)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "value": "47"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HotWaterTankHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, HotWaterTankHeatRequest.OFF.value, 0),
        ],
    )
    async def test_get_heat_request(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test get heat request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].values.heatRequestTop",
                        "attributes": {},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.hot_water_tank.get_heat_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].values.heatRequestTop", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HotWaterTankHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, HotWaterTankHeatRequest.OFF.value, 0),
        ],
    )
    async def test_get_hot_water_flow(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test get hot water flow."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterFlow.values.actValue",
                        "attributes": {
                            "longText": "FWM flow switch",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.hot_water_tank.get_hot_water_flow(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterFlow.values.actValue", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_fresh_water_module_temperature(self) -> None:
        """Test get fresh water module temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "FWM temp.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "30",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_fresh_water_module_temperature()

            assert isinstance(data, float)
            assert data == 30.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterTemp.values.actValue", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )


class TestHeatPumpSection:
    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
        """Test get name."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].param.name",
                        "attributes": {
                            "longText": "Name",
                        },
                        "value": "WPS26",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.heat_pump.get_name()

            assert isinstance(data, str)
            assert data == "WPS26"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].param.name", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 1, "flow"), (False, 1, 1)],
    )
    async def test_get_state(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: int | str,
    ) -> None:
        """Test get state."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState",
                        "attributes": {
                            "formatId": "fmtHPState",
                            "longText": "State",
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
            data: int | str = await client.heat_pump.get_state(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 0, "off"), (False, 2, 2)],
    )
    async def test_get_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHPOpMode",
                            "longText": "Operating mode",
                            "lowerLimit": "0",
                            "unitId": "Enum",
                            "upperLimit": "2",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("off", 0), ("ON", 1), (HeatPumpOperatingMode.BACKUP.value, 2)],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int | str,
        expected_value: int,
    ) -> None:
        """Test set operating mode for system."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_pump.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].param.operatingMode", "value": "%s"}]'  # noqa: UP031
                % expected_value,
                method="POST",
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
        """Test set operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.heat_pump.set_operating_mode(operating_mode)

            assert str(error.value) == "Invalid value! Allowed values are ['OFF', '0', 'ON', '1', 'BACKUP', '2']"

            mock_keenergy_api.assert_not_called()

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
    async def test_get_compressor_use_night_speed(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get compressor use night speed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.useDayNightSpeed",
                        "attributes": {
                            "longText": "Day/Night switch",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.get_compressor_use_night_speed(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.useDayNightSpeed", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("mode", "expected_value"),
        [
            ("off", "0"),
            ("ON", "1"),
            (HeatPumpCompressorUseNightSpeed.ON.value, "1"),
            (HeatPumpCompressorUseNightSpeed.OFF.value, "0"),
        ],
    )
    async def test_set_compressor_use_night_speed(
        self,
        mode: int | str,
        expected_value: str,
    ) -> None:
        """Test set compressor use night speed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_pump.set_compressor_use_night_speed(mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.useDayNightSpeed", "value": "%s"}]'  # noqa: E501, UP031
                % expected_value,
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_compressor_use_night_speed(
        self,
        operating_mode: int | str,
    ) -> None:
        """Test set operating mode."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.heat_pump.set_compressor_use_night_speed(operating_mode)

            assert str(error.value) == "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_compressor_night_speed(self) -> None:
        """Test get compressor night speed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Max. pwr. limit night",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.5",
                        },
                        "value": "0.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor_night_speed()

            assert isinstance(data, float)
            assert data == 0.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_compressor_night_speed(self) -> None:
        """Test set compressor night speed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_pump.set_compressor_night_speed(0.6)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight", "value": "0.6"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_min_compressor_night_speed(self) -> None:
        """Test get min compressor night speed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Max. pwr. limit night",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.5",
                        },
                        "value": "0.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_min_compressor_night_speed()

            assert isinstance(data, float)
            assert data == 0.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_max_compressor_night_speed(self) -> None:
        """Test get max compressor night speed."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Max. pwr. limit night",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.5",
                        },
                        "value": "0.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_max_compressor_night_speed()

            assert isinstance(data, float)
            assert data == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatPumpPowerCtrl.param.maxPowerScaledNight", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_circulation_pump(self) -> None:
        """Test get circulation pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Circulation pump",
                            "lowerLimit": "0.0",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                        },
                        "value": "0.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_circulation_pump()

            assert isinstance(data, float)
            assert data == 0.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_flow_temperature(self) -> None:
        """Test get flow temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.200001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_flow_temperature()

            assert isinstance(data, float)
            assert data == 24.2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_return_flow_temperature(self) -> None:
        """Test get return flow temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Reflux temp.",
                            "unitId": "Temp",
                        },
                        "value": "23.200001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_return_flow_temperature()

            assert isinstance(data, float)
            assert data == 23.2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_source_input_temperature(self) -> None:
        """Test get source input temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Source in temp.",
                            "unitId": "Temp",
                        },
                        "value": "22.700001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_input_temperature()

            assert isinstance(data, float)
            assert data == 22.7  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_source_output_temperature(self) -> None:
        """Test get source output temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Source out temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.6",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_output_temperature()

            assert isinstance(data, float)
            assert data == 24.6  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_input_temperature(self) -> None:
        """Test get compressor input temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Comp. in temp.",
                            "unitId": "Temp",
                        },
                        "value": "26.4",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor_input_temperature()

            assert isinstance(data, float)
            assert data == 26.4  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_output_temperature(self) -> None:
        """Test get compressor output temperature."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Comp. out temp.",
                            "unitId": "Temp",
                        },
                        "value": "26.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor_output_temperature()

            assert isinstance(data, float)
            assert data == 26.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor(self) -> None:
        """Test get compressor."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Compressor",
                            "lowerLimit": "0.0",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                        },
                        "value": "0.3",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor()

            assert isinstance(data, float)
            assert data == 0.3  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_high_pressure(self) -> None:
        """Test get high pressure."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "High pressure",
                            "unitId": "PressBar",
                        },
                        "value": "15.018749",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_high_pressure()

            assert isinstance(data, float)
            assert data == 15.02  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_low_pressure(self) -> None:
        """Test get low pressure."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Low pressure",
                            "unitId": "PressBar",
                        },
                        "value": "14.8125",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_low_pressure()

            assert isinstance(data, float)
            assert data == 14.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHeatRequest.OFF.value, 0),
        ],
    )
    async def test_get_heat_request(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test get heat request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.request",
                        "attributes": {},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.get_heat_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.request", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_power(self) -> None:
        """Test get compressor power."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].ElectricEnergyMeter.values.power",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Power input",
                            "unitId": "Pwr",
                        },
                        "value": "5.52",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor_power()

            assert isinstance(data, float)
            assert data == 5.52  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].ElectricEnergyMeter.values.power", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_power(self) -> None:
        """Test get heating power."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HeatMeter.values.power",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Heating power",
                            "unitId": "Pwr",
                        },
                        "value": "3.22",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_heating_power()

            assert isinstance(data, float)
            assert data == 3.22  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HeatMeter.values.power", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_power(self) -> None:
        """Test get hot water power."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HotWaterMeter.values.power",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Hot water power",
                            "unitId": "Pwr",
                        },
                        "value": "2.77",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_hot_water_power()

            assert isinstance(data, float)
            assert data == 2.77  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HotWaterMeter.values.power", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cop(self) -> None:
        """Test get COP."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.COP",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "COP",
                        },
                        "value": "2.55",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_cop()

            assert isinstance(data, float)
            assert data == 2.55  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.COP", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_energy(self) -> None:
        """Test get heating energy."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.heating.energy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Heating energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "8.43",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_heating_energy()

            assert isinstance(data, float)
            assert data == 8.43  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.heating.energy", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_energy_consumption(self) -> None:
        """Test get heating energy consumption."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.heating.electricalenergy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Heat el. energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "7.33",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_heating_energy_consumption()

            assert isinstance(data, float)
            assert data == 7.33  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.heating.electricalenergy", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_spf(self) -> None:
        """Test get heating SPF."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatioHeat",
                        "attributes": {
                            "longText": "SPF heating",
                        },
                        "value": "3.32",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_heating_spf()

            assert isinstance(data, float)
            assert data == 3.32  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatioHeat", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_energy(self) -> None:
        """Test get cooling energy."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.cooling.energy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Cooling energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "7.21",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_cooling_energy()

            assert isinstance(data, float)
            assert data == 7.21  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.cooling.energy", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_energy_consumption(self) -> None:
        """Test get colling energy consumption."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.cooling.electricalenergy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Cool el. energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "8.72",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_cooling_energy_consumption()

            assert isinstance(data, float)
            assert data == 8.72  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.cooling.electricalenergy", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_spf(self) -> None:
        """Test get cooling SPF."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatioCool",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "SPF cooling",
                        },
                        "value": "4.22",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_cooling_spf()

            assert isinstance(data, float)
            assert data == 4.22  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatioCool", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_energy(self) -> None:
        """Test get hot water energy."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.domHotWater.energy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Dom. HW energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "7.86",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_hot_water_energy()

            assert isinstance(data, float)
            assert data == 7.86  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.domHotWater.energy", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_energy_consumption(self) -> None:
        """Test get hot water energy consumption."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.domHotWater.electricalenergy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Dom.HW el. energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "2.77",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_hot_water_energy_consumption()

            assert isinstance(data, float)
            assert data == 2.77  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.domHotWater.electricalenergy", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_spf(self) -> None:
        """Test get hot water SPF."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatioDomHotWater",
                        "attributes": {
                            "longText": "SPF DHW",
                        },
                        "value": "2.50",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_hot_water_spf()

            assert isinstance(data, float)
            assert data == 2.50  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatioDomHotWater", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_thermal_energy(self) -> None:
        """Test get total thermal energy."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.energy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "8.22",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_total_thermal_energy()

            assert isinstance(data, float)
            assert data == 8.22  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.energy", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_energy_consumption(self) -> None:
        """Test get total energy consumption."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.electricalenergy",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "El. energy",
                            "unitId": "kWhwithoutConv",
                        },
                        "value": "5.21",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_total_energy_consumption()

            assert isinstance(data, float)
            assert data == 5.21  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].consumption.electricalenergy", "attr": "1"}]',  # noqa: E501
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_spf(self) -> None:
        """Test get total SPF."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatio",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "SPF general",
                        },
                        "value": "2.43",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_total_spf()

            assert isinstance(data, float)
            assert data == 2.43  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sStatisticalData.heatpump[0].EnergyEfficiencyRatio", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHasPassiveCooling.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasPassiveCooling.OFF.value, 0),
        ],
    )
    async def test_has_passive_cooling(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test has passive cooling."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.heatpump[0].hasPassiveCooling",
                        "attributes": {"longText": "With passive cooling,"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_passive_cooling(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.heatpump[0].hasPassiveCooling", "attr": "1"}]',
                method="POST",
                ssl=False,
            )


class TestHeatCircuitSection:
    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
        """Test get name."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatCircuitHasRoomTemperature.ON.value, 1),
            (True, "false", "off"),
            (False, HeatCircuitHasRoomTemperature.OFF.value, 0),
        ],
    )
    async def test_has_room_temperature(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test has room temperature."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_room_temperature(self) -> None:
        """Test get room temperature."""
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
            assert data == 22.43  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatCircuitHasRoomTemperature.ON.value, 1),
            (True, "false", "off"),
            (False, HeatCircuitHasRoomTemperature.OFF.value, 0),
        ],
    )
    async def test_has_room_humidity(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test has room humidity."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_room_humidity(self) -> None:
        """Test get room humidity."""
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
            assert data == 53  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].humidityRoom.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_dew_point(self) -> None:
        """Test get dew point."""
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
            assert data == 13.10  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].dewPoint.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_flow_temperature_setpoint(self) -> None:
        """Test get flow temperature setpoint."""
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
            assert data == 26.25  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.flowSetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature(self) -> None:
        """Test get target temperature."""
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
            assert data == 22.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_day(self) -> None:
        """Test get target temperature for the day."""
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
            assert data == 23.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_day(self) -> None:
        """Test set target temperature for the day."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_limit_day(self) -> None:
        """Test get day heating limit for the day."""
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
            assert data == 16.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_night(self) -> None:
        """Test get target temperature for the night."""
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
            assert data == 23.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_night(self) -> None:
        """Test set target temperature for the night."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_limit_night(self) -> None:
        """Test get heating limit for the night."""
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
            assert data == 16.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_away(self) -> None:
        """Test get target temperature when away."""
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
            assert data == 14.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_away(self) -> None:
        """Test set target temperature when away."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_offset(self) -> None:
        """Test get target temperature offset."""
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
            assert data == 2.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_offset(self) -> None:
        """Test set target temperature offset."""
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
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 3, "night"), (False, 3, 3)],
    )
    async def test_get_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get operating mode."""
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
        """Test set operating mode heat circuit."""
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
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "value": "%s"}]'  # noqa: UP031
                % expected_value,
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_operating_mode(
        self,
        operating_mode: int,
    ) -> None:
        """Test set operating mode heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.heat_circuit.set_operating_mode(operating_mode)

            assert str(error.value) == (
                "Invalid value! Allowed values are "
                "['OFF', '0', 'AUTO', '1', 'DAY', '2', 'NIGHT', '3', 'HOLIDAY', '4', 'PARTY', '5', 'EXTERNAL', '8', "
                "'ROOM_CONTROL', '9']"
            )

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value"),
        [(True, "16")],
    )
    async def test_get_invalid_heat_request(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
    ) -> None:
        """Test get heat request."""
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

            with pytest.raises(APIError) as error:
                await client.heat_circuit.get_heat_request(human_readable=human_readable)

            assert str(error.value) == (
                "Can't convert value to human readable value! "
                "{'name': 'APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest', "
                "'attributes': {'unitId': 'Enum', 'upperLimit': '6', 'lowerLimit': '0'}, 'value': '16'}"
            )

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest", "attr": "1"}]',
                method="POST",
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
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test get heat request."""
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
                ssl=False,
            )

    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatCircuitExternalCoolRequest.ON.value, 1),
            (True, "false", "off"),
            (False, HeatCircuitExternalCoolRequest.OFF.value, 0),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_external_cool_request(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test get external cool request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.external.coolRequest",
                        "attributes": {"longText": "Ext. cool request"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_external_cool_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.external.coolRequest", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatCircuitExternalHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, HeatCircuitExternalHeatRequest.OFF.value, 0),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_external_heat_request(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        """Test get external heat request."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.external.heatRequest",
                        "attributes": {"longText": "Ext. cool request"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_external_heat_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.external.heatRequest", "attr": "1"}]',
                method="POST",
                ssl=False,
            )
