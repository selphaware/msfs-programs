from SimConnect import SimConnect, AircraftRequests, AircraftEvents
import time
from typing import Tuple, List, Any, Dict, Union
from commands import EventCom, VarCom


class SimCentral(object):
    def __init__(self,
                 request_time: int = 2000,
                 sleep_ranges: Tuple[float] = (0.1, 2, 4)):
        self._request_time = request_time
        self.sim = None
        self.req = None
        self.eve = None
        self._sleep_ranges = {
            "LO": sleep_ranges[0],
            "MI": sleep_ranges[1],
            "HI": sleep_ranges[2]}
        self.start_sim()

    def start_sim(self):
        self.sim = SimConnect()
        self.req = AircraftRequests(self.sim, _time=self._request_time)
        self.eve = AircraftEvents(self.sim)
        print("Connected to Flight Simulator.")

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
            print(f"ERROR GET [ {req_id} ]: {err}")
            return None

    def get(self, req_id: VarCom, wait: bool = False) -> Any:
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

    def run(self, event_id: EventCom, sleep_range: str,
            *args: List[Any]) -> Dict[str, Union[bool, str]]:
        try:
            event_sim = self.eve.find(event_id)
            event_sim(*args)
            time.sleep(self.srange(sleep_range))
        except Exception as err:
            print(f"ERROR EVENT [ {event_id} ]: {err}")
            return {"success": False, "message": str(err)}
        return {"success": True, "message": ""}

    def pinfo(self) -> None:
        get_coms = [key for key in VarCom.__dict__.keys() if not ("_" == key[0])]
        for get_id in get_coms:
            g_id, lam, units = self.get(get_id)
            print(f"{get_id}: {lam(g_id)} {units}")
