from typing import Union, Dict, List, Tuple

IN_STRUCT = Union[str, int, float]
OUT_STRUCT = Union[str, int, float, Dict[str, IN_STRUCT]]
PROC_INPUT_STRUCT = List[Tuple[str, IN_STRUCT]]