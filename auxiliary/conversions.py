from math import pi


MAX_VAL = 2 ** 14 - 1  # 16383
KM_TO_NM_RATIO = 1.852
M_TO_FT_RATIO = 3.28084


IDENTITY = lambda x: x

INT_CONV = lambda x: int(float(x))

RAD_TO_DEG_HALF = lambda x: (1 - (x / pi)) * (180 / pi)

RAD_TO_DEG = lambda x: x * (180 / pi)

KM_TO_NM = lambda x: x / 1000 / KM_TO_NM_RATIO

PCT_CNVT = lambda x: x * 100

MACH_CNVT = lambda x: x * 10

PCT_REVR = lambda x: round(float(x) * MAX_VAL / 100)

FLAP_CNV = lambda x: PCT_REVR(x * 100 / 30)  # 0 - 30 degrees range for flaps

M_TO_FT = lambda x: round(x * M_TO_FT_RATIO)

BOOL_CHK = lambda x: x == 1
INIT_VAL = -9999
