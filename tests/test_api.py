import asyncio
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
from keba_keenergy_api.constants import System
from keba_keenergy_api.endpoints import ValueResponse
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import AuthenticationError


class TestKebaKeEnergyAPI:
    @pytest.mark.asyncio
    async def test_api(self) -> None:
        """Test api without session."""
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
        """Test api with seassion."""
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
        """Test api with basic auth."""
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
            "expected_data",
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
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
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
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.",
                            "lowerLimit": "20",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "40.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.extHeatSource[0].values.setTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "20",
                        },
                        "value": "22.56",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Acc. energy",
                            "unitId": "kWh",
                        },
                        "value": "349442.23",
                    },
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].values.setTemp", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat", "attr": "1"}]'  # noqa: E501
                ),
                {
                    "system": {
                        "hot_water_tank_numbers": {"value": 2, "attributes": {"lower_limit": "0", "upper_limit": "4"}},
                    },
                    "buffer_tank": {},
                    "hot_water_tank": {
                        "current_temperature": [
                            {
                                "attributes": {"lower_limit": "20", "upper_limit": "90"},
                                "value": 40.81,
                            },
                        ],
                    },
                    "heat_pump": {},
                    "heat_circuit": {},
                    "solar_circuit": {},
                    "external_heat_source": {
                        "target_temperature": [
                            {
                                "attributes": {"lower_limit": "20", "upper_limit": "90"},
                                "value": 22.56,
                            },
                        ],
                    },
                    "photovoltaic": {
                        "total_energy": {
                            "attributes": {},
                            "value": 349442.23,
                        },
                    },
                },
            ),
            (
                [HeatCircuit.TARGET_TEMPERATURE, HeatPump.FLOW_TEMPERATURE],
                [0, 1, 3],
                None,
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "10.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "11.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.200001",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "23.200001",
                    },
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue", "attr": "1"}]'
                ),
                {
                    "system": {},
                    "buffer_tank": {},
                    "hot_water_tank": {},
                    "heat_pump": {
                        "flow_temperature": [{"value": 24.2, "attributes": {}}, {"value": 23.2, "attributes": {}}],
                    },
                    "heat_circuit": {
                        "target_temperature": [
                            {"value": 10.81, "attributes": {"lower_limit": "10", "upper_limit": "90"}},
                            {"value": 11.81, "attributes": {"lower_limit": "10", "upper_limit": "90"}},
                        ],
                    },
                    "solar_circuit": {},
                    "external_heat_source": {},
                    "photovoltaic": {},
                },
            ),
            (
                [
                    System.OUTDOOR_TEMPERATURE,
                    HeatCircuit.TARGET_TEMPERATURE,
                    HeatPump.FLOW_TEMPERATURE,
                    ExternalHeatSource.TARGET_TEMPERATURE,
                ],
                None,
                [
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
                        "value": "0",
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
                        "value": "0",
                    },
                ],
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "17.54",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "10.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.200001",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "23.200001",
                    },
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue", "attr": "1"}]'
                ),
                {
                    "system": {
                        "outdoor_temperature": {
                            "value": 17.54,
                            "attributes": {"lower_limit": "-100", "upper_limit": "100"},
                        },
                    },
                    "buffer_tank": {},
                    "hot_water_tank": {},
                    "heat_pump": {
                        "flow_temperature": [{"value": 24.2, "attributes": {}}, {"value": 23.2, "attributes": {}}],
                    },
                    "heat_circuit": {
                        "target_temperature": [
                            {"value": 10.81, "attributes": {"lower_limit": "10", "upper_limit": "90"}},
                        ],
                    },
                    "solar_circuit": {},
                    "external_heat_source": {},
                    "photovoltaic": {},
                },
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
                [
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
                        "value": "2",
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
                        "value": "0",
                    },
                ],
                [
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
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].collectorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Source temp.",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "20",
                        },
                        "value": "22.426912",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[1].collectorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Source temp.",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "20",
                        },
                        "value": "22.426912",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.1",
                            "unitId": "Temp",
                        },
                        "value": "55.753",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.2",
                            "unitId": "Temp",
                        },
                        "value": "45.753",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[2].referenceTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.1",
                            "unitId": "Temp",
                        },
                        "value": "53.753",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[3].referenceTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.2",
                            "unitId": "Temp",
                        },
                        "value": "43.753",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom. 1",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "35",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom. 2",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "45",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom. 1",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "35",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom. 2",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "45",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest",
                        "attributes": {
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": "false",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[1].values.heatRequest",
                        "attributes": {
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": "true",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.heatRequest",
                        "attributes": {
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": "false",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[3].values.heatRequest",
                        "attributes": {
                            "unitId": "Enum",
                            "upperLimit": "6",
                            "lowerLimit": "0",
                        },
                        "value": "true",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState",
                        "attributes": {
                            "formatId": "fmtHPSubState",
                            "longText": "Substate",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                            "lowerLimit": "0",
                        },
                        "value": "21",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[1].values.heatpumpSubState",
                        "attributes": {
                            "formatId": "fmtHPSubState",
                            "longText": "Substate",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                            "lowerLimit": "0",
                        },
                        "value": "5",
                    },
                ],
                '[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].topTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].collectorTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.solarCircuit[1].collectorTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].referenceTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].referenceTemp.values.actValue", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].values.heatRequest", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].values.heatRequest", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState", "attr": "1"}, '
                '{"name": "APPL.CtrlAppl.sParam.heatpump[1].values.heatpumpSubState", "attr": "1"}]',
                {
                    "system": {},
                    "buffer_tank": {
                        "current_top_temperature": [
                            {
                                "attributes": {
                                    "lower_limit": "5",
                                    "upper_limit": "90",
                                },
                                "value": 45.03,
                            },
                        ],
                    },
                    "hot_water_tank": {},
                    "heat_pump": {
                        "substate": [
                            {
                                "attributes": {
                                    "lower_limit": "0",
                                    "upper_limit": "32767",
                                },
                                "value": "pressure_equalization",
                            },
                            {
                                "attributes": {
                                    "lower_limit": "0",
                                    "upper_limit": "32767",
                                },
                                "value": "pressure_equalization",
                            },
                        ],
                    },
                    "heat_circuit": {},
                    "solar_circuit": {
                        "current_temperature": [
                            [
                                {
                                    "attributes": {},
                                    "value": 55.75,
                                },
                                {
                                    "attributes": {},
                                    "value": 45.75,
                                },
                            ],
                            [
                                {
                                    "attributes": {},
                                    "value": 53.75,
                                },
                                {
                                    "attributes": {},
                                    "value": 43.75,
                                },
                            ],
                        ],
                        "heat_request": [
                            [
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "6",
                                    },
                                    "value": "off",
                                },
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "6",
                                    },
                                    "value": "on",
                                },
                            ],
                            [
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "6",
                                    },
                                    "value": "off",
                                },
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "6",
                                    },
                                    "value": "on",
                                },
                            ],
                        ],
                        "target_temperature": [
                            [
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "90",
                                    },
                                    "value": 35.0,
                                },
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "90",
                                    },
                                    "value": 45.0,
                                },
                            ],
                            [
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "90",
                                    },
                                    "value": 35.0,
                                },
                                {
                                    "attributes": {
                                        "lower_limit": "0",
                                        "upper_limit": "90",
                                    },
                                    "value": 45.0,
                                },
                            ],
                        ],
                        "source_temperature": [
                            {
                                "attributes": {
                                    "lower_limit": "20",
                                    "upper_limit": "90",
                                },
                                "value": 22.43,
                            },
                            {
                                "attributes": {
                                    "lower_limit": "20",
                                    "upper_limit": "90",
                                },
                                "value": 22.43,
                            },
                        ],
                    },
                    "external_heat_source": {},
                    "photovoltaic": {},
                },
            ),
        ],
    )
    async def test_read_data(
        self,
        section: Section,
        position: int | list[int] | None,
        option_payload: list[dict[str, str]] | None,
        payload: list[dict[str, str]],
        expected_data: str,
        expected_response: dict[str, ValueResponse],
    ) -> None:
        """Test read multiple data."""
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

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: dict[str, ValueResponse] = await client.read_data(
                request=section,
                position=position,
            )

            assert isinstance(response, dict)
            assert response == expected_response

            mock_keenergy_api.assert_called_with(
                url="http://mocked-host/var/readWriteVars",
                data=expected_data,
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
                    HotWaterTank.STANDBY_TEMPERATURE: [
                        10,
                    ],
                    HotWaterTank.TARGET_TEMPERATURE: (
                        45,
                        44,
                    ),
                },
                (
                    "["
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", '
                    '"value": "10"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", '
                    '"value": "45"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[1].param.normalSetTempMax.value", '
                    '"value": "44"}'
                    "]"
                ),
            ),
        ],
    )
    async def test_write_data(self, section: dict[Section, Any], expected_data: str) -> None:
        """Test write multiple data."""
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

    def test_invalid_credentials(self) -> None:
        """Test invalid credentials."""
        loop = asyncio.get_event_loop()

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

            with pytest.raises(AuthenticationError) as error:
                loop.run_until_complete(client.system.get_outdoor_temperature())

            assert str(error.value) == "401 Unauthorized: No permission -- see authorization schemes"

    def test_api_status_4xx(self) -> None:
        """Test api status 4xx."""
        loop = asyncio.get_event_loop()

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

            with pytest.raises(APIError) as error:
                loop.run_until_complete(client.system.get_outdoor_temperature())

            assert str(error.value) == "405 Method Not Allowed: Specified method is invalid for this resource - {}"

    def test_api_client_error(self) -> None:
        """Test api client error."""
        loop = asyncio.get_event_loop()

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                exception=ServerTimeoutError("Server took too long to respond"),
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                loop.run_until_complete(client.system.get_outdoor_temperature())

            assert str(error.value) == "Server took too long to respond"

    def test_api_error(self) -> None:
        """Test api error."""
        loop = asyncio.get_event_loop()

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload={"developerMessage": "mocked-error"},
                headers={"Content-Type": "application/json;charset=utf-8"},
                status=500,
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                loop.run_until_complete(client.system.get_outdoor_temperature())

            assert str(error.value) == "500 Internal Server Error: Server got itself in trouble - mocked-error"
