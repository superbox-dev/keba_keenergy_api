import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI


class TestSwitchValveSection:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 1, "open"), (False, 0, 0), (True, 2, "closed")],
    )
    async def test_get_position(
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
                        "name": "APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition",
                        "attributes": {
                            "formatId": "fmtSwitchValveStateV1",
                            "longText": "Valve pos.",
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
            data: int | str = await client.switch_valve.get_position(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition", "attr": "1"}]',
                method="POST",
                auth=None,
                ssl=False,
            )
