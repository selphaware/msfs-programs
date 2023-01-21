from typing import Callable
from aircraft.aircraft_class import Aircraft
from fscentral.comcentral import ComCentral

CC: ComCentral = ComCentral()
AA: Aircraft = CC.aircraft
COM: Callable = AA.com_inter
TKOF: Callable = CC.procs["TAKEOFF"].exproc
APLA: Callable = CC.procs["APPROACH_LAND"].exproc
AUTO: Callable = CC.procs["FULL_AUTO"].exproc
