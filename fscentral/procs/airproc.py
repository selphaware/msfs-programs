from aircraft.aircraft_class import Aircraft
from auxiliary.structs import PROC_INPUT_STRUCT
import abc


class AirProc(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        self.comc = airplane
        self.inputs = inputs

    @abc.abstractmethod
    def exproc(self, **inputs):
        """

        :param inputs:
        :return:
        """
        return
