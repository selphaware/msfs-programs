from typing import Optional, Union, Dict
from SimConnect import AircraftRequests, AircraftEvents
from time import sleep

from aircraft.find_funcs import test_find_func, wrap_find_func
from aircraft.idmap.event_map import EVE_IDS_MAP
from idmap.request_map import REQ_IDS_MAP

INIT_VAL = -9999


class Aircraft(object):
    def __init__(self,
                 req: Optional[AircraftRequests] = None,
                 eve: Optional[AircraftEvents] = None):
        """

        :param req:
        :param eve:
        """
        self.__req = req
        self.__eve = eve

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

    def get_var_ids(self):
        return [x_id.upper()
                for x_id in self.__dict__.keys() if not ("_" == x_id[0])]

    def var_id_valid(self, var_id: str) -> bool:
        return var_id.upper() in self.get_var_ids()

    def refresh(self, req_id: Optional[str] = None,
                tsleep: float = 0.0) -> None:
        """

        :param tsleep:
        :param req_id:
        :return:
        """
        if self.__req is None:
            raise Exception("Requests variable req cannot be None.")

        if req_id is not None:
            if not self.var_id_valid(req_id):
                raise Exception(f"Request id {req_id} not found.")

            var_ids = [req_id]

        else:
            var_ids = self.get_var_ids()

        for var_id in var_ids:
            setattr(self, var_id, self.__req.get(var_id))
            if tsleep > 0:
                sleep(tsleep)

    def get(self, req_id: Optional[str] = None, refresh_vals: bool = True) -> Union[
        str, int, float, Dict[str, Union[str, int, float]]
    ]:
        """

        :param req_id:
        :param refresh_vals:
        :return:
        """
        if refresh_vals:
            self.refresh(req_id)

        if req_id is not None:
            return getattr(self, req_id)

        else:
            return {var_id: getattr(self, var_id) for var_id in self.get_var_ids()}


if __name__ == "__main__":
    import pdb
    pdb.set_trace()
