from colorama import just_fix_windows_console
from colorama import Fore, Back, Style
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
import time
from typing import Tuple, List, Any, Dict, Union, Optional
from simcoms import EventCom, VarCom

just_fix_windows_console()


class SimCentral(object):
    def __init__(self,
                 request_time: int = 2000,
                 sleep_ranges: Tuple[float] = (0.1, 2, 4),
                 test: bool = False):
        self._request_time = request_time
        self.sim = None
        self.req = None
        self.eve = None
        self._sleep_ranges = {
            "LO": sleep_ranges[0],
            "MI": sleep_ranges[1],
            "HI": sleep_ranges[2]}
        self.test = test
        self.start_sim()

    def start_sim(self):
        if not self.test:
            self.sim = SimConnect()
            self.req = AircraftRequests(self.sim, _time=self._request_time)
            self.eve = AircraftEvents(self.sim)
            print(Back.GREEN + Fore.WHITE +
                  "Connected to LIVE Flight Simulator." + Style.RESET_ALL)
        else:
            print(Back.BLUE + Fore.WHITE +
                  "NOT Connected to Flight Simulator. Running in TEST MODE"
                  + Style.RESET_ALL)

    def stop_sim(self):
        self.sim.exit()
        print("Disconnected from Flight Simulator.")

    def srange(self, rng: str) -> float:
        return self._sleep_ranges[rng]

    def find(self, req_id: str) -> Any:
        try:
            val = self.req.find(req_id)
            return val

        except Exception as err:
            print(Fore.RED + f"ERROR GET [ {req_id} ]: {err}" + Style.RESET_ALL)
            return None

    def get(self, req_id: VarCom, wait: bool = False) -> Any:
        if self.test:
            return -4321

        else:
            try:
                val = self.req.get(req_id)

                while val is None:
                    val = self.req.get(req_id)
                    time.sleep(self.srange("LO"))
                    if not wait:
                        break

                return val

            except Exception as err:
                print(f"ERROR GET [ {req_id} ]: {err}")
                return None

    def run(self, event_id: Optional[str], sleep_range: str,
            *args) -> Dict[str, Union[bool, str]]:

        try:
            if not self.test:
                event_sim = self.eve.find(event_id)
                event_sim(*args)
            else:
                print(Fore.GREEN + f"TEST: Running Command {event_id}, sleeping "
                                   f"for "
                      f"{self.srange(sleep_range)}s, VALUE ARGS = {args}"
                      + Style.RESET_ALL)
            time.sleep(self.srange(sleep_range))

        except Exception as err:

            print(Fore.RED + f"ERROR EVENT [ {event_id} ]: {err}" + Style.RESET_ALL)
            return {"success": False, "message": str(err)}

        return {"success": True, "message": ""}

    def execute(self, comm: str, sleep_range: str) -> Dict[str, Union[bool, str]]:
        vc_map = EventCom.__dict__
        comm = comm.upper()
        get_coms = [(key, val)
                    for key, val in vc_map.items() if not ("_" == key[0])]
        com_list = [x_com for key, (key2, x_com, _, _) in get_coms]

        for key, (i_event, i_com, units, i_lam) in get_coms:
            i_com = i_com.upper()

            if i_com == comm:

                # special case for max auto brakes
                if (i_event is None) and (i_com == "ABR M"):  # max auto brakes
                    for _ in range(5):
                        self.run("INCREASE_AUTOBRAKE", "LO")
                    return self.run("INCREASE_AUTOBRAKE", "LO")
                else:
                    return self.run(i_event, sleep_range, None)

            elif (i_com == comm[:len(i_com)]) and (comm not in com_list):
                return self.run(i_event, sleep_range,
                                i_lam(comm.split(i_com)[1].strip()))
            else:
                pass

    def pinfo(self) -> None:
        vc_map = VarCom.__dict__
        get_coms = [key for key in vc_map.keys() if not ("_" == key[0])]

        for get_id in get_coms:

            val = self.get(get_id)
            _, _, lam, units = vc_map[get_id]
            units = "" if units is None else units
            print(Fore.YELLOW + f"{get_id}:" + Fore.CYAN +
                  f" {lam(val)} {units}" + Style.RESET_ALL)
