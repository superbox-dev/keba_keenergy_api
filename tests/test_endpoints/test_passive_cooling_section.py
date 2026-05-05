import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI


@pytest.mark.happy
class TestHappyPathPassiveCoolingSection:

    @pytest.mark.asyncio
    async def test_get_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.passivecooling[0].TempCoolPassive.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. passive cool",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "-100",
                        },
                        "value": "20.6",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.passive_cooling.get_temperature()

            assert isinstance(data, float)
            assert data == 20.60  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.passivecooling[0].TempCoolPassive.values.actValue", "attr": "1"}]',  # noqa: E501
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 1, "open"), (False, 0, 0), (True, 2, "closed")],
    )
    async def test_get_switch_valve_position(
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
                        "name": "APPL.CtrlAppl.sParam.passivecooling[0].SwitchValvePassiveCool.values.actPosition",
                        "attributes": {
                            "formatId": "fmtSwitchValveState",
                            "longText": "Act. Pos.",
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
            data: int | str = await client.passive_cooling.get_switch_valve_position(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.passivecooling[0].SwitchValvePassiveCool.values.actPosition", "attr": "1"}]',  # noqa: E501
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
                        "name": "APPL.CtrlAppl.sParam.passivecooling[0].Pump.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "CP speed",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "0.0",
                        },
                        "value": "0.2",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.passive_cooling.get_circulation_pump_speed()

            assert isinstance(data, float)
            assert data == 0.2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.passivecooling[0].Pump.values.setValueScaled", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_mixer_target_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.passivecooling[0].Mixer.values.setValue",
                        "attributes": {
                            "longText": "Set temp",
                        },
                        "value": "22",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.passive_cooling.get_mixer_target_temperature()

            assert isinstance(data, float)
            assert data == 22.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.passivecooling[0].Mixer.values.setValue", "attr": "1"}]',
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
                        "name": "APPL.CtrlAppl.sParam.passivecooling[0].Mixer.flowTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp. act.",
                            "unitId": "Temp",
                            "upperLimit": "100",
                            "lowerLimit": "0",
                        },
                        "value": "22.1",
                    }
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.passive_cooling.get_mixer_flow_temperature()

            assert isinstance(data, float)
            assert data == 22.10  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.passivecooling[0].Mixer.flowTemp.values.actValue", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    async def test_get_mixer_position(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.passivecooling[0].Mixer.mixer.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Mixer nom. value",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                            "lowerLimit": "-1",
                        },
                        "value": "1",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.passive_cooling.get_mixer_position()

            assert isinstance(data, float)
            assert data == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.passivecooling[0].Mixer.mixer.values.setValueScaled", '
                    '"attr": "1"}]'
                ),
                method="POST",
                auth=None,
                ssl=False,
            )
