from typing import Callable
from aircraft.aircraft_class import Aircraft
from fscentral.comcentral import ComCentral
import sys
from colorama import Fore, Style, Back

sys.ps1 = Fore.LIGHTBLUE_EX + "[" + Fore.LIGHTCYAN_EX + \
          " FS " + Fore.LIGHTBLUE_EX + \
          "+ " + Fore.LIGHTMAGENTA_EX + "Py " + Fore.LIGHTBLUE_EX + "] " + \
          Fore.LIGHTGREEN_EX + ">> " + Style.RESET_ALL

if __name__ == "__main__":
    args = sys.argv[1:]
    test = False
    if len(args):
        test = args[0].upper() == "TEST"

    CC: ComCentral = ComCentral(test=test)
    AA: Aircraft = CC.aircraft
    COM: Callable = AA.com_inter
    TKOF: Callable = CC.procs["TAKEOFF"].exproc
    APLA: Callable = CC.procs["APPROACH_LAND"].exproc
    AUTO: Callable = CC.procs["FULL_AUTO"].exproc
    P: Callable = AA.pinfo
    Q: Callable = quit
    print(
        "\n" + Fore.BLACK + Back.LIGHTCYAN_EX +
        " ***** --- ** - Flight Simulator "
        "COMMAND CONSOLE v1.1 - ** --- ***** " +
        Fore.LIGHTRED_EX + Back.BLACK +
        " by Usman Ahmad @ selphaware @ polardesert\n" +
        Style.RESET_ALL
    )
