# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Test data for the `KebaKeEnergyAPI` client."""

from typing import Any
from typing import Final

from keba_keenergy_api.models import DeviceCounts
from keba_keenergy_api.models import HeatingCurvePoint
from keba_keenergy_api.sections import BufferTank
from keba_keenergy_api.sections import HeatingCircuit
from keba_keenergy_api.sections import HeatPump
from keba_keenergy_api.sections import Section
from keba_keenergy_api.sections import SolarCircuit
from keba_keenergy_api.sections import System

LOGIN: Final = "mocked-login"
TIMEZONE_RESPONSE: Final = {"timezone": "Europe/Vienna"}

DEVICE_COUNTS_RESPONSE: Final = [
    {"name": f"APPL.CtrlAppl.sParam.options.systemNumberOf{name}", "value": value}
    for name, value in (
        ("Buffers", "0"),
        ("HotWaterTanks", "1"),
        ("ExtHeatSources", "1"),
        ("HeatPumps", "1"),
        ("HeatingCircuits", "2"),
        ("SolarCircuits", "1"),
        ("SwitchValves", "0"),
    )
]

# One heat pump and two heating circuits.
FILTER_COUNTS: Final = DeviceCounts(
    buffer_tank=0,
    dhw_tank=0,
    external_heat_source=0,
    heat_pump=1,
    heating_circuit=2,
    solar_circuit=0,
    switch_valve=0,
)

READ_SECTIONS: Final[list[Section]] = [
    System.OUTDOOR_TEMPERATURE,
    System.OPERATING_MODE,
    HeatPump.SUB_STATE,
    HeatPump.OPERATING_TIME,
    HeatingCircuit.NAME,
    HeatingCircuit.PUMP_ACTIVE,
    SolarCircuit.CONSUMER_TEMPERATURE,
    BufferTank.TOP_TEMPERATURE,
    # A section that is requested twice is read once.
    System.OUTDOOR_TEMPERATURE,
]

READ_RESPONSE: Final[list[dict[str, Any]]] = [
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
    {"name": "APPL.CtrlAppl.sParam.param.operatingMode", "attributes": {"unitId": "Enum"}, "value": "4"},
    {"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState", "value": "25"},
    {"name": "APPL.CtrlAppl.sParam.heatpump[0].operationalData.operationalTimeS", "value": "3600"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.name", "value": "FBH1"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[1].param.name", "value": "FBH2"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB", "value": "true"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[1].pump.values.setValueB", "value": "false"},
    {
        "name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue",
        "attributes": {"lowerLimit": "-", "upperLimit": "150"},
        "value": "45.5",
    },
    {"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue", "value": "38"},
]

# The message id follows the value of each section that has one.
READ_WITH_MESSAGE_IDS_RESPONSE: Final = [
    {"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.5"},
    {"name": "APPL.CtrlAppl.sParam.outdoorTemp.state.msgId", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState", "value": "2"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.state.msgId", "value": "10"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[1].tempRoom.values.actValue", "value": "21.5"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[1].tempRoom.state.msgId", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue", "value": "-50"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.state.msgId", "value": "53"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue", "value": "38"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.state.msgId", "value": "0"},
]

UNKNOWN_MESSAGE_ID: Final = "APPL.CtrlAppl.sParam.outdoorTemp.state.msgId"

# The response without the unknown message id of the outdoor temperature.
READ_WITHOUT_UNKNOWN_MESSAGE_ID_RESPONSE: Final = [
    {"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.5"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.state.msgId", "value": "10"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[1].tempRoom.values.actValue", "value": "21.5"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[1].tempRoom.state.msgId", "value": "0"},
]

HEATING_CURVE_NAMES_RESPONSE: Final = [
    {"name": f"APPL.CtrlAppl.sParam.linTabPool[{index}].name", "value": name}
    for index, name in enumerate(["HC1", "", "", "HC2", "LT5", *[""] * 25])
]

HEATING_CURVE_POINTS: Final = [
    HeatingCurvePoint(outdoor=-20.0, flow=50.0),
    HeatingCurvePoint(outdoor=-10.0, flow=45.0),
    HeatingCurvePoint(outdoor=-5.0, flow=40.5),
    HeatingCurvePoint(outdoor=0.0, flow=38.0),
    HeatingCurvePoint(outdoor=5.0, flow=33.25),
    HeatingCurvePoint(outdoor=10.0, flow=30.0),
    HeatingCurvePoint(outdoor=20.0, flow=25.0),
]

# More than the maximum number of points.
HEATING_CURVE_MAX_POINTS: Final = [HeatingCurvePoint(outdoor=float(index), flow=30.0) for index in range(16)]


def heating_curve_response(number_of_points: str, points: list[HeatingCurvePoint], /) -> list[dict[str, Any]]:
    """Return the response for the number of points and the points of one line table.

    Parameters
    ----------
    number_of_points
        Raw number of points of the line table.
    points
        The points, the rest of the 16 points is 0.

    Returns
    -------
    list[dict[str, Any]]
        The response items in the order of the read payload.

    """
    values: list[float] = [value for point in points for value in point]
    values += [0.0] * (32 - len(values))

    return [{"value": number_of_points}, *({"value": str(value)} for value in values)]
