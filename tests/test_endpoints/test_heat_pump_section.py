import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatPumpCompressorUseNightSpeed
from keba_keenergy_api.constants import HeatPumpHasCompressorFailure
from keba_keenergy_api.constants import HeatPumpHasPassiveCooling
from keba_keenergy_api.constants import HeatPumpHasSourceActuatorFailure
from keba_keenergy_api.constants import HeatPumpHasSourceFailure
from keba_keenergy_api.constants import HeatPumpHasSourcePressureFailure
from keba_keenergy_api.constants import HeatPumpHasThreePhaseFailure
from keba_keenergy_api.constants import HeatPumpHasVFDFailure
from keba_keenergy_api.constants import HeatPumpHeatRequest
from keba_keenergy_api.constants import HeatPumpOperatingMode
from keba_keenergy_api.error import APIError


@pytest.mark.happy
class TestHappyPathHeatPumpSection:
    @pytest.mark.asyncio
    async def test_get_name(self) -> None:
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, 9, "flushing"),
            (True, 5, "pressure_equalization"),
            (True, 21, "pressure_equalization"),
        ],
    )
    async def test_get_substate(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: int | str,
    ) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState",
                        "attributes": {
                            "formatId": "fmtHPSubState",
                            "longText": "Substate",
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
            data: int | str = await client.heat_pump.get_substate(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState", "attr": "1"}]',
                method="POST",
                auth=None,
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
                auth=None,
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
    async def test_get_compressor_use_night_speed(
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_night_speed(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_set_compressor_night_speed(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_min_compressor_night_speed(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_max_compressor_night_speed(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_circulation_pump_speed(self) -> None:
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
            data: float = await client.heat_pump.get_circulation_pump_speed()

            assert isinstance(data, float)
            assert data == 0.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_source_pump_speed(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].Source.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Source",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.0",
                        },
                        "value": "0.44875106",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_pump_speed()

            assert isinstance(data, float)
            assert data == 0.45  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Source.values.setValueScaled", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_flow_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_source_input_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_source_output_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_input_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_output_temperature(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_speed(self) -> None:
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
            data: float = await client.heat_pump.get_compressor_speed()

            assert isinstance(data, float)
            assert data == 0.3  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_condenser_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.tempCond",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Cond. temp.",
                            "unitId": "Temp",
                            "upperLimit": "200",
                            "lowerLimit": "0",
                        },
                        "value": "31.514103",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_condenser_temperature()

            assert isinstance(data, float)
            assert data == 31.51  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.tempCond", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_vaporizer_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.tempVap",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Evap. temp.",
                            "unitId": "Temp",
                        },
                        "value": "-4.5617409",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_vaporizer_temperature()

            assert isinstance(data, float)
            assert data == -4.56  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.tempVap", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_target_overheating(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.setOH",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Set suction SH",
                            "unitId": "TempRel",
                        },
                        "value": "5.4999752",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_target_overheating()

            assert isinstance(data, float)
            assert data == 5.50  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.setOH", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_current_overheating(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.actOH",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Act. suction SH",
                            "unitId": "TempRel",
                        },
                        "value": "18.676249",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_current_overheating()

            assert isinstance(data, float)
            assert data == 18.68  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.actOH", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_expansion_valve_position(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.stepperPos",
                        "attributes": {
                            "formatId": "fmt4p0",
                            "longText": "Stepper position",
                        },
                        "value": "20",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_pump.get_expansion_valve_position()

            assert isinstance(data, int)
            assert data == 20  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].OverHeatCtrl.values.stepperPos", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_high_pressure(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_low_pressure(self) -> None:
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_compressor_power(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_power(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_power(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cop(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_energy_consumption(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_heating_spf(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_energy(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_energy_consumption(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_cooling_spf(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_energy(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_energy_consumption(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_hot_water_spf(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_thermal_energy(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_energy_consumption(self) -> None:
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_total_spf(self) -> None:
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
                auth=None,
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
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_operating_time(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.operationalTimeS",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Operational hrs.",
                            "unitId": "TimeHour",
                        },
                        "value": "65037217",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_pump.get_operating_time()

            assert isinstance(data, int)
            assert data == 65037217  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.operationalTimeS", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_max_runtime(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.maxRunTimeS",
                        "attributes": {
                            "formatId": "fmt6p1",
                            "longText": "Max run-time",
                            "unitId": "TimeHour",
                        },
                        "value": "8836597",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_pump.get_max_runtime()

            assert isinstance(data, int)
            assert data == 8836597  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.maxRunTimeS", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_activation_counter(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.activationCounter",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Turn-on cycles",
                        },
                        "value": "1197",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_pump.get_activation_counter()

            assert isinstance(data, int)
            assert data == 1197  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.activationCounter", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHasCompressorFailure.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasCompressorFailure.OFF.value, 0),
        ],
    )
    async def test_has_compressor_failure(
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
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].FailureCompressor.values.actValue",
                        "attributes": {
                            "longText": "Failure compressor",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_compressor_failure(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureCompressor.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHasSourceFailure.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasSourceFailure.OFF.value, 0),
        ],
    )
    async def test_has_source_failure(
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
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].FailureSource.values.actValue",
                        "attributes": {
                            "longText": "Failure Source",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_source_failure(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureSource.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHasSourceActuatorFailure.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasSourceActuatorFailure.OFF.value, 0),
        ],
    )
    async def test_has_source_actuator_failure(
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
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].FailureActuatorSource.values.actValue",
                        "attributes": {
                            "longText": "Failure actuator src",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_source_actuator_failure(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureActuatorSource.values.actValue", "attr": "1"}]'
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
            (False, HeatPumpHasThreePhaseFailure.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasThreePhaseFailure.OFF.value, 0),
        ],
    )
    async def test_has_three_phase_failure(
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
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].FailureThreePhase.values.actValue",
                        "attributes": {
                            "longText": "Failure 3-Phase",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_three_phase_failure(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureThreePhase.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHasSourcePressureFailure.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasSourcePressureFailure.OFF.value, 0),
        ],
    )
    async def test_has_source_pressure_failure(
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
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].FailureSrcPressure.values.actValue",
                        "attributes": {
                            "longText": "Failure src pressure",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_source_pressure_failure(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureSrcPressure.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, HeatPumpHasVFDFailure.ON.value, 1),
            (True, "false", "off"),
            (False, HeatPumpHasVFDFailure.OFF.value, 0),
        ],
    )
    async def test_has_vfd_failure(
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
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].FailureVFD.values.actValue",
                        "attributes": {
                            "longText": "Failure VFD",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.has_vfd_failure(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureVFD.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )


@pytest.mark.unhappy
class TestUnhappyPathHeatPumpSection:

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
                await client.heat_pump.set_operating_mode(operating_mode)

            assert str(error.value) == "Invalid value! Allowed values are ['OFF', '0', 'ON', '1', 'BACKUP', '2']"

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_compressor_use_night_speed(
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

            with pytest.raises(APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1']"):
                await client.heat_pump.set_compressor_use_night_speed(operating_mode)

            mock_keenergy_api.assert_not_called()
