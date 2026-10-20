# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Payloads and expected results for the `read_data()` tests."""

from typing import Any
from typing import Final

from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_payload

read_data_payload_1: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty heat pumps",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. act.",
            "lowerLimit": "20",
            "unitId": "Temp",
            "upperLimit": "90",
        },
        "value": "40.808357",
    },
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
    {
        "name": "APPL.CtrlAppl.sParam.passivecooling[0].TempCoolPassive.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. passive cool",
            "unitId": "Temp",
            "upperLimit": "100",
            "lowerLimit": "-100",
        },
        "value": "21.16",
    },
    {
        "name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
        "attributes": {
            "formatId": "fmt6p0",
            "longText": "Acc. energy",
            "unitId": "kWh",
        },
        "value": "349442.23",
    },
]

read_data_payload_2: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Room temp. Nom.",
            "lowerLimit": "10",
            "unitId": "Temp",
            "upperLimit": "90",
        },
        "value": "10.808357",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Room temp. Nom.",
            "lowerLimit": "10",
            "unitId": "Temp",
            "upperLimit": "90",
        },
        "value": "11.808357",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Inflow temp.",
            "unitId": "Temp",
        },
        "value": "24.200001",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Inflow temp.",
            "unitId": "Temp",
        },
        "value": "23.200001",
    },
]

read_data_option_payload_3: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty heat pumps",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty HC",
            "lowerLimit": "0",
            "upperLimit": "8",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty solar",
            "upperLimit": "4",
            "lowerLimit": "0",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty buffers",
            "upperLimit": "0",
            "lowerLimit": "0",
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
        },
        "value": "0",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty HW tank",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty ext. heat sources",
            "upperLimit": "1",
            "lowerLimit": "0",
        },
        "value": "0",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty switch valves",
            "upperLimit": "0",
            "lowerLimit": "0",
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
        },
        "value": "1",
    },
]

read_data_payload_3: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Exterior temp.",
            "lowerLimit": "-100",
            "unitId": "Temp",
            "upperLimit": "100",
        },
        "value": "17.54",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Room temp. Nom.",
            "lowerLimit": "10",
            "unitId": "Temp",
            "upperLimit": "90",
        },
        "value": "10.808357",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName",
        "attributes": {
            "longText": "Heat curve",
        },
        "value": "HC1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Inflow temp.",
            "unitId": "Temp",
        },
        "value": "24.200001",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Inflow temp.",
            "unitId": "Temp",
        },
        "value": "23.2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.passivecooling[0].TempCoolPassive.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. passive cool",
            "unitId": "Temp",
            "upperLimit": "100",
            "lowerLimit": "-100",
        },
        "value": "21.21",
    },
    {
        "name": "APPL.CtrlAppl.sParam.passivecooling[1].TempCoolPassive.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. passive cool",
            "unitId": "Temp",
            "upperLimit": "100",
            "lowerLimit": "-100",
        },
        "value": "20.16",
    },
    {
        "name": "APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition",
        "attributes": {
            "formatId": "fmtSwitchValveStateV1",
            "longText": "Valve pos.",
            "unitId": "Enum",
            "upperLimit": "2",
            "lowerLimit": "0",
        },
        "value": "1",
    },
]

# Only HC1 (the first table of the line table pool) is in use, so only its name, number of points and 16 points
# are read.
read_data_extra_attributes_payload_3: list[dict[str, Any]] = heating_curve_points_payload[:34]

read_data_option_payload_4: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty heat pumps",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty HC",
            "lowerLimit": "0",
            "upperLimit": "8",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty solar",
            "upperLimit": "4",
            "lowerLimit": "0",
        },
        "value": "2",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty buffers",
            "upperLimit": "0",
            "lowerLimit": "0",
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty HW tank",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty ext. heat sources",
            "upperLimit": "1",
            "lowerLimit": "0",
        },
        "value": "0",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty switch valves",
            "upperLimit": "0",
            "lowerLimit": "0",
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
        },
        "value": "1",
    },
]

read_data_payload_4: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.bufferTank[0].topTemp.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. top act.",
            "unitId": "Temp",
            "upperLimit": "90",
            "lowerLimit": "5",
        },
        "value": "45.0273",
    },
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
    {
        "name": "APPL.CtrlAppl.sParam.solarCircuit[1].collectorTemp.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Source temp.",
            "unitId": "Temp",
            "upperLimit": "90",
            "lowerLimit": "20",
        },
        "value": "22.426912",
    },
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
            "longText": "Temp. act.2",
            "unitId": "Temp",
        },
        "value": "45.753",
    },
    {
        "name": "APPL.CtrlAppl.sParam.genericHeat[2].referenceTemp.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. act.1",
            "unitId": "Temp",
        },
        "value": "53.753",
    },
    {
        "name": "APPL.CtrlAppl.sParam.genericHeat[3].referenceTemp.values.actValue",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. act.2",
            "unitId": "Temp",
        },
        "value": "43.753",
    },
    {
        "name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. nom. 1",
            "unitId": "Temp",
            "upperLimit": "90",
            "lowerLimit": "0",
        },
        "value": "35",
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
    {
        "name": "APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. nom. 1",
            "unitId": "Temp",
            "upperLimit": "90",
            "lowerLimit": "0",
        },
        "value": "35",
    },
    {
        "name": "APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value",
        "attributes": {
            "formatId": "fmtTemp",
            "longText": "Temp. nom. 2",
            "unitId": "Temp",
            "upperLimit": "90",
            "lowerLimit": "0",
        },
        "value": "45",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.heatRequest",
        "attributes": {
            "unitId": "Enum",
            "upperLimit": "6",
            "lowerLimit": "0",
        },
        "value": "false",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[1].values.heatRequest",
        "attributes": {
            "unitId": "Enum",
            "upperLimit": "6",
            "lowerLimit": "0",
        },
        "value": "true",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.heatRequest",
        "attributes": {
            "unitId": "Enum",
            "upperLimit": "6",
            "lowerLimit": "0",
        },
        "value": "false",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatCircuit[3].values.heatRequest",
        "attributes": {
            "unitId": "Enum",
            "upperLimit": "6",
            "lowerLimit": "0",
        },
        "value": "true",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState",
        "attributes": {
            "formatId": "fmtHPSubState",
            "longText": "Substate",
            "unitId": "Enum",
            "upperLimit": "32767",
            "lowerLimit": "0",
        },
        "value": "21",
    },
    {
        "name": "APPL.CtrlAppl.sParam.heatpump[1].values.heatpumpSubState",
        "attributes": {
            "formatId": "fmtHPSubState",
            "longText": "Substate",
            "unitId": "Enum",
            "upperLimit": "32767",
            "lowerLimit": "0",
        },
        "value": "5",
    },
]

read_message_ids_payload: list[dict[str, Any]] = [
    {"name": "APPL.CtrlAppl.sParam.heatpump[0].FailureVFD.state.msgId", "value": "10"},
    {"name": "APPL.CtrlAppl.sParam.heatpump[1].FailureVFD.state.msgId", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].tempRoom.state.msgId", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.state.msgId", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.state.msgId", "value": "10"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[2].referenceTemp.state.msgId", "value": "10"},
    {"name": "APPL.CtrlAppl.sParam.genericHeat[3].referenceTemp.state.msgId", "value": "0"},
    {"name": "APPL.CtrlAppl.sParam.outdoorTemp.state.msgId", "value": "0"},
]

positions_payload: list[dict[str, Any]] = [
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty heat pumps",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty HC",
            "lowerLimit": "0",
            "upperLimit": "8",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSolarCircuits",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty solar",
            "upperLimit": "4",
            "lowerLimit": "0",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfBuffers",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty buffers",
            "upperLimit": "0",
            "lowerLimit": "0",
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
        "attributes": {
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
            "formatId": "fmt2p0",
            "longText": "Qty HW tank",
            "lowerLimit": "0",
            "upperLimit": "4",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfExtHeatSources",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty ext. heat sources",
            "upperLimit": "1",
            "lowerLimit": "0",
        },
        "value": "1",
    },
    {
        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfSwitchValves",
        "attributes": {
            "formatId": "fmt2p0",
            "longText": "Qty switch valves",
            "upperLimit": "0",
            "lowerLimit": "0",
            "dynLowerLimit": 1,
            "dynUpperLimit": 1,
        },
        "value": "1",
    },
]

LOGIN: Final[str] = "test"
INVALID_LOGIN: Final[str] = "invalid"
