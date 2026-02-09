import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import ExternalHeatSourceHeatRequest
from keba_keenergy_api.constants import ExternalHeatSourceOperatingMode
from keba_keenergy_api.error import APIError


class TestExternalHeatSourceSection:
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
                        "name": "APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtExternalSourceType",
                            "longText": "Oper. mode",
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
            data: int | str = await client.external_heat_source.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("on", 1), ("OFF", 0), (ExternalHeatSourceOperatingMode.ON.value, 1)],
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
            await client.external_heat_source.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].param.operatingMode", "value": "%s"}]'  # noqa: UP031
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

            with pytest.raises(APIError, match=r"Invalid value! Allowed values are \['OFF', '0', 'ON', '1']"):
                await client.external_heat_source.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_target_temperature(self) -> None:

        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.external_heat_source.get_target_temperature()

            assert isinstance(data, float)
            assert data == 22.56  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].values.setTemp", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [
            (True, "true", "on"),
            (False, ExternalHeatSourceHeatRequest.ON.value, 1),
            (True, "false", "off"),
            (False, ExternalHeatSourceHeatRequest.OFF.value, 0),
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
                        "name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.values.setValueB",
                        "attributes": {
                            "longText": "Dig. request",
                        },
                        "value": payload_value,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.external_heat_source.get_heat_request(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.values.setValueB", "attr": "1"}]',
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
                        "name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.operationalTimeS",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Operational hrs.",
                            "unitId": "TimeHour",
                        },
                        "value": "3809028",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.external_heat_source.get_operating_time()

            assert isinstance(data, int)
            assert data == 3809028  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.operationalTimeS", "attr": "1"}]',  # noqa: E501
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
                        "name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.maxRunTimeS",
                        "attributes": {
                            "formatId": "fmt6p1",
                            "longText": "Max run-time",
                            "unitId": "TimeHour",
                        },
                        "value": "602403",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.external_heat_source.get_max_runtime()

            assert isinstance(data, int)
            assert data == 602403  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.maxRunTimeS", "attr": "1"}]',
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
                        "name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.activationCounter",
                        "attributes": {
                            "formatId": "fmt6p0",
                            "longText": "Turn-on cycles",
                        },
                        "value": "477",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.external_heat_source.get_activation_counter()

            assert isinstance(data, int)
            assert data == 477  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].DO.operationalData.activationCounter", "attr": "1"}]',  # noqa: E501
                method="POST",
                auth=None,
                ssl=False,
            )
