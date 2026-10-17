# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Heating curve payloads and expected results for the heating circuit tests."""

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
