from aircraft.aircraft_class import Aircraft
from fscentral.procs.airproc import AirProc
from auxiliary.structs import PROC_INPUT_STRUCT


class ApproachLandProc(AirProc):
    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        super().__init__(airplane, inputs)
        self.__name = "APPROACH_LAND"

    def exproc(self, **inputs):
        pass
