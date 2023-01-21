from aircraft.aircraft_class import Aircraft
from auxiliary.structs import PROC_INPUT_STRUCT, IN_STRUCT
import abc
from typing import Dict


class AirProc(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        self.airplane = airplane
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
        for inp in self.inputs:
            inp_name, inp_def = inp
            inputs[inp_name] = inp_def if inputs[inp_name] is None else inputs[inp_name]

        return inputs
