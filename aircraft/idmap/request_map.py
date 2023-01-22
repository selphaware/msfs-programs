from typing import Dict, Union, Callable
from auxiliary.conversions import (
    IDENTITY, RAD_TO_DEG_HALF, RAD_TO_DEG,
    PCT_CNVT, KM_TO_NM, M_TO_FT, BOOL_CHK
)

REQ_IDS_MAP: Dict[str, Dict[str, Union[str, Callable]]] = {

    "PLANE_ALTITUDE": {
        "COMMAND": "G ALT",
        "CAST_LOGIC": IDENTITY,
        "UNITS": "FT"
    },

    "AIRSPEED_TRUE": {
        "COMMAND": "G SPD T",
        "CAST_LOGIC": IDENTITY,
        "UNITS": "KTS"
    },

    "AIRSPEED_INDICATED": {
        "COMMAND": "G SPD I",
        "CAST_LOGIC": IDENTITY,
        "UNITS": "KTS"
    },

    "AIRSPEED_MACH": {
        "COMMAND": "G SPD M",
        "CAST_LOGIC": IDENTITY,
        "UNITS": "MACH"
    },

    "VERTICAL_SPEED": {
        "COMMAND": "G VS",
        "CAST_LOGIC": IDENTITY,
        "UNITS": "M/S"
    },

    "AILERON_POSITION": {
        "COMMAND": "G ALERPOS",
        "CAST_LOGIC": IDENTITY,
        "UNITS": "DEGREES"
    },

    "ANGLE_OF_ATTACK_INDICATOR": {
        "COMMAND": "G AOA",
        "CAST_LOGIC": RAD_TO_DEG_HALF,
        "UNITS": "DEGREES"
    },

    "PLANE_PITCH_DEGREES": {
        "COMMAND": "G PPD",
        "CAST_LOGIC": RAD_TO_DEG,
        "UNITS": "DEGREES"
    },

    "ELEVATOR_TRIM_PCT": {
        "COMMAND": "G E T",
        "CAST_LOGIC": PCT_CNVT,
        "UNITS": "%"
    },

    "TRAILING_EDGE_FLAPS_LEFT_ANGLE": {
        "COMMAND": "G FLAP L",
        "CAST_LOGIC": RAD_TO_DEG,
        "UNITS": "DEGREES"
    },

    "TRAILING_EDGE_FLAPS_RIGHT_ANGLE": {
        "COMMAND": "G FLAP R",
        "CAST_LOGIC": RAD_TO_DEG,
        "UNITS": "DEGREES"
    },

    "GPS_WP_DISTANCE": {
        "COMMAND": "G WP DIS",
        "CAST_LOGIC": KM_TO_NM,
        "UNITS": "N.MILES"
    },

    "GPS_TARGET_DISTANCE": {
        "COMMAND": "G TGT DIS",
        "CAST_LOGIC": KM_TO_NM,
        "UNITS": "N.MILES"
    },

    "GPS_WP_NEXT_ALT": {
        "COMMAND": "G WP NX ALT",
        "CAST_LOGIC": M_TO_FT,
        "UNITS": "FT"
    },

    "GPS_WP_NEXT_ID": {
        "COMMAND": "G WP NX ID",
        "CAST_LOGIC": IDENTITY,
        "UNITS": ""
    },

    "AUTOPILOT_FLIGHT_LEVEL_CHANGE": {
        "COMMAND": "G FLC",
        "CAST_LOGIC": BOOL_CHK,
        "UNITS": ""
    },

    "AUTOPILOT_APPROACH_HOLD": {
        "COMMAND": "G APR H",
        "CAST_LOGIC": BOOL_CHK,
        "UNITS": ""
    },

    "GPS_WP_PREV_ID": {
        "COMMAND": "G WP PRE ID",
        "CAST_LOGIC": IDENTITY,
        "UNITS": ""
    },

    "GROUND_ALTITUDE": {
        "COMMAND": "G GD ALT",
        "CAST_LOGIC": M_TO_FT,
        "UNITS": "FT"
    },

    "GEAR_HANDLE_POSITION": {
        "COMMAND": "G GR POS",
        "CAST_LOGIC": BOOL_CHK,
        "UNITS": ""
    }
}
