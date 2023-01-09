from typing import Dict
from simcoms import VarCom, EventCom, MAX_VAL
from simcentral import SimCentral


class SimProcs(object):
    def __init__(self, sc: SimCentral):
        self.sc = sc


    def takeoff(self,
                power: int = -1,
                rise_alt: int = 2000,
                cruise_alt: int = 33000,
                cruise_kspd: int = 420,
                steady_throttle: bool = True
                ) -> Dict[str, str]:

        print("Setting initial altitude")
        self.sc
