from typing import Optional, Tuple, List
from SimConnect import AircraftRequests, AircraftEvents
from time import sleep
from colorama import Fore, Style, Back

from auxiliary.conversions import INIT_VAL
from aircraft.find_funcs import test_find_func, wrap_efunc
from aircraft.idmap.event_map import EVE_IDS_MAP
from aircraft.idmap.request_map import REQ_IDS_MAP
from auxiliary.structs import IN_STRUCT, OUT_STRUCT


class Aircraft(object):
    def __init__(self,
                 req: Optional[AircraftRequests] = None,
                 eve: Optional[AircraftEvents] = None,
                 test: bool = False):
        """

        :param req:
        :param eve:
        """
        self.__req = req
        self.__eve = eve
        self.__test = test

        # -- REQUESTS --
        # GET Simulation Variables
        get_vars = {x: y["CAST_LOGIC"](INIT_VAL)
                    for x, y in REQ_IDS_MAP.items()}

        self.__dict__.update(get_vars)

        # -- EVENTS --
        # SET Simulation Variables
        if eve is None:
            find_func = test_find_func

        else:
            find_func = eve.find

        set_vars = {f"_{x_main}": wrap_efunc(find_func)(x_main,
                                                        y_main["CAST_LOGIC"])
                    for x_main, y_main in EVE_IDS_MAP.items()}

        self.__dict__.update(set_vars)

        # Initialise GET attributes
        if not test:
            self.refresh(initialise=True)

        # -- COMMANDS --
        # Initialise Command variables
        get_coms = {y["COMMAND"]: x for x, y in REQ_IDS_MAP.items()}
        self.__req_coms = get_coms

        set_coms = {y_main["COMMAND"]: x_main
                    for x_main, y_main in EVE_IDS_MAP.items()}
        self.__eve_coms = set_coms

        # TODO: Add bespoke COMmand variables

    def get_req_ids(self):
        return [x_id.upper()
                for x_id in self.__dict__.keys() if not ("_" == x_id[0])]

    def get_eve_ids(self):
        return [x_id.upper()
                for x_id in self.__dict__.keys()
                if ("_Aircraft__" not in x_id) and ("_" == x_id[0])]

    def req_id_valid(self, var_id: str) -> bool:
        return var_id.upper() in self.get_req_ids()

    def eve_id_valid(self, var_id: str) -> bool:
        return var_id.upper() in self.get_eve_ids()

    def refresh(self, req_id: Optional[str] = None,
                initialise: bool = False,
                wait: bool = False) -> None:
        """

        :param wait:
        :param initialise:
        :param req_id:
        :return:
        """
        if self.__req is None:
            raise Exception("Requests variable req cannot be None.")

        if req_id is not None:
            if not self.req_id_valid(req_id):
                raise Exception(f"Request id {req_id} not found.")

            var_ids = [req_id]

        else:
            var_ids = self.get_req_ids()

        for var_id in var_ids:
            if initialise:
                self.__req.find(var_id).time = 200

            val = self.__req.get(var_id)

            while val is None:

                val = self.__req.get(var_id)
                sleep(0.01)

                if not wait:
                    break

            setattr(self, var_id, val)

    def get(self, req_id: Optional[str] = None,
            refresh_vals: bool = True, time_sleep: float = 0.0,
            request_refresh: bool = False,
            wait: bool = False) -> OUT_STRUCT:
        """

        :param wait:
        :param request_refresh:
        :param time_sleep:
        :param req_id:
        :param refresh_vals:
        :return:
        """
        if refresh_vals and not self.__test:
            self.refresh(req_id, initialise=request_refresh, wait=wait)

        if time_sleep > 0:
            sleep(time_sleep)

        if req_id is not None:
            return REQ_IDS_MAP[req_id]["CAST_LOGIC"](getattr(self, req_id))

        else:
            return {var_id: REQ_IDS_MAP[var_id]["CAST_LOGIC"](getattr(self, var_id))
                    for var_id in self.get_req_ids()}

    def run(self, eve_id: str,
            args: Optional[List[IN_STRUCT]] = None,
            time_sleep: float = 0.1) -> None:
        """

        :param eve_id:
        :param args:
        :param time_sleep:
        :return:
        """
        eve_id = f"_{eve_id}"
        if not self.eve_id_valid(eve_id):
            raise Exception(f"Event id {eve_id} not found.")

        efunc = getattr(self, eve_id)
        efunc(time_sleep, *args)

    def com(
            self, com_id: str, args: Optional[List[IN_STRUCT]] = None,
            time_sleep: float = 0.1, wait: bool = False
    ) -> Optional[OUT_STRUCT]:
        """

        :param wait:
        :param com_id:
        :param args:
        :param time_sleep:
        :return:
        """
        com_id = com_id.upper()

        if "G " == com_id[0:2]:
            var_id = self.__req_coms[com_id]
            return self.get(var_id, time_sleep=time_sleep, wait=wait)

        elif "G" == com_id:
            return self.get(time_sleep=time_sleep, wait=wait)

        else:
            var_id = self.__eve_coms[com_id]
            self.run(var_id, args, time_sleep)

    def com_inter(self, com_str: str,
                  time_sleep: float = 0.1) -> Optional[OUT_STRUCT]:
        """

        :param com_str:
        :param time_sleep:
        :return:
        """
        try:
            com_str = com_str.upper()
            wait = com_str[-2:] == " W"
            com_str = com_str[0:-2] if wait else com_str
            init_com_ls = com_str.split("/")
            com_ls = init_com_ls[0].split("->")
            var_id = com_ls[0].strip()

            if len(com_ls) > 1:
                args = com_ls[1].strip().split(chr(32))
            else:
                args = []

            if len(init_com_ls) > 1:
                time_sleep = float(init_com_ls[1].strip())

            return self.com(var_id, args, time_sleep=time_sleep, wait=wait)

        except Exception as err:
            err_str = f"ERROR: {err}"
            print(Back.LIGHTRED_EX, Fore.BLACK + err_str + Style.RESET_ALL)
            return err_str

    def inter(self, com_ls: List[str]) -> List[Tuple[str, OUT_STRUCT]]:
        ret = []
        for com_ln in com_ls:
            ret.append((com_ln, self.com_inter(com_ln)))

        return ret

    def pinfo(self):
        for get_id, val in self.get(wait=True).items():
            print(Fore.YELLOW + f"{get_id}:" + Fore.CYAN +
                  f" {val} {REQ_IDS_MAP[get_id]['UNITS']}" + Style.RESET_ALL)


if __name__ == "__main__":
    import pdb
    pdb.set_trace()
