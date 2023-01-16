from typing import Optional, Union, Dict, Callable, List
from SimConnect import AircraftRequests, AircraftEvents
from time import sleep

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
            find_func = lambda x_set: lambda *y_args: print(
                f"TEST: Executing command {x_set}, Args: {y_args}"
            )

            def _find_func(in_event_id: str):
                def _in_f1(*in_args):
                    print(
                        f"TEST: Executing command {in_event_id}, Args: {in_args}"
                    )
                return _in_f1

            find_func = _find_func

        else:
            find_func = eve.find

        def final_find_func(main_event_id: str, cast_logic: Callable):
            def in_find_func(time_sleep: float,
                             *z_args: List[Union[str, int, float]]):
                find_func(main_event_id)(*[cast_logic(in_z) for in_z in z_args])
                if time_sleep > 0:
                    sleep(time_sleep)
            return in_find_func

        set_vars = {f"_{x_main}": final_find_func(x_main, y_main["CAST_LOGIC"])
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
            var_ids = self.get_var_ids()
            ret = dict()
            for var_id in var_ids:
                ret[var_id] = getattr(self, var_id)

            return ret


if __name__ == "__main__":
    import pdb
    pdb.set_trace()
