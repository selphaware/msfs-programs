from fscentral.procs.full_auto import FullAutoProc
from fscentral.procs.procs_inputs import (
    TAKEOFF_INPUTS, APPROACH_LAND_INPUTS,
    FULL_AUTO_INPUTS,
)
from fscentral.procs.takeoff import TakeOffProc
from fscentral.procs.approach_land import ApproachLandProc

PROCS = {
    "TAKEOFF": (
        TakeOffProc,
        TAKEOFF_INPUTS
    ),

    "APPROACH_LAND": (
        ApproachLandProc,
        APPROACH_LAND_INPUTS
    ),

    "FULL_AUTO": (
        FullAutoProc,
        FULL_AUTO_INPUTS
    )
}
