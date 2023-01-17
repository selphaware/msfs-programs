from colorama import just_fix_windows_console
from colorama import Fore, Back, Style
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from typing import Tuple, Any, Dict, Union, Optional

from aircraft.aircraft_class import Aircraft


just_fix_windows_console()


class ComCentral(object):
    def __init__(self, request_time: int = 2000, test: bool = False):
        self._request_time = request_time
        self.sim = None
        self.req = None
        self.eve = None
        self.aircraft = None
        self.test = test
        self.start_sim()

    def start_sim(self):
        if not self.test:
            self.sim = SimConnect()
            self.req = AircraftRequests(self.sim, _time=self._request_time)
            self.eve = AircraftEvents(self.sim)
            print(Back.GREEN + Fore.WHITE +
                  " Connected to LIVE Flight Simulator. " + Style.RESET_ALL)
        else:
            print(Back.BLUE + Fore.WHITE +
                  " Running in TEST MODE. NOT Connected to Flight Simulator."
                  + Style.RESET_ALL)

        self.aircraft = Aircraft(self.req, self.eve, test=self.test)

    def stop_sim(self):
        if not self.test:
            self.sim.exit()
        print("Disconnected from Flight Simulator.")
