from typing import Callable
from aircraft.aircraft_class import Aircraft
from fscentral.comcentral import ComCentral
import sys
from colorama import Fore, Style

sys.ps1 = Fore.YELLOW + "<" + Fore.LIGHTCYAN_EX + " FS " + Fore.YELLOW + \
          "+ " + Fore.LIGHTMAGENTA_EX + "Py " + Fore.YELLOW + "> " + \
          Fore.LIGHTGREEN_EX + ">> " + Style.RESET_ALL

CC: ComCentral = ComCentral()
AA: Aircraft = CC.aircraft
COM: Callable = AA.com_inter
TKOF: Callable = CC.procs["TAKEOFF"].exproc
APLA: Callable = CC.procs["APPROACH_LAND"].exproc
AUTO: Callable = CC.procs["FULL_AUTO"].exproc
P: Callable = AA.pinfo
