import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HotWaterTankCirculationPumpState
from keba_keenergy_api.constants import HotWaterTankHeatRequest
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.error import APIError


class TestHotWaterTankSection:
    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.name",
                        "attributes": {
                            "longText": "Name",
                        },
                        "value": "Boiler",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.hot_water_tank.get_name()

            assert isinstance(data, str)
            assert data == "Boiler"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.name", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_current_temperature(self) -> None:
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
                auth=None,
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
                auth=None,
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

            with pytest.raises(
                APIError,
                match=(
                    "Can't convert value to human readable value! "
                    r"{'name': 'APPL\.CtrlAppl\.sParam.hotWaterTank\[0]\.param\.operatingMode', "
                    r"'attributes': {'formatId': 'fmtHotWaterTank', 'longText': 'Op\.mode', "
                    "'lowerLimit': '0', 'unitId': 'Enum', 'upperLimit': '32767'}, 'value': '10'}"
                ),
            ):
                await client.hot_water_tank.get_operating_mode(human_readable=human_readable)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                auth=None,
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_max_target_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_standby_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_standby_temperature(self) -> None:
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
                auth=None,
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_fresh_water_module_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_fresh_water_module_pump_speed(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterPump.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "FWM pump",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.0",
                        },
                        "value": "0.40000001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_fresh_water_module_pump_speed()

            assert isinstance(data, float)
            assert data == 0.4  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].FreshWater.freshWaterPump.values.setValueScaled", '
                    '"attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_circulation_return_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].circTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Circ. reflux temp.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "-100",
                        },
                        "value": "47.44",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_circulation_return_temperature()

            assert isinstance(data, float)
            assert data == 47.44  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=('[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].circTemp.values.actValue", "attr": "1"}]'),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HotWaterTankCirculationPumpState.ON.value, 1),
            (True, "false", "off"),
            (False, HotWaterTankCirculationPumpState.OFF.value, 0),
        ],
    )
    async def test_get_circulation_pump_state(
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
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].circPump.pump.values.setValueB",
                        "attributes": {
                            "longText": "Pumps nom. value Circ.",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.hot_water_tank.get_circulation_pump_state(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=('[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].circPump.pump.values.setValueB", "attr": "1"}]'),
                method="POST",
                auth=None,
                ssl=False,
            )
