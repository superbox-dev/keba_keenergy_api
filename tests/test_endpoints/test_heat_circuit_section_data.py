# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Heating curve payloads and expected results for the heating circuit tests."""

from typing import Any
from typing import Final

from keba_keenergy_api.endpoints import HeatingCurvePoint
from keba_keenergy_api.endpoints import HeatingCurvePoints
from keba_keenergy_api.endpoints import Response

heating_curve_names_payload: Response = [
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC3",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC4",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC5",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC6",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC8",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[8].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "ValveOffset",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[9].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "VFS5-100",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[10].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "Fan",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[11].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "PowerLimit",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC FBH",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "HC HK",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[14].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "ValveOffsetAT",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[15].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "Fan WPLK412",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[16].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[17].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[18].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[19].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[20].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[21].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[22].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[23].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[24].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[25].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[26].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[27].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[28].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[29].name",
        "attributes": {
            "longText": "Table name",
        },
        "value": "",
    },
]

heating_curve_points_payload: Response = [
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].name",
        "attributes": {"longText": "Table name"},
        "value": "HC1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[0].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].name",
        "attributes": {"longText": "Table name"},
        "value": "HC2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[1].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].name",
        "attributes": {"longText": "Table name"},
        "value": "HC3",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[2].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].name",
        "attributes": {"longText": "Table name"},
        "value": "HC4",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[3].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].name",
        "attributes": {"longText": "Table name"},
        "value": "HC5",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[4].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].name",
        "attributes": {"longText": "Table name"},
        "value": "HC6",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[5].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].name",
        "attributes": {"longText": "Table name"},
        "value": "HC7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[6].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].name",
        "attributes": {"longText": "Table name"},
        "value": "HC8",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[7].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].name",
        "attributes": {"longText": "Table name"},
        "value": "HC FBH",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[12].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].name",
        "attributes": {"longText": "Table name"},
        "value": "HC HK",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].noOfPoints",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "QTY points",
            "upperLimit": "16",
            "lowerLimit": "0",
        },
        "value": "7",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[0].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[0].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[1].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[1].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[2].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[2].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[3].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[3].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[4].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[4].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[5].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[5].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[6].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[6].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[7].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[7].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[8].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[8].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[9].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[9].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[10].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[10].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[11].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[11].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[12].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[12].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[13].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[13].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[14].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[14].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[15].x",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point X",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "-15",
    },
    {
        "name": "APPL.CtrlAppl.sParam.linTabPool[13].points[15].y",
        "attributes": {
            "formatId": "fmtCurrent",
            "longText": "Point Y",
            "upperLimit": "90000",
            "lowerLimit": "-90000",
        },
        "value": "20",
    },
]

GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]]] = [
    ("get_name", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.name": "FBH"}, "FBH"),
    ("get_mode", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": "0"}, "heating"),
    ("get_mode", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": 0}, 0),
    ("get_mode", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": "1"}, "cooling"),
    ("get_mode", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": 1}, 1),
    (
        "get_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": "2"},
        "heating_and_cooling",
    ),
    ("get_mode", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": 2}, 2),
    (
        "get_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": "3"},
        "heating_and_active_cooling",
    ),
    ("get_mode", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].type": 3}, 3),
    (
        "has_room_temperature",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomTemp": "true"},
        "on",
    ),
    (
        "has_room_temperature",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomTemp": 1},
        1,
    ),
    (
        "has_room_temperature",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomTemp": "false"},
        "off",
    ),
    (
        "has_room_temperature",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomTemp": 0},
        0,
    ),
    ("get_room_temperature", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue": "22.426912"}, 22.43),
    (
        "has_room_humidity",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomHumidity": "true"},
        "on",
    ),
    (
        "has_room_humidity",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomHumidity": 1},
        1,
    ),
    (
        "has_room_humidity",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomHumidity": "false"},
        "off",
    ),
    (
        "has_room_humidity",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRoomHumidity": 0},
        0,
    ),
    ("get_room_humidity", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].humidityRoom.values.actValue": "53"}, 53.0),
    ("get_dew_point", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].dewPoint.values.actValue": "13.100544"}, 13.1),
    (
        "get_flow_temperature_setpoint",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.flowSetTemp": "26.254391"},
        26.25,
    ),
    ("has_mixer", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasMixer": "true"}, "on"),
    ("has_mixer", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasMixer": 1}, 1),
    ("has_mixer", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasMixer": "false"}, "off"),
    ("has_mixer", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasMixer": 0}, 0),
    (
        "get_mixer_flow_temperature",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.flowTemp.values.actValue": "26.254391"},
        26.25,
    ),
    (
        "get_mixer_return_flow_temperature",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.refluxTemp.values.actValue": "31.254391"},
        31.25,
    ),
    (
        "get_mixer_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled": "-1"},
        "closed",
    ),
    (
        "get_mixer_position",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled": "0"},
        0,
    ),
    (
        "get_mixer_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled": "1"},
        "open",
    ),
    (
        "get_mixer_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled": "-0.045793723"},
        "off",
    ),
    (
        "get_mixer_position",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].heatCircuitMixer.mixer.values.setValueScaled": "0.045793723"},
        "off",
    ),
    (
        "get_pump_state",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB": "true"},
        "on",
    ),
    ("get_pump_state", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB": 1}, 1),
    (
        "get_pump_state",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB": "false"},
        "off",
    ),
    ("get_pump_state", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].pump.values.setValueB": 0}, 0),
    (
        "has_return_flow_temperature",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRefluxTemp": "true"},
        "on",
    ),
    (
        "has_return_flow_temperature",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRefluxTemp": 1},
        1,
    ),
    (
        "has_return_flow_temperature",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRefluxTemp": "false"},
        "off",
    ),
    (
        "has_return_flow_temperature",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasRefluxTemp": 0},
        0,
    ),
    ("get_return_flow_temperature", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].tempReflux.values.actValue": "19"}, 19.0),
    ("get_target_temperature", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue": "22"}, 22.0),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "true"},
        "on",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "false"},
        "off",
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "true"},
        1,
    ),
    (
        "get_use_excess_energy",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "false"},
        0,
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.useExcessEnergy": "2"},
        "cooling",
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.useExcessEnergy": "0"},
        0,
    ),
    (
        "get_excess_energy_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.useExcessEnergy": "1"},
        1,
    ),
    (
        "get_excess_energy_target_temperature",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.value": "23"},
        23.0,
    ),
    (
        "get_excess_energy_target_temperature_hysteresis",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.hyst": "0.2"},
        0.2,
    ),
    (
        "get_excess_energy_target_cooling_temperature",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.value": "23"},
        23.0,
    ),
    (
        "get_excess_energy_target_cooling_temperature_hysteresis",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.hyst": "0.2"},
        0.2,
    ),
    (
        "get_selected_target_temperature",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.selectedSetTemp": "21.5"},
        21.5,
    ),
    ("get_target_temperature_day", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp": "23"}, 23.0),
    (
        "get_target_cooling_temperature_day",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.normalCoolSetTemp": "22"},
        22.0,
    ),
    ("get_heating_limit_day", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value": "16"}, 16.0),
    ("get_cooling_limit_day", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayCoolTemp.value": "24"}, 24.0),
    (
        "get_excess_energy_heating_limit_day",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayTemp": "25"},
        25.0,
    ),
    (
        "get_excess_energy_cooling_limit_day",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayCoolTemp": "10"},
        10.0,
    ),
    ("get_target_temperature_night", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp": "23"}, 23.0),
    (
        "get_target_cooling_temperature_night",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedCoolSetTemp": "22"},
        22.0,
    ),
    ("get_heating_limit_night", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value": "16"}, 16.0),
    (
        "get_cooling_limit_night",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightCoolTemp.value": "24"},
        24.0,
    ),
    (
        "get_excess_energy_heating_limit_night",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightTemp": "25"},
        25.0,
    ),
    (
        "get_excess_energy_cooling_limit_night",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightCoolTemp": "25"},
        25.0,
    ),
    ("get_target_temperature_away", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp": "14"}, 14.0),
    ("get_target_temperature_offset", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp": "2"}, 2.0),
    (
        "get_operating_mode",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode": "3"},
        "night",
    ),
    (
        "get_operating_mode",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode": "3"},
        3,
    ),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "0"},
        "off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 0}, 0),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "1"},
        "on",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 1}, 1),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "2"},
        "flow_off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 2}, 2),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "3"},
        "temporary_off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 3}, 3),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "4"},
        "room_off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 4}, 4),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "5"},
        "outdoor_off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 5}, 5),
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "6"},
        "inflow_off",
    ),
    ("get_heat_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": 6}, 6),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "0"},
        "off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 0}, 0),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "1"},
        "on",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 1}, 1),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "2"},
        "flow_off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 2}, 2),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "3"},
        "temporary_off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 3}, 3),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "4"},
        "room_off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 4}, 4),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "5"},
        "outdoor_off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 5}, 5),
    (
        "get_cool_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": "6"},
        "inflow_off",
    ),
    ("get_cool_request", {"human_readable": False}, {"APPL.CtrlAppl.sParam.heatCircuit[0].values.coolRequest": 6}, 6),
    ("get_away_start_date", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.start": "1768690800"}, 1768690800),
    ("get_away_end_date", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.stop": "1769036400"}, 1769036400),
    ("get_heating_curve_offset", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveOffset": "3.5"}, 3.5),
    ("get_cooling_curve_offset", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveOffset": "3.5"}, 3.5),
    ("get_heating_curve_slope", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveGradient": "0.25"}, 0.25),
    ("get_cooling_curve_slope", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveGradient": "0.5"}, 0.5),
    (
        "get_use_heating_curve",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "true"},
        "on",
    ),
    (
        "get_use_heating_curve",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "false"},
        "off",
    ),
    (
        "get_use_heating_curve",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "true"},
        1,
    ),
    (
        "get_use_heating_curve",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "false"},
        0,
    ),
    ("get_heating_curve", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName": "HC4"}, "HC4"),
    ("get_cooling_curve", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.coollinTab.fileName": "HC1"}, "HC1"),
    ("has_pump", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasPump": "true"}, "on"),
    ("has_pump", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasPump": 1}, 1),
    ("has_pump", {"human_readable": True}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasPump": "false"}, "off"),
    ("has_pump", {"human_readable": False}, {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasPump": 0}, 0),
    (
        "has_var_speed_pump",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasVarSpeedPump": "true"},
        "on",
    ),
    (
        "has_var_speed_pump",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasVarSpeedPump": 1},
        1,
    ),
    (
        "has_var_speed_pump",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasVarSpeedPump": "false"},
        "off",
    ),
    (
        "has_var_speed_pump",
        {"human_readable": False},
        {"APPL.CtrlAppl.sParam.options.heatCircuit[0].hasVarSpeedPump": 0},
        0,
    ),
    ("get_pump_speed", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].pumpAO.values.setValueScaled": "0.4"}, 0.4),
    (
        "get_room_temperature",
        {"position": 1},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.values.actValue": "21.456"},
        21.46,
    ),
    (
        "get_room_temperature",
        {"position": 2},
        {"APPL.CtrlAppl.sParam.heatCircuit[1].tempRoom.values.actValue": "21.456"},
        21.46,
    ),
    (
        "get_room_temperature",
        {"position": 3},
        {"APPL.CtrlAppl.sParam.heatCircuit[2].tempRoom.values.actValue": "21.456"},
        21.46,
    ),
    ("has_mixer", {"position": 2}, {"APPL.CtrlAppl.sParam.options.heatCircuit[1].hasMixer": "true"}, "on"),
]

INVALID_GETTERS: Final[list[tuple[str, dict[str, Any], dict[str, Any], str]]] = [
    (
        "get_heat_request",
        {"human_readable": True},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest": "16"},
        (
            "Can't convert value to human readable value! {'name': "
            "'APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest', 'value': '16'}"
        ),
    ),
]

SETTERS: Final[list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]]] = [
    (
        "set_use_excess_energy",
        "off",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "0"},
    ),
    (
        "set_use_excess_energy",
        "ON",
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "1"},
    ),
    ("set_use_excess_energy", 1, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "1"}),
    ("set_use_excess_energy", 0, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.useExcessEnergy": "0"}),
    (
        "set_excess_energy_target_temperature",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.value": "23"},
    ),
    (
        "set_excess_energy_target_temperature_hysteresis",
        3,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTemp.hyst": "3"},
    ),
    (
        "set_excess_energy_target_cooling_temperature",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.value": "23"},
    ),
    (
        "set_excess_energy_target_cooling_temperature_hysteresis",
        3,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergyTempCool.hyst": "3"},
    ),
    ("set_target_temperature_day", 23, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp": "23"}),
    (
        "set_target_cooling_temperature_day",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.normalCoolSetTemp": "23"},
    ),
    ("set_heating_limit_day", 23, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value": "23"}),
    ("set_cooling_limit_day", 23, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayCoolTemp.value": "23"}),
    (
        "set_excess_energy_heating_limit_day",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayTemp": "23"},
    ),
    (
        "set_excess_energy_cooling_limit_day",
        11,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdDayCoolTemp": "11"},
    ),
    ("set_target_temperature_night", 23, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp": "23"}),
    (
        "set_target_cooling_temperature_night",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedCoolSetTemp": "23"},
    ),
    ("set_heating_limit_night", 23, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value": "23"}),
    (
        "set_cooling_limit_night",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightCoolTemp.value": "23"},
    ),
    (
        "set_excess_energy_heating_limit_night",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightTemp": "23"},
    ),
    (
        "set_excess_energy_cooling_limit_night",
        23,
        {},
        {"APPL.CtrlAppl.sParam.heatCircuit[0].param.excessEnergy.thresholdNightCoolTemp": "23"},
    ),
    ("set_target_temperature_away", 14, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp": "14"}),
    ("set_target_temperature_offset", 2, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp": "2"}),
    ("set_operating_mode", "OFF", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode": "0"}),
    ("set_operating_mode", "AUTO", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode": "1"}),
    ("set_operating_mode", 2, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode": "2"}),
    ("set_operating_mode", 3, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode": "3"}),
    ("set_away_start_date", 1768690800, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.start": "1768690800"}),
    ("set_away_end_date", 1768690800, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.holiday.stop": "1768690800"}),
    ("set_heating_curve_offset", 3.5, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveOffset": "3.5"}),
    ("set_cooling_curve_offset", 3.5, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveOffset": "3.5"}),
    ("set_heating_curve_slope", 0.5, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.heatCurveGradient": "0.5"}),
    ("set_cooling_curve_slope", 0.5, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.coolCurveGradient": "0.5"}),
    ("set_use_heating_curve", "off", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "0"}),
    ("set_use_heating_curve", "ON", {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "1"}),
    ("set_use_heating_curve", 1, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "1"}),
    ("set_use_heating_curve", 0, {}, {"APPL.CtrlAppl.sParam.heatCircuit[0].param.enableHeatCurveLinTab": "0"}),
]

INVALID_SETTERS: Final[list[tuple[str, int | str, dict[str, Any], str]]] = [
    ("set_use_excess_energy", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
    (
        "set_operating_mode",
        "INVALID",
        {},
        (
            "Invalid value! Allowed values are ['OFF', '0', 'AUTO', '1', 'DAY', '2', 'NIGHT', '3', "
            "'HOLIDAY', '4', 'PARTY', '5', 'EXTERNAL', '8', 'ROOM_CONTROL', '9']"
        ),
    ),
    ("set_use_heating_curve", "INVALID", {}, "Invalid value! Allowed values are ['OFF', '0', 'ON', '1']"),
]

HEATING_CURVE_POINTS: Final[HeatingCurvePoints] = (
    HeatingCurvePoint(outdoor=-20, flow=35),
    HeatingCurvePoint(outdoor=-10, flow=33),
    HeatingCurvePoint(outdoor=-5, flow=32),
    HeatingCurvePoint(outdoor=0, flow=30),
    HeatingCurvePoint(outdoor=5, flow=28),
    HeatingCurvePoint(outdoor=10, flow=27),
    HeatingCurvePoint(outdoor=20, flow=25),
)

INVALID_CURVE_MESSAGE: Final[str] = (
    "Invalid value! Allowed values are ['HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC FBH', 'HC HK']"
)
