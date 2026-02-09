import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatCircuitHasRoomTemperature
from keba_keenergy_api.constants import HeatCircuitHeatRequest
from keba_keenergy_api.constants import HeatCircuitHeatingCurve
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HeatCircuitUseHeatingCurve
from keba_keenergy_api.endpoints import HeatingCurvePoint
from keba_keenergy_api.endpoints import HeatingCurves
from keba_keenergy_api.error import APIError
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_expected_data
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_expected_response_1
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_expected_response_2
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_payload


class TestHeatCircuitSection:
    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_room_temperature(self) -> None:
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_room_humidity(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_dew_point(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_flow_temperature_setpoint(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_mixer_flow_temperature(self) -> None:
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
            assert data == 26.25  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.flowTemp.values.actValue", "attr": "1"}]',  # noqa: E501
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_mixer_return_flow_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.refluxTemp.values.actValue",
                        "value": "31.254391",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_mixer_return_flow_temperature()

            assert isinstance(data, float)
            assert data == 31.25  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.refluxTemp.values.actValue", "attr": "1"}]',  # noqa: E501
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_return_flow_temperature(self) -> None:
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
            assert data == 19.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempReflux.values.actValue", "attr": "1"}]',
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_selected_target_temperature(self) -> None:
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
            assert data == 21.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.selectedSetTemp", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_day(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_day(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_limit_day(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_night(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_night(self) -> None:

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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_limit_night(self) -> None:

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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_away(self) -> None:

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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_away(self) -> None:

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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_temperature_offset(self) -> None:

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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_target_temperature_offset(self) -> None:

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
                auth=None,
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
                auth=None,
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
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
    ) -> None:

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
                auth=None,
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
                auth=None,
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
        human_readable: bool,  # noqa: FBT001
        payload_value: str,
        expected_value: str,
    ) -> None:

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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_away_start_date(self) -> None:
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
            assert data == 1768690800  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.start", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_away_start_date(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_away_end_date(self) -> None:
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
            assert data == 1769036400  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.stop", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_away_end_date(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_curve_offset(self) -> None:
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
            assert data == 3.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveOffset", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_curve_offset(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_curve_slope(self) -> None:
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
            assert data == 0.25  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveGradient", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_curve_slope(self) -> None:
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
                auth=None,
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
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("mode", "expected_value"),
        [
            ("off", "0"),
            ("ON", "1"),
            (HeatCircuitUseHeatingCurve.ON.value, "1"),
            (HeatCircuitUseHeatingCurve.OFF.value, "0"),
        ],
    )
    async def test_set_use_heating_curve(
        self,
        mode: int | str,
        expected_value: str,
    ) -> None:
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
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab", '  # noqa: UP031
                    '"value": "%s"}]' % expected_value
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "mode",
        ["INVALID"],
    )
    async def test_set_invalid_use_heating_curve(self, mode: int | str) -> None:
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
    async def test_get_heating_curve(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("name", "expected_value"),
        [
            ("HC1", "HC1"),
            (HeatCircuitHeatingCurve.HC_FBH.name, "HC FBH"),
        ],
    )
    async def test_set_heating_curve(self, name: str, expected_value: str) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_heating_curve(name)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName", '  # noqa: UP031
                    '"value": "%s"}]' % expected_value
                ),
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name",
        ["INVALID"],
    )
    async def test_set_invalid_heating_curve(
        self,
        name: str,
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
                    r"\['HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC FBH', 'HC HK']"
                ),
            ):
                await client.heat_circuit.set_heating_curve(name)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        (
            "heating_curve",
            "payload",
            "expected_response",
            "expected_data",
        ),
        [
            (
                None,
                heating_curve_points_payload,
                heating_curve_points_expected_response_1,
                heating_curve_points_expected_data,
            ),
            (
                "HC1",
                heating_curve_points_payload,
                heating_curve_points_expected_response_2,
                heating_curve_points_expected_data,
            ),
        ],
    )
    async def test_get_heating_curve_points(
        self,
        heating_curve: str | None,
        payload: list[dict[str, str]],
        expected_response: HeatingCurves,
        expected_data: str,
    ) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: HeatingCurves = await client.heat_circuit.get_heating_curve_points(heating_curve)

            assert isinstance(response, dict)
            assert response == expected_response

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=expected_data,
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        (
            "heating_curve",
            "payload",
            "expected_data",
        ),
        [
            (
                "HC10",
                heating_curve_points_payload,
                heating_curve_points_expected_data,
            ),
        ],
    )
    async def test_get_invalide_heating_curve_points(
        self,
        heating_curve: str | None,
        payload: list[dict[str, str]],
        expected_data: str,
    ) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError, match='Heating curve "HC10" not found'):
                await client.heat_circuit.get_heating_curve_points(heating_curve)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=expected_data,
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_heating_curve_points(
        self,
    ) -> None:
        with aioresponses() as mock_keenergy_api:
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

            mock_keenergy_api.assert_called_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.linTabPool[0].name", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

            mock_keenergy_api.assert_called_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.linTabPool[0].noOfPoints", "value": "7"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[0].x", "value": "-20"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[0].y", "value": "35"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[1].x", "value": "-10"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[1].y", "value": "33"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[2].x", "value": "-5"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[2].y", "value": "32"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[3].x", "value": "0"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[3].y", "value": "30"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[4].x", "value": "5"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[4].y", "value": "28"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[5].x", "value": "10"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[5].y", "value": "27"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[6].x", "value": "20"}, '
                    '{"name": "APPL.CtrlAppl.sParam.linTabPool[0].points[6].y", "value": "25"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )
