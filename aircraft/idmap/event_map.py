from typing import Dict, Union, Callable
from auxiliary.conversions import IDENTITY, PCT_REVR, INT_CONV, FLAP_CNV

EVE_IDS_MAP: Dict[str, Dict[str, Union[str, Callable]]] = {

    "AP_SPD_VAR_SET": {
        "COMMAND": "S SPD K",
        "CAST_LOGIC": INT_CONV,
        "UNIT": "KTS"
    },

    "AP_MACH_VAR_SET": {
        "COMMAND": "S SPD M",
        "CAST_LOGIC": lambda x: int(10 * float(x)),
        "UNIT": "MACH"
    },

    "AP_ALT_VAR_SET_ENGLISH": {
        "COMMAND": "S ALT",
        "CAST_LOGIC": INT_CONV,
        "UNIT": "FT"
    },

    "AP_PANEL_ALTITUDE_ON": {
        "COMMAND": "S ALT PUSH",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_ALT_HOLD_ON": {
        "COMMAND": "S ALT HOLD ON",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_ALT_HOLD_OFF": {
        "COMMAND": "S ALT HOLD OFF",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "FLAPS_INCR": {
        "COMMAND": "S FLAP I",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "FLAPS_DECR": {
        "COMMAND": "S FLAP D",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "FLAPS_SET": {
        "COMMAND": "S FLAP",
        "CAST_LOGIC": FLAP_CNV,
        "UNIT": "%"
    },

    "AXIS_ELEV_TRIM_SET": {
        "COMMAND": "S E T",
        "CAST_LOGIC": PCT_REVR,
        "UNIT": "%"
    },

    "AP_MASTER": {
        "COMMAND": "AP",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AUTOPILOT_OFF": {
        "COMMAND": "AP OFF",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AUTOPILOT_ON": {
        "COMMAND": "AP ON",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "INCREASE_AUTOBRAKE_CONTROL": {
        "COMMAND": "ABR I",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "DECREASE_AUTOBRAKE_CONTROL": {
        "COMMAND": "ABR D",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "MAX_AUTOBRAKE_CONTROL": {
        "COMMAND": "ABR M",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "FLIGHT_LEVEL_CHANGE": {
        "COMMAND": "FLC",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "FLIGHT_LEVEL_CHANGE_ON": {
        "COMMAND": "FLC ON",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "FLIGHT_LEVEL_CHANGE_OFF": {
        "COMMAND": "FLC OFF",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AUTO_THROTTLE_ARM": {
        "COMMAND": "AT",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AUTO_THROTTLE_TO_GA": {
        "COMMAND": "TOGA",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "THROTTLE_SET": {
        "COMMAND": "S T",
        "CAST_LOGIC": PCT_REVR,
        "UNIT": ""
    },

    "THROTTLE_CUT": {
        "COMMAND": "T C",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "THROTTLE_FULL": {
        "COMMAND": "T F",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "GEAR_UP": {
        "COMMAND": "GR UP",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "GEAR_DOWN": {
        "COMMAND": "GR DO",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "PARKING_BRAKES": {
        "COMMAND": "PB",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_LOC_HOLD_ON": {
        "COMMAND": "LOC ON",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_APR_HOLD_ON": {
        "COMMAND": "APR ON",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_LOC_HOLD_OFF": {
        "COMMAND": "LOC OFF",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_APR_HOLD_OFF": {
        "COMMAND": "APR OFF",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_NAV1_HOLD_ON": {
        "COMMAND": "LNAV ON",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

    "AP_NAV1_HOLD_OFF": {
        "COMMAND": "LNAV OFF",
        "CAST_LOGIC": IDENTITY,
        "UNIT": ""
    },

}
