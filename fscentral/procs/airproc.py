from aircraft.aircraft_class import Aircraft
from auxiliary.structs import PROC_INPUT_STRUCT, IN_STRUCT
import abc
from typing import Dict


class AirProc(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        self.airplane = airplane
        self.com = self.airplane.com_inter
        self.inputs = inputs

    @abc.abstractmethod
    def exproc(self, **inputs):
        """

        :param inputs:
        :return:
        """
        return

    def get_inputs(self, inputs: Dict[str, IN_STRUCT]) -> Dict[str, IN_STRUCT]:
        """

        :param inputs:
        :return:
        """
        inputs = {x.upper(): y for x, y in inputs.items()}
        for inp in self.inputs:
            inp_name, inp_def = inp
            inputs[inp_name] = inp_def if inputs.get(inp_name) is None else inputs[inp_name]

        return inputs

    # generic sub-procedures
    def set_max_autobrake(self):
        """

        :return:
        """
        for _ in range(6):
            self.com("ABR I / 0.1")

    def get_next_alt(self, floating_alt: int, land_alt: int) -> int:
        """

        :param floating_alt:
        :param land_alt:
        :return:
        """
        val = None
        count = 0
        zval = False
        while (val is None) or (val == 0):
            val = self.com("G WP NX ALT W")
            count += 1
            if count > 100:
                zval = True
                break

        g_alt = self.com("G GD ALT W")

        if zval:
            red_alt = round(((self.com("G ALT W") - g_alt) * .75) + g_alt)
            return max(floating_alt + land_alt, red_alt)

        else:
            return round(val)
