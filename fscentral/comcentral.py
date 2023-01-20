from colorama import just_fix_windows_console
from colorama import Fore, Back, Style
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from typing import Tuple, Dict, Type

from aircraft.aircraft_class import Aircraft
from fscentral.procs.airproc import AirProc
from auxiliary.structs import PROC_INPUT_STRUCT
from fscentral.procs.procs import PROCS

just_fix_windows_console()

PROC_STRUCT = Tuple[AirProc, PROC_INPUT_STRUCT]

MPROC_STRUCT = Dict[str, PROC_STRUCT]


class ComCentral(object):
    def __init__(self, request_time: int = 2000, test: bool = False):
        self._request_time = request_time
        self.sim = None
        self.req = None
        self.eve = None
        self.procs = None
        self.aircraft = None
        self.test = test
        self.start_sim()

    def start_sim(self):
        if not self.test:
            # initialise Simulator connection, requests and events
            self.sim: SimConnect = SimConnect()
            self.req: AircraftRequests = AircraftRequests(self.sim,
                                                          _time=self._request_time)
            self.eve: AircraftEvents = AircraftEvents(self.sim)

            print(Back.GREEN + Fore.WHITE +
                  " Connected to LIVE Flight Simulator. " + Style.RESET_ALL)

        else:
            print(Back.BLUE + Fore.WHITE +
                  " Running in TEST MODE. NOT Connected to Flight Simulator."
                  + Style.RESET_ALL)

        # initialise aircraft
        self.aircraft = Aircraft(self.req, self.eve, test=self.test)
        print(Back.YELLOW + Fore.WHITE +
              " Aircraft initialised. " + Style.RESET_ALL)

        # initialise flight procedures
        self.procs: Dict[str, AirProc] = dict()
        for proc, pdat in PROCS.items():
            pclass: Type[AirProc] = pdat[0]
            pinputs: PROC_INPUT_STRUCT = pdat[1]
            self.procs[proc] = pclass(self.aircraft, pinputs)

        print(Back.MAGENTA + Fore.WHITE +
              " Flight Procedures initialised. " + Style.RESET_ALL)

    def stop_sim(self):
        if not self.test:
            self.sim.exit()
        print("Disconnected from Flight Simulator.")
