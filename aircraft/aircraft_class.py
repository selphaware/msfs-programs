from typing import Optional, Union, Dict, List
from SimConnect import AircraftRequests, AircraftEvents
from time import sleep

from aircraft.find_funcs import test_find_func, wrap_find_func
from aircraft.idmap.event_map import EVE_IDS_MAP
from aircraft.idmap.request_map import REQ_IDS_MAP

INIT_VAL = -9999


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

        # GET Simulation Variables
        get_vars = {x: y["CAST_LOGIC"](INIT_VAL)
                    for x, y in REQ_IDS_MAP.items()}

        self.__dict__.update(get_vars)

        # SET Simulation Variables
        if eve is None:
            find_func = test_find_func

        else:
            find_func = eve.find

        set_vars = {f"_{x_main}": wrap_find_func(find_func)(x_main,
                                                            y_main["CAST_LOGIC"])
                    for x_main, y_main in EVE_IDS_MAP.items()}

        self.__dict__.update(set_vars)

        # Initialise GET attributes
        if not test:
            self.refresh(initialise=True)

        # Initialise COMmand variables
        get_coms = {x: y["COMMAND"] for x, y in REQ_IDS_MAP.items()}
        self.req_coms = get_coms

        set_coms = {x_main: y_main["COMMAND"]
                    for x_main, y_main in EVE_IDS_MAP.items()}
        self.eve_com = set_coms

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
                initialise: bool = False) -> None:
        """

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

            setattr(self, var_id, self.__req.get(var_id))

    def get(self, req_id: Optional[str] = None,
            refresh_vals: bool = True, time_sleep: float = 0.0,
            request_refresh: bool = False) -> Union[
        str, int, float, Dict[str, Union[str, int, float]]
    ]:
        """

        :param request_refresh:
        :param time_sleep:
        :param req_id:
        :param refresh_vals:
        :return:
        """
        if refresh_vals and not self.__test:
            self.refresh(req_id, initialise=request_refresh)

        if time_sleep > 0:
            sleep(time_sleep)

        if req_id is not None:
            return getattr(self, req_id)

        else:
            return {var_id: getattr(self, var_id) for var_id in self.get_req_ids()}

    def run(self, eve_id: str,
            args: Optional[List[Union[str, int, float]]] = None,
            time_sleep: float = 0.1) -> None:
        eve_id = f"_{eve_id}"
        if not self.eve_id_valid(eve_id):
            raise Exception(f"Event id {eve_id} not found.")

        efunc = getattr(self, eve_id)
        efunc(time_sleep, *args)

    def com(self, com_id):
        pass


if __name__ == "__main__":
    import pdb
    pdb.set_trace()
