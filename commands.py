from enum import Enum
from typing import Tuple, Any
from math import pi


class VarCom(Tuple[str, Any, str], Enum):
    PLANE_ALTITUDE = ("PLANE_ALTITUDE", lambda x: x, "FT")

    AIRSPEED_TRUE = ("AIRSPEED_TRUE", lambda x: x, "KTS")

    AIRSPEED_INDICATED = ("AIRSPEED_INDICATED", lambda x: x, "KTS")

    AIRSPEED_MACH = ("AIRSPEED_MACH", lambda x: x, "MACH")

    VERTICAL_SPEED = ("VERTICAL_SPEED", lambda x: x, "M/S")

    AILERON_POSITION = ("AILERON_POSITION", lambda x: x, "DEGREES")

    ANGLE_OF_ATTACK_INDICATOR = ("ANGLE_OF_ATTACK_INDICATOR",
                                 lambda x: (1 - (x / pi)) * (180 / pi),
                                 "DEGREES")

    PLANE_PITCH_DEGREES = ("PLANE_PITCH_DEGREES", lambda x: x * (180 / pi),
                           "DEGREES")

    TRAILING_EDGE_FLAPS_LEFT_ANGLE = ("TRAILING_EDGE_FLAPS_LEFT_ANGLE",
                                      lambda x: x * (180 / pi), "DEGREES")

    TRAILING_EDGE_FLAPS_RIGHT_ANGLE = ("TRAILING_EDGE_FLAPS_RIGHT_ANGLE",
                                       lambda x: x * (180 / pi), "DEGREES")

    GPS_WP_DISTANCE = ("GPS_WP_DISTANCE", lambda x: x / 1000 / 1.852, "MILES")

    GPS_TARGET_DISTANCE = ("GPS_TARGET_DISTANCE", lambda x: x / 1000 / 1.852,
                           "MILES")

    GPS_WP_NEXT_ALT = ("GPS_WP_NEXT_ALT", lambda x: round(x * 3.28084), "FT")

    GPS_WP_NEXT_ID = ("GPS_WP_NEXT_ID", lambda x: x, _)

    AUTOPILOT_FLIGHT_LEVEL_CHANGE = ("AUTOPILOT_FLIGHT_LEVEL_CHANGE",
                                     lambda x: (x - 1) == 0, _)

    GPS_WP_PREV_ID = ("GPS_WP_PREV_ID", lambda x: x, _)

    GROUND_ALTITUDE = ("GROUND_ALTITUDE", lambda x: round(x * 3.28084), "FT")

    GEAR_ON_GROUND = ("GEAR_ON_GROUND", lambda x: x, _)


class EventCom(str, Enum):
    AP_SPD_VAR_SET = "AP_SPD_VAR_SET"
    AP_MACH_VAR_SET = "AP_MACH_VAR_SET"
    AP_ALT_VAR_SET_ENGLISH = "AP_ALT_VAR_SET_ENGLISH"
    AP_PANEL_ALTITUDE_ON = "AP_PANEL_ALTITUDE_ON"
    AP_ALT_HOLD_ON = "AP_ALT_HOLD_ON"
    AP_ALT_HOLD_OFF = "AP_ALT_HOLD_OFF"
    FLAPS_INCR = "FLAPS_INCR"
    FLAPS_DECR = "FLAPS_DECR"
    FLAPS_SET = "FLAPS_SET"
    AP_MASTER = "AP_MASTER"
    AUTOPILOT_OFF = "AUTOPILOT_OFF"
    AUTOPILOT_ON = "AUTOPILOT_ON"
    INCREASE_AUTOBRAKE_CONTROL = "INCREASE_AUTOBRAKE_CONTROL"
    DECREASE_AUTOBRAKE_CONTROL = "DECREASE_AUTOBRAKE_CONTROL"
    FLIGHT_LEVEL_CHANGE = "FLIGHT_LEVEL_CHANGE"
    FLIGHT_LEVEL_CHANGE_ON = "FLIGHT_LEVEL_CHANGE_ON"
    FLIGHT_LEVEL_CHANGE_OFF = "FLIGHT_LEVEL_CHANGE_OFF"
    AUTO_THROTTLE_ARM = "AUTO_THROTTLE_ARM"
    AUTO_THROTTLE_TO_GA = "AUTO_THROTTLE_TO_GA"
    THROTTLE_SET = "THROTTLE_SET"
    THROTTLE_CUT = "THROTTLE_CUT"
    THROTTLE_FULL = "THROTTLE_FULL"
    GEAR_UP = "GEAR_UP"
    GEAR_DOWN = "GEAR_DOWN"
    PARKING_BRAKES = "PARKING_BRAKES"
    AP_LOC_HOLD_ON = "AP_LOC_HOLD_ON"
    AP_APR_HOLD_ON = "AP_LOC_HOLD_ON"
    AP_LOC_HOLD_OFF = "AP_LOC_HOLD_OFF"
    AP_APR_HOLD_OFF = "AP_APR_HOLD_OFF"
    AP_NAV1_HOLD_ON = "AP_NAV1_HOLD_ON"
    AP_NAV1_HOLD_OFF = "AP_NAV1_HOLD_OFF"
