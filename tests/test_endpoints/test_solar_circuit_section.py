import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import SolarCircuitConsumer1PrioritySolar
from keba_keenergy_api.constants import SolarCircuitHeatRequest
from keba_keenergy_api.constants import SolarCircuitOperatingMode
from keba_keenergy_api.error import APIError


class TestSolarCircuitSection:
    @pytest.mark.asyncio
    async def test_get_name(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].param.name",
                        "attributes": {
                            "longText": "Name",
                        },
                        "value": "Diff. Regler 1",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.solar_circuit.get_name()

            assert isinstance(data, str)
            assert data == "Diff. Regler 1"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].param.name", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 1, "on"), (False, 0, 0)],
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
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtSolarOpMode",
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
            data: int | str = await client.solar_circuit.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("on", 1), ("OFF", 0), (SolarCircuitOperatingMode.ON.value, 1)],
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
            await client.solar_circuit.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].param.operatingMode", "value": "%s"}]'  # noqa: UP031
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
        operating_mode: int,
    ) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1']"):
                await client.solar_circuit.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, "true", "on"), (False, "false", 0)],
    )
    async def test_get_priority_1_before_2(
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
                        "name": "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[0]",
                        "attributes": {
                            "longText": "Priority 1 bef. 2",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.solar_circuit.get_priority_1_before_2(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[0]", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("on", (1, 14)), ("OFF", (0, 15)), (SolarCircuitConsumer1PrioritySolar.ON.value, (1, 14))],
    )
    async def test_set_priority_1_before_2(
        self,
        operating_mode: int | str,
        expected_value: tuple[int, ...],
    ) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.solar_circuit.set_priority_1_before_2(operating_mode, position=2)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.hmiRetainData.consumer1PrioritySolar[1]", "value": "%s"}, '  # noqa: UP031
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].param.priority", "value": "%s"}]' % expected_value
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_priority_1_before_2(
        self,
        operating_mode: int,
    ) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1']"):
                await client.solar_circuit.set_priority_1_before_2(operating_mode, position=2)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_source_temperature(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_source_temperature()

            assert isinstance(data, float)
            assert data == 22.43  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].collectorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_pump_1_speed(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].values.pump1",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Pump 1",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.0",
                        },
                        "value": "0.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_pump_1_speed()

            assert isinstance(data, float)
            assert data == 0.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].values.pump1", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_pump_2_speed(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].values.pump2",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Pump 2",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.0",
                        },
                        "value": "0.55",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_pump_2_speed()

            assert isinstance(data, float)
            assert data == 0.55  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].values.pump2", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_current_temperature_1(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                            "longText": "Temp. act.1",
                            "unitId": "Temp",
                        },
                        "value": "25.753",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_current_temperature_1()

            assert isinstance(data, float)
            assert data == 55.75  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_current_temperature_2(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                            "longText": "Temp. act.1",
                            "unitId": "Temp",
                        },
                        "value": "25.753",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_current_temperature_2()

            assert isinstance(data, float)
            assert data == 25.75  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_1(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom. 1",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "55",
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
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_target_temperature_1()

            assert isinstance(data, float)
            assert data == 55  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_1(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.solar_circuit.set_target_temperature_1(47)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "value": "47"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_2(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom. 1",
                            "unitId": "Temp",
                            "upperLimit": "90",
                            "lowerLimit": "0",
                        },
                        "value": "55",
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
                        "value": "35",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_target_temperature_2()

            assert isinstance(data, float)
            assert data == 35  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_2(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.solar_circuit.set_target_temperature_2(37)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value", "value": "37"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, SolarCircuitHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, SolarCircuitHeatRequest.OFF.value, 0),
        ],
    )
    async def test_get_heat_request_1(
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
                        "name": "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest",
                        "attributes": {
                            "longText": "Heat request 1",
                        },
                        "value": payload_value,
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest",
                        "attributes": {
                            "longText": "Heat request 2",
                        },
                        "value": "false" if payload_value == "true" else "true",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.solar_circuit.get_heat_request_1(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, SolarCircuitHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, SolarCircuitHeatRequest.OFF.value, 0),
        ],
    )
    async def test_get_heat_request_2(
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
                        "name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest",
                        "attributes": {
                            "longText": "Heat request 1",
                        },
                        "value": "false" if payload_value == "true" else "true",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest",
                        "attributes": {
                            "longText": "Heat request 2",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.solar_circuit.get_heat_request_2(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest", "attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_energy(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.accumulatedHeat",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Heat quantity",
                            "unitId": "kWh",
                            "upperLimit": "900000",
                            "lowerLimit": "0",
                        },
                        "value": "8.43",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_heating_energy()

            assert isinstance(data, float)
            assert data == 8.43  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.accumulatedHeat", "attr": "1"}]',
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
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.heatDay",
                        "attributes": {
                            "formatId": "fmt6p1",
                            "longText": "Energy per day",
                            "unitId": "kWh",
                        },
                        "value": "1.23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_daily_energy()

            assert isinstance(data, float)
            assert data == 1.23  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.heatDay", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_actual_power(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.power",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Act. power",
                            "unitId": "Pwr",
                        },
                        "value": "3.23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.solar_circuit.get_actual_power()

            assert isinstance(data, float)
            assert data == 3.23  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].heatMeter.values.power", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )
