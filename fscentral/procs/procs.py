from fscentral.procs.full_auto import FullAutoProc
from fscentral.procs.takeoff import TakeOffProc
from fscentral.procs.approach_land import ApproachLandProc

PROCS = {
    "TAKEOFF": (
        TakeOffProc,
        [
            ("POWER", -1),
            ("RISE_ALT", 2000),
            ("CRUISE_ALT", 33000),
            ("CRUISE_KSPD", 420),
            ("STEADY_THROTTLE", 1),
            ("ELEVATOR_TRIM", -20),
            ("LIFTOFF_KSPD", 165)
        ]
    ),

    "APPROACH_LAND": (
        ApproachLandProc,
        [
            ("RUNWAY", None),
            ("LAND_ALT", None),
            ("FLOATING_ALT", 1500),
            ("CUT_OFF", 5.5)
        ]
    ),

    "FULL_AUTO": (
        FullAutoProc,
        [
            ("RUNWAY", None),
            ("LAND_ALT", None),
            ("RENDE_WP_ID", None),
            ("POWER", -1),
            ("RISE_ALT", 2000),
            ("CRUISE_ALT", 33000),
            ("CRUISE_KSPD", 420),
            ("STEADY_THROTTLE", 1),
            ("ELEVATOR_TRIM", -20),
            ("LIFTOFF_KSPD", 165),
            ("FLOATING_ALT", 1500),
            ("CUT_OFF", 5.5)
        ]
    )
}
