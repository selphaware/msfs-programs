from simprocs import *
import sys


if __name__ == "__main__":
    args = [""] if not len(sys.argv[1:]) else sys.argv[1:]
    test = args[0].upper() == "TEST"
    sc = SimCentral(test=test)
    sp = SimProcs(sc)
    sp.inter()
