import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI


@pytest.mark.happy
class TestHappyPathPhotovoltaicSection:
    @pytest.mark.asyncio
    async def test_get_excess_power(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.power",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Actual excess power",
                            "unitId": "Pwr",
                        },
                        "value": "23.234",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.photovoltaics.get_excess_power()

            assert isinstance(data, float)
            assert data == 23.23  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.power", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_daily_energy(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.heatDay",
                        "attributes": {
                            "formatId": "fmt6p1",
                            "longText": "Energy per day",
                            "unitId": "kWh",
                        },
                        "value": "49.394",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.photovoltaics.get_daily_energy()

            assert isinstance(data, float)
            assert data == 49.39  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.heatDay", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_energy(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.photovoltaics.get_total_energy()

            assert isinstance(data, float)
            assert data == 349442.23  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat", "attr": "1"}]',  # noqa: E501
                method="POST",
                auth=None,
                ssl=False,
            )
