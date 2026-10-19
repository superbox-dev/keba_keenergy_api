# Copyright 2023 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Tests for the heating circuit endpoints."""

import json
import re
from copy import deepcopy
from typing import Any

import pytest
from aioresponses import aioresponses
from syrupy.assertion import SnapshotAssertion

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.endpoints import HeatingCurvePoint
from keba_keenergy_api.endpoints import HeatingCurvePoints
from keba_keenergy_api.endpoints import HeatingCurves
from keba_keenergy_api.error import APIError
from tests.conftest import READ_URL
from tests.conftest import WRITE_URL
from tests.conftest import SentRequests
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_names_payload
from tests.test_endpoints.test_heat_circuit_section_data import heating_curve_points_payload

GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], float | int | str]] = [
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

INVALID_GETTERS: list[tuple[str, dict[str, Any], dict[str, Any], str]] = [
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

SETTERS: list[tuple[str, float | int | str, dict[str, Any], dict[str, str]]] = [
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

INVALID_SETTERS: list[tuple[str, int | str, dict[str, Any], str]] = [
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

HEATING_CURVE_POINTS: HeatingCurvePoints = (
    HeatingCurvePoint(outdoor=-20, flow=35),
    HeatingCurvePoint(outdoor=-10, flow=33),
    HeatingCurvePoint(outdoor=-5, flow=32),
    HeatingCurvePoint(outdoor=0, flow=30),
    HeatingCurvePoint(outdoor=5, flow=28),
    HeatingCurvePoint(outdoor=10, flow=27),
    HeatingCurvePoint(outdoor=20, flow=25),
)

INVALID_CURVE_MESSAGE: str = (
    "Invalid value! Allowed values are ['HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC FBH', 'HC HK']"
)


class TestHappyPathHeatCircuitSection:
    """Tests for the heating circuit endpoints with valid responses and input."""

    @pytest.mark.parametrize(("method", "kwargs", "response", "expected"), GETTERS)
    async def test_getter(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        method: str,
        kwargs: dict[str, Any],
        response: dict[str, Any],
        expected: float | str,
    ) -> None:
        """Test that a getter reads its variables and returns the converted value."""
        mock_api.post(READ_URL, payload=[{"name": name, "value": value} for name, value in response.items()])

        data: float | str = await getattr(client.heat_circuit, method)(**kwargs)

        assert data == expected
        assert type(data) is type(expected)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize(("method", "value", "kwargs", "expected"), SETTERS)
    async def test_setter(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        method: str,
        value: float | str,
        kwargs: dict[str, Any],
        expected: dict[str, str],
    ) -> None:
        """Test that a setter writes the expected variables."""
        mock_api.post(WRITE_URL, payload={})

        await getattr(client.heat_circuit, method)(value, **kwargs)

        mock_api.assert_called_once_with(
            url=WRITE_URL,
            data=json.dumps([{"name": name, "value": value} for name, value in expected.items()]),
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize("name", ["HC1", "HC FBH"])
    async def test_set_heating_curve(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        name: str,
    ) -> None:
        """Test that `set_heating_curve()` checks the curve name and writes it."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(WRITE_URL, payload={})

        await client.heat_circuit.set_heating_curve(name)

        assert sent_requests(mock_api) == snapshot

    @pytest.mark.parametrize("name", ["HC1", "HC FBH"])
    async def test_set_cooling_curve(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        name: str,
    ) -> None:
        """Test that `set_cooling_curve()` checks the curve name and writes it."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(WRITE_URL, payload={})

        await client.heat_circuit.set_cooling_curve(name)

        assert sent_requests(mock_api) == snapshot

    @pytest.mark.parametrize(
        ("heating_curve", "points_payload"),
        [
            (None, heating_curve_points_payload),
            # Only the requested heating curve is read (name, number of points and 16 points)
            ("HC1", heating_curve_points_payload[:34]),
        ],
        ids=["all", "HC1"],
    )
    async def test_get_heating_curve_points(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        heating_curve: str | None,
        points_payload: list[dict[str, Any]],
    ) -> None:
        """Test that `get_heating_curve_points()` returns the value from the response."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(READ_URL, payload=points_payload)

        response: HeatingCurves = await client.heat_circuit.get_heating_curve_points(heating_curve)

        assert response == snapshot(name="response")
        assert sent_requests(mock_api) == snapshot(name="requests")

    async def test_set_heating_curve_points(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `set_heating_curve_points()` reads the curve names and writes the points."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(READ_URL, payload=[{"name": "APPL.CtrlAppl.sParam.linTabPool[0].name", "value": "HC1"}])
        mock_api.post(WRITE_URL, payload={})

        await client.heat_circuit.set_heating_curve_points("HC1", points=HEATING_CURVE_POINTS)

        assert sent_requests(mock_api) == snapshot

    async def test_get_available_heating_curves(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `get_available_heating_curves()` returns the value from the response."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)

        data: tuple[tuple[int, str], ...] = await client.heat_circuit.get_available_heating_curves()

        assert data == (
            (0, "HC1"),
            (1, "HC2"),
            (2, "HC3"),
            (3, "HC4"),
            (4, "HC5"),
            (5, "HC6"),
            (6, "HC7"),
            (7, "HC8"),
            (12, "HC FBH"),
            (13, "HC HK"),
        )
        assert sent_requests(mock_api) == snapshot


class TestUnhappyPathHeatCircuitSection:
    """Tests for the heating circuit endpoints with invalid responses and input."""

    @pytest.mark.parametrize(("method", "kwargs", "response", "message"), INVALID_GETTERS)
    async def test_invalid_getter(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        method: str,
        kwargs: dict[str, Any],
        response: dict[str, Any],
        message: str,
    ) -> None:
        """Test that a getter raises `APIError` for a value that can't be converted."""
        mock_api.post(READ_URL, payload=[{"name": name, "value": value} for name, value in response.items()])

        with pytest.raises(APIError, match=re.escape(message)):
            await getattr(client.heat_circuit, method)(**kwargs)

        mock_api.assert_called_once_with(
            url=READ_URL,
            data=json.dumps([{"name": name, "attr": "1"} for name in response]),
            method="POST",
            headers={},
            ssl=False,
        )

    @pytest.mark.parametrize(("method", "value", "kwargs", "message"), INVALID_SETTERS)
    async def test_invalid_setter(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        method: str,
        value: str,
        kwargs: dict[str, Any],
        message: str,
    ) -> None:
        """Test that a setter raises `APIError` for an invalid value and sends no request."""
        with pytest.raises(APIError, match=re.escape(message)):
            await getattr(client.heat_circuit, method)(value, **kwargs)

        mock_api.assert_not_called()

    @pytest.mark.parametrize("name", ["INVALID"])
    async def test_set_invalid_heating_curve(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        name: str,
    ) -> None:
        """Test that `set_heating_curve()` raises `APIError` for an unknown heating curve."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)

        with pytest.raises(APIError, match=re.escape(INVALID_CURVE_MESSAGE)):
            await client.heat_circuit.set_heating_curve(name)

        assert sent_requests(mock_api) == snapshot

    @pytest.mark.parametrize("name", ["INVALID"])
    async def test_set_invalid_cooling_curve(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        name: str,
    ) -> None:
        """Test that `set_cooling_curve()` raises `APIError` for an unknown cooling curve."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)

        with pytest.raises(APIError, match=re.escape(INVALID_CURVE_MESSAGE)):
            await client.heat_circuit.set_cooling_curve(name)

        assert sent_requests(mock_api) == snapshot

    @pytest.mark.parametrize("heating_curve", ["HC10"])
    async def test_get_invalid_heating_curve_points(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
        heating_curve: str,
    ) -> None:
        """Test that `get_heating_curve_points()` raises `APIError` for an unknown curve without reading points."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)

        with pytest.raises(APIError, match='Heating curve "HC10" not found'):
            await client.heat_circuit.get_heating_curve_points(heating_curve)

        assert sent_requests(mock_api) == snapshot

    async def test_heating_curve_name_is_invalid_in_set_heating_curve_points(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `set_heating_curve_points()` raises `APIError` for an unknown heating curve."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)

        with pytest.raises(APIError, match=re.escape(INVALID_CURVE_MESSAGE)):
            await client.heat_circuit.set_heating_curve_points("HC_HK", points=HEATING_CURVE_POINTS)

        assert sent_requests(mock_api) == snapshot

    async def test_heating_curve_name_not_match_in_set_heating_curve_points(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
        snapshot: SnapshotAssertion,
        sent_requests: SentRequests,
    ) -> None:
        """Test that `set_heating_curve_points()` raises `APIError` if the curve name does not match its index."""
        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(READ_URL, payload=[{"name": "APPL.CtrlAppl.sParam.linTabPool[0].name", "value": "INVALID"}])

        with pytest.raises(APIError, match='Name of heating curve "HC1" does not match entry with index 0'):
            await client.heat_circuit.set_heating_curve_points("HC1", points=HEATING_CURVE_POINTS)

        assert sent_requests(mock_api) == snapshot

    async def test_too_many_points_in_get_heating_curve_points(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
    ) -> None:
        """Test that `get_heating_curve_points()` returns at most 16 points."""
        payload: list[dict[str, Any]] = deepcopy(heating_curve_points_payload[:34])
        payload[1]["value"] = "99"

        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(READ_URL, payload=payload)

        response: HeatingCurves = await client.heat_circuit.get_heating_curve_points("HC1")

        expected: int = 16
        assert len(response["HC1"]) == expected

    async def test_get_heating_curve_points_skips_unknown_curve_name(
        self,
        client: KebaKeEnergyAPI,
        mock_api: aioresponses,
    ) -> None:
        """Test that `get_heating_curve_points()` skips the points of unknown heating curves."""
        payload: list[dict[str, Any]] = deepcopy(heating_curve_points_payload)
        payload[0]["value"] = "UNKNOWN"

        mock_api.post(READ_URL, payload=heating_curve_names_payload)
        mock_api.post(READ_URL, payload=payload)

        response: HeatingCurves = await client.heat_circuit.get_heating_curve_points()

        assert "UNKNOWN" not in response
        assert "HC1" not in response
        assert "HC2" in response
