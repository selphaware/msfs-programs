from time import sleep
from typing import Callable

from aircraft.structs import IN_STRUCT


def test_find_func(in_event_id: str):
    """

    :param in_event_id:
    :return:
    """
    def _in_f1(*in_args: IN_STRUCT):
        """

        :param in_args:
        :return:
        """
        print(
            f"TEST: Executing command {in_event_id}, Args: {in_args}"
        )

    return _in_f1


def wrap_find_func(ff_func: Callable):
    """

    :param ff_func:
    :return:
    """
    def final_find_func(main_event_id: str, cast_logic: Callable):
        """

        :param main_event_id:
        :param cast_logic:
        :return:
        """
        def in_find_func(
                time_sleep: float,
                *z_args: IN_STRUCT
                ):
            """

            :param time_sleep:
            :param z_args:
            :return:
            """
            ff_func(main_event_id)(*[cast_logic(in_z) for in_z in z_args])

            if time_sleep > 0:
                sleep(time_sleep)

        return in_find_func

    return final_find_func
