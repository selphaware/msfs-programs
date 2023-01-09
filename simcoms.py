from typing import Tuple, Any
from math import pi

MAX_VAL = 2 ** 14 - 1  # 16383


class VarCom(Tuple[str, str, Any, str]):
    PLANE_ALTITUDE = ("PLANE_ALTITUDE", "G ALT", lambda x: x, "FT")

    AIRSPEED_TRUE = ("AIRSPEED_TRUE", "G SPD T", lambda x: x, "KTS")

    AIRSPEED_INDICATED = ("AIRSPEED_INDICATED", "G SPD I", lambda x: x, "KTS")

    AIRSPEED_MACH = ("AIRSPEED_MACH", "G SPD M", lambda x: x, "MACH")

    VERTICAL_SPEED = ("VERTICAL_SPEED", "G VS", lambda x: x, "M/S")

    AILERON_POSITION = ("AILERON_POSITION", "G ALERPOS", lambda x: x, "DEGREES")

    ANGLE_OF_ATTACK_INDICATOR = ("ANGLE_OF_ATTACK_INDICATOR", "G AOA",
                                 lambda x: (1 - (x / pi)) * (180 / pi),
                                 "DEGREES")

    PLANE_PITCH_DEGREES = ("PLANE_PITCH_DEGREES", "G PPD",
                           lambda x: x * (180 / pi),
                           "DEGREES")

    TRAILING_EDGE_FLAPS_LEFT_ANGLE = ("TRAILING_EDGE_FLAPS_LEFT_ANGLE",
                                      "G FLAP L",
                                      lambda x: x * (180 / pi), "DEGREES")

    TRAILING_EDGE_FLAPS_RIGHT_ANGLE = ("TRAILING_EDGE_FLAPS_RIGHT_ANGLE",
                                       "G FLAP R",
                                       lambda x: x * (180 / pi), "DEGREES")

    GPS_WP_DISTANCE = ("GPS_WP_DISTANCE", "G WP DIS",
                       lambda x: x / 1000 / 1.852, "MILES")

    GPS_TARGET_DISTANCE = ("GPS_TARGET_DISTANCE", "G TGT DIS",
                           lambda x: x / 1000 / 1.852, "MILES")

    GPS_WP_NEXT_ALT = ("GPS_WP_NEXT_ALT", "G WP NX ALT",
                       lambda x: round(x * 3.28084), "FT")

    GPS_WP_NEXT_ID = ("GPS_WP_NEXT_ID", "G WP NX ID", lambda x: x, None)

    AUTOPILOT_FLIGHT_LEVEL_CHANGE = ("AUTOPILOT_FLIGHT_LEVEL_CHANGE",
                                     "G FLC",
                                     lambda x: (x - 1) == 0, None)

    GPS_WP_PREV_ID = ("GPS_WP_PREV_ID", "G WP PRE ID", lambda x: x, None)

    GROUND_ALTITUDE = ("GROUND_ALTITUDE", "G GD ALT",
                       lambda x: round(x * 3.28084), "FT")

    GEAR_ON_GROUND = ("GEAR_ON_GROUND", "G GD GR", lambda x: x, None)


class EventCom(Tuple[str, str, str, Any]):
    AP_SPD_VAR_SET = ("AP_SPD_VAR_SET", "S SPD K", "KTS", lambda x: int(x))

    AP_MACH_VAR_SET = ("AP_MACH_VAR_SET", "S SPD M", "MACH", lambda x: int(10 *
                                                                           float(x)))

    AP_ALT_VAR_SET_ENGLISH = ("AP_ALT_VAR_SET_ENGLISH", "S ALT", "FT",
                              lambda x: int(x))
    AP_PANEL_ALTITUDE_ON = ("AP_PANEL_ALTITUDE_ON", "S ALT PUSH", None, lambda x: x)
    AP_ALT_HOLD_ON = ("AP_ALT_HOLD_ON", "S ALT HOLD ON", None, lambda x: x)
    AP_ALT_HOLD_OFF = ("AP_ALT_HOLD_OFF", "S ALT HOLD OFF", None, lambda x: x)

    FLAPS_INCR = ("FLAPS_INCR", "S FLAP I", None, lambda x: x)
    FLAPS_DECR = ("FLAPS_DECR", "S FLAP D", None, lambda x: x)

    FLAPS_SET = ("FLAPS_SET", "S FLAP", "%", lambda x: round(float(x) * MAX_VAL /
                                                                   100))

    AP_MASTER = ("AP_MASTER", "AP", None, lambda x: x)
    AUTOPILOT_OFF = ("AUTOPILOT_OFF", "AP OFF", None, lambda x: x)
    AUTOPILOT_ON = ("AUTOPILOT_ON", "AP ON", None, lambda x: x)

    INCREASE_AUTOBRAKE_CONTROL = ("INCREASE_AUTOBRAKE_CONTROL", "ABR I", None,
                                  lambda x: x)

    DECREASE_AUTOBRAKE_CONTROL = ("DECREASE_AUTOBRAKE_CONTROL", "ABR D", None,
                                  lambda x: x)

    MAX_AUTOBRAKE_CONTROL = (None, "ABR M", None, lambda x: x)
    FLIGHT_LEVEL_CHANGE = ("FLIGHT_LEVEL_CHANGE", "FLC", None, lambda x: x)
    FLIGHT_LEVEL_CHANGE_ON = ("FLIGHT_LEVEL_CHANGE_ON", "FLC ON", None, lambda x: x)
    FLIGHT_LEVEL_CHANGE_OFF = ("FLIGHT_LEVEL_CHANGE_OFF", "FLC OFF", None, lambda x: x)
    AUTO_THROTTLE_ARM = ("AUTO_THROTTLE_ARM", "AT", None, lambda x: x)
    AUTO_THROTTLE_TO_GA = ("AUTO_THROTTLE_TO_GA", "TOGA", None, lambda x: x)

    THROTTLE_SET = ("THROTTLE_SET", "S T", "%", lambda x: round(float(x) * MAX_VAL /
                                                                100))

    THROTTLE_CUT = ("THROTTLE_CUT", "T C", None, lambda x: x)
    THROTTLE_FULL = ("THROTTLE_FULL", "T F", None, lambda x: x)
    GEAR_UP = ("GEAR_UP", "GR UP", None, lambda x: x)
    GEAR_DOWN = ("GEAR_DOWN", "GR DO", None, lambda x: x)
    PARKING_BRAKES = ("PARKING_BRAKES", "PB", None, lambda x: x)
    AP_LOC_HOLD_ON = ("AP_LOC_HOLD_ON", "LOC ON", None, lambda x: x)
    AP_APR_HOLD_ON = ("AP_LOC_HOLD_ON", "APR ON", None, lambda x: x)
    AP_LOC_HOLD_OFF = ("AP_LOC_HOLD_OFF", "LOC OFF", None, lambda x: x)
    AP_APR_HOLD_OFF = ("AP_APR_HOLD_OFF", "APR OFF", None, lambda x: x)
    AP_NAV1_HOLD_ON = ("AP_NAV1_HOLD_ON", "LNAV ON", None, lambda x: x)
    AP_NAV1_HOLD_OFF = ("AP_NAV1_HOLD_OFF", "LNAV OFF", None, lambda x: x)
