from typing import Any

import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import SystemHasPhotovoltaics
from keba_keenergy_api.constants import SystemOperatingMode
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.error import APIError


@pytest.mark.happy
class TestHappyPathSystemSection:
    @pytest.mark.asyncio
    async def test_get_positions(self) -> None:
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

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: Position = await client.system.get_positions()

            assert isinstance(response, Position)
            assert response.heat_pump == 2  # noqa: PLR2004
            assert response.heat_circuit == 1
            assert response.solar_circuit == 1
            assert response.buffer_tank == 1
            assert response.hot_water_tank == 1
            assert response.external_heat_source == 1
            assert response.switch_valve == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_info(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hmi_info(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/swupdate?action=getHmiInstalled",
                payload=[
                    {
                        "ret": "OK",
                        "name": "KeEnergy.WebHmi_2.2.0.0",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: dict[str, Any] = await client.system.get_hmi_info()

            assert isinstance(data, dict)
            assert data == {
                "name": "KeEnergy.WebHmi_2.2.0.0",
            }

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/swupdate?action=getHmiInstalled",
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_device_info(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_buffer_tanks(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                        "value": "2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_number_of_buffer_tanks()

            assert isinstance(data, int)
            assert data == 2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_hot_water_tanks(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_heat_pumps(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_heating_circuits(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_external_heat_sources(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_number_of_external_heat_sources()

            assert isinstance(data, int)
            assert data == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_number_of_switch_valves(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves", "value": "1"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_number_of_switch_valves()

            assert isinstance(data, int)
            assert data == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, SystemHasPhotovoltaics.ON.value, 1),
            (True, "false", "off"),
            (False, SystemHasPhotovoltaics.OFF.value, 0),
        ],
    )
    async def test_has_photovoltaics(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.options.hasPhotovoltaics",
                        "attributes": {"longText": "With photovoltaics"},
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.system.has_photovoltaics(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.hasPhotovoltaics", "attr": "1"}]',
                method="POST",
                auth=None,
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cpu_usage(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sProcData.globalCpuTimePercent",
                        "attributes": {
                            "formatId": "fmt3p1",
                            "longText": "CPU usage",
                            "unitId": "Pct10",
                        },
                        "value": "27",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.system.get_cpu_usage()

            assert isinstance(data, float)
            assert data == 2.7  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sProcData.globalCpuTimePercent", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_webview_cpu_usage(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sProcData.processStatus[0].cpuTimePercent",
                        "attributes": {
                            "formatId": "fmt3p1",
                            "longText": "WebView CPU",
                            "unitId": "Pct10",
                        },
                        "value": "34",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.system.get_webview_cpu_usage()

            assert isinstance(data, float)
            assert data == 3.4  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sProcData.processStatus[0].cpuTimePercent", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_webserver_cpu_usage(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sProcData.processStatus[1].cpuTimePercent",
                        "attributes": {
                            "formatId": "fmt3p1",
                            "longText": "WebServer CPU",
                            "unitId": "Pct10",
                        },
                        "value": "67",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.system.get_webserver_cpu_usage()

            assert isinstance(data, float)
            assert data == 6.7  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sProcData.processStatus[1].cpuTimePercent", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_control_cpu_usage(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sProcData.processStatus[2].cpuTimePercent",
                        "attributes": {
                            "formatId": "fmt3p1",
                            "longText": "Ctrl CPU",
                            "unitId": "Pct10",
                        },
                        "value": "7",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.system.get_control_cpu_usage()

            assert isinstance(data, float)
            assert data == 0.7  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sProcData.processStatus[2].cpuTimePercent", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_ram_usage(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sProcData.RAMstatus.tmpfs",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Used Temporary Memory",
                            "unitId": "kB",
                        },
                        "value": "6432",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_ram_usage()

            assert isinstance(data, int)
            assert data == 6432  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sProcData.RAMstatus.tmpfs", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_free_ram(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sProcData.totFreeRAM",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Free RAM",
                            "unitId": "kB",
                        },
                        "value": "100060",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.system.get_free_ram()

            assert isinstance(data, int)
            assert data == 100060  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sProcData.totFreeRAM", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_timezone(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/dateTime?action=getTimeZone",
                payload={"timezone": "Europe/Vienna"},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: str = await client.system.get_timezone()

            assert isinstance(response, str)
            assert response == "Europe/Vienna"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/dateTime?action=getTimeZone",
                method="POST",
                auth=None,
                ssl=False,
            )


@pytest.mark.unhappy
class TestUnhappyPathSystemSection:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_operating_mode(
        self,
        operating_mode: int | str,
    ) -> None:
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
                    "Invalid value! Allowed values are "
                    r"\['SETUP', '-1', 'STANDBY', '0', 'SUMMER', '1', 'AUTO_HEAT', '2', 'AUTO_COOL', '3', 'AUTO', '4']"
                ),
            ):
                await client.system.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_not_called()
