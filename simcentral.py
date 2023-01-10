from colorama import just_fix_windows_console
from colorama import Fore, Back, Style
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
import time
from typing import Tuple, Any, Dict, Union, Optional
from simcoms import EventCom, VarCom
from simcoms import M_TO_FT


just_fix_windows_console()


class SimCentral(object):
    def __init__(self,
                 request_time: int = 2000,
                 sleep_ranges: Tuple[float] = (0.01, 0.1, 2, 4),
                 test: bool = False):
        self._request_time = request_time
        self.sim = None
        self.req = None
        self.eve = None
        self._sleep_ranges = {
            "XO": sleep_ranges[0],
            "LO": sleep_ranges[1],
            "MI": sleep_ranges[2],
            "HI": sleep_ranges[3]}
        self.test = test
        self.start_sim()
        if not self.test:
            self.pinfo(refresh=True)

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

    def get(self, req_id: str, wait: bool = False,
            xo: bool = True, refresh: bool = False) -> Any:
        if self.test:
            return -4321

        else:
            try:
                val = self.req.get(req_id)

                while val is None:

                    if refresh:
                        self.req.find(req_id).time = 200

                    val = self.req.get(req_id)
                    time.sleep(self.srange("XO" if xo else "LO"))
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
                if (args is not None) and len(args) and (args[0] is not None):
                    event_sim(*args)
                else:
                    event_sim()
            else:
                print(Fore.GREEN + f"TEST: Running Command {event_id}, sleeping "
                                   f"for "
                      f"{self.srange(sleep_range)}s, VALUE ARGS = {args}"
                      + Style.RESET_ALL)
            time.sleep(self.srange(sleep_range))

        except Exception as err:

            print(Fore.RED + f"ERROR EVENT [ {event_id} ]: {err}" + Style.RESET_ALL)
            return {"success": False, "message": str(err)}

        return {"success": True, "message": f"Command Success: [ {event_id} ] with "
                                            f"Args = [ {args} ]"}

    def execute(self, comm: str, sleep_range: str) -> Optional[Dict[str,
                                                                    Union[bool, str]]]:
        try:
            vc_map = EventCom.__dict__
            comm = comm.upper()
            get_coms = [(key, val)
                        for key, val in vc_map.items() if not ("_" == key[0])]
            com_list = [x_com for key, (key2, x_com, _, _) in get_coms]

            for key, (i_event, i_com, units, i_lam) in get_coms:
                i_com = i_com.upper()

                if i_com == comm:

                    # special case for max auto brakes
                    # TODO: move to procs to clean this up
                    if (i_event is None) and (i_com == "ABR M"):  # max auto brakes
                        for _ in range(5):
                            self.run("INCREASE_AUTOBRAKE_CONTROL", "LO")
                        return self.run("INCREASE_AUTOBRAKE_CONTROL", "LO")
                    else:
                        return self.run(i_event, sleep_range, None)

                elif (i_com == comm[:len(i_com)]) and (comm not in com_list):
                    return self.run(i_event, sleep_range,
                                    i_lam(comm.split(i_com)[1].strip()))
                else:
                    pass

        except Exception as err:
            print(Fore.RED + f"ERROR, recheck your command: {err}" + Style.RESET_ALL)
            return None

        print(Fore.RED + f"ERROR: Invalid Command -> {comm}" + Style.RESET_ALL)

    def pinfo(self, refresh: bool = False) -> None:
        vc_map = VarCom.__dict__
        get_coms = [key for key in vc_map.keys() if not ("_" == key[0])]

        for get_id in get_coms:

            val = self.get(get_id, refresh=refresh, wait=True)
            _, _, lam, units = vc_map[get_id]
            units = "" if units is None else units
            print(Fore.YELLOW + f"{get_id}:" + Fore.CYAN +
                  f" {lam(val)} {units}" + Style.RESET_ALL)

    def get_next_alt(self) -> Tuple[int, int]:
        val = None
        count = 0
        zval = False
        while (val is None) or (val == 0):
            val = self.get("GPS_WP_NEXT_ALT", xo=True, wait=True)
            count += 1
            if count > 100:
                zval = True
                break

        g_alt = self.get("GROUND_ALTITUDE")
        if zval:
            red_alt = round((self.get("PLANE_ALTITUDE",
                                          xo=True,
                                          wait=True) - g_alt) * .75)
            return red_alt, red_alt

        else:
            return round(val * M_TO_FT), round(6000 + g_alt)
