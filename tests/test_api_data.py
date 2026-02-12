from typing import Any

from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_expected_data
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
        "name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat",
        "attributes": {
            "formatId": "fmt6p0",
            "longText": "Acc. energy",
            "unitId": "kWh",
        },
        "value": "349442.23",
    },
]

read_data_expected_data_1: str = (
    '[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.extHeatSource[0].values.setTemp", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.photovoltaics.ElectricEnergyMeter.values.accumulatedHeat", "attr": "1"}]'
)

read_data_expected_response_1: dict[str, Any] = {
    "system": {
        "hot_water_tank_numbers": {"value": 2, "attributes": {"lower_limit": "0", "upper_limit": "4"}},
    },
    "buffer_tank": {},
    "hot_water_tank": {
        "current_temperature": [
            {
                "attributes": {"lower_limit": "20", "upper_limit": "90"},
                "value": 40.81,
            },
        ],
    },
    "heat_pump": {},
    "heat_circuit": {},
    "solar_circuit": {},
    "switch_valve": {},
    "external_heat_source": {
        "target_temperature": [
            {
                "attributes": {"lower_limit": "20", "upper_limit": "90"},
                "value": 22.56,
            },
        ],
    },
    "photovoltaic": {
        "total_energy": {
            "attributes": {},
            "value": 349442.23,
        },
    },
}

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

read_data_expected_data_2: str = (
    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue", "attr": "1"}]'
)

read_data_expected_response_2: dict[str, Any] = {
    "system": {},
    "buffer_tank": {},
    "hot_water_tank": {},
    "heat_pump": {
        "flow_temperature": [{"value": 24.2, "attributes": {}}, {"value": 23.2, "attributes": {}}],
    },
    "heat_circuit": {
        "target_temperature": [
            {"value": 10.81, "attributes": {"lower_limit": "10", "upper_limit": "90"}},
            {"value": 11.81, "attributes": {"lower_limit": "10", "upper_limit": "90"}},
        ],
    },
    "solar_circuit": {},
    "switch_valve": {},
    "external_heat_source": {},
    "photovoltaic": {},
}

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

read_data_extra_attributes_payload_3: list[dict[str, Any]] = heating_curve_points_payload

read_data_expected_data_3: str = (
    '[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.linTab.fileName", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.switchvalve[0].values.actPosition", "attr": "1"}]'
)

read_data_expected_response_3: dict[str, Any] = {
    "system": {
        "outdoor_temperature": {
            "value": 17.54,
            "attributes": {"lower_limit": "-100", "upper_limit": "100"},
        },
    },
    "buffer_tank": {},
    "hot_water_tank": {},
    "heat_pump": {
        "flow_temperature": [
            {
                "value": 24.2,
                "attributes": {},
            },
            {
                "value": 23.2,
                "attributes": {},
            },
        ],
    },
    "heat_circuit": {
        "heating_curve": [
            {
                "attributes": {
                    "points": [
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                        {
                            "flow": 20.0,
                            "outdoor": -15.0,
                        },
                    ],
                },
                "value": "hc1",
            },
        ],
        "target_temperature": [
            {
                "value": 10.81,
                "attributes": {
                    "lower_limit": "10",
                    "upper_limit": "90",
                },
            },
        ],
    },
    "solar_circuit": {},
    "switch_valve": {
        "position": [
            {
                "attributes": {
                    "lower_limit": "0",
                    "upper_limit": "2",
                },
                "value": "open",
            },
        ],
    },
    "external_heat_source": {},
    "photovoltaic": {},
}

read_data_expected_extra_attributes_3: str = heating_curve_points_expected_data

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

read_data_expected_data_4: str = (
    '[{"name": "APPL.CtrlAppl.sParam.bufferTank[0].topTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.solarCircuit[0].collectorTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.solarCircuit[1].collectorTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].referenceTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].referenceTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].referenceTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].referenceTemp.values.actValue", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].param.setTempMax.value", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].param.setTempMax.value", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].param.setTempMax.value", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].param.setTempMax.value", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[0].values.heatRequest", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[1].values.heatRequest", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[2].values.heatRequest", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.genericHeat[3].values.heatRequest", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpSubState", "attr": "1"}, '
    '{"name": "APPL.CtrlAppl.sParam.heatpump[1].values.heatpumpSubState", "attr": "1"}]'
)

read_data_expected_response_4: dict[str, Any] = {
    "system": {},
    "buffer_tank": {
        "current_top_temperature": [
            {
                "attributes": {
                    "lower_limit": "5",
                    "upper_limit": "90",
                },
                "value": 45.03,
            },
        ],
    },
    "hot_water_tank": {},
    "heat_pump": {
        "substate": [
            {
                "attributes": {
                    "lower_limit": "0",
                    "upper_limit": "32767",
                },
                "value": "pressure_equalization",
            },
            {
                "attributes": {
                    "lower_limit": "0",
                    "upper_limit": "32767",
                },
                "value": "pressure_equalization",
            },
        ],
    },
    "heat_circuit": {},
    "solar_circuit": {
        "current_temperature": [
            [
                {
                    "attributes": {},
                    "value": 55.75,
                },
                {
                    "attributes": {},
                    "value": 45.75,
                },
            ],
            [
                {
                    "attributes": {},
                    "value": 53.75,
                },
                {
                    "attributes": {},
                    "value": 43.75,
                },
            ],
        ],
        "heat_request": [
            [
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "6",
                    },
                    "value": "off",
                },
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "6",
                    },
                    "value": "on",
                },
            ],
            [
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "6",
                    },
                    "value": "off",
                },
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "6",
                    },
                    "value": "on",
                },
            ],
        ],
        "target_temperature": [
            [
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "90",
                    },
                    "value": 35.0,
                },
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "90",
                    },
                    "value": 45.0,
                },
            ],
            [
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "90",
                    },
                    "value": 35.0,
                },
                {
                    "attributes": {
                        "lower_limit": "0",
                        "upper_limit": "90",
                    },
                    "value": 45.0,
                },
            ],
        ],
        "source_temperature": [
            {
                "attributes": {
                    "lower_limit": "20",
                    "upper_limit": "90",
                },
                "value": 22.43,
            },
            {
                "attributes": {
                    "lower_limit": "20",
                    "upper_limit": "90",
                },
                "value": 22.43,
            },
        ],
    },
    "switch_valve": {},
    "external_heat_source": {},
    "photovoltaic": {},
}
