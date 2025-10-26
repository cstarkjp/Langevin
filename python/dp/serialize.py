"""
Write to files.
"""
import warnings
from typing import Any
import builtins
import numpy as np
from lvn.dp import dplvn
from lvn.utils import (
    progress, progress_disabled, 
)
from lvn.file import is_serializable

warnings.filterwarnings("ignore")

__all__ = [
    "to_serializable",
    "from_serializable",
    "import_info",
    "export_info",
    "read_info",
    "export_plots",
    "export_plot"
]

def to_serializable(value: Any,) -> Any:
    """
    Convert value into serializable version.

    Args:
        value: to be converted.

    Returns: 
        serializable value.
    """
    match type(value):
        case builtins.str:
            return value
        case np.float64 | builtins.float:
            return float(value)
        case builtins.int:
            return int(value)
        case builtins.bool:
            return value
        case builtins.list:
            return value
        case dplvn.GridDimension:
            match value:
                case dplvn.D1:
                    return "D1"
                case dplvn.D2:
                    return "D2"
                case dplvn.D3:
                    return "D3"
                case _:
                    return None
        case dplvn.InitialCondition:
            match value:
                case dplvn.RANDOM_UNIFORM:
                     return "RANDOM_UNIFORM"
                case dplvn.RANDOM_GAUSSIAN:
                     return "RANDOM_GAUSSIAN"
                case dplvn.CONSTANT_VALUE:
                     return "CONSTANT_VALUE"
                case dplvn.SINGLE_SEED:
                     return "SINGLE_SEED"
                case _:
                    return None
        case dplvn.IntegrationMethod:
            match value:
                case dplvn.RUNGE_KUTTA:
                    return "RUNGE_KUTTA"
                case dplvn.EULER:
                    return "EULER"
                case _:
                    return None
        case builtins.tuple:
            if is_serializable(value[0]) and is_serializable(value):
                return value
            combo: list = []
            for value_ in value:
                match value_:
                    case dplvn.BOUNDED:
                        combo += ["BOUNDED"]
                        continue
                    case dplvn.PERIODIC:
                        combo += ["PERIODIC"]
                        continue
                    case dplvn.FLOATING:
                        combo += ["FLOATING"] 
                        continue
                    case dplvn.FIXED_VALUE:
                        combo += ["FIXED_VALUE"] 
                        continue
                    case dplvn.FIXED_FLUX :
                        combo += ["FIXED_FLUX"] 
                        continue
                    case _:
                        combo += [None]
                        continue
            return combo
        case np.ndarray:
            return value.tolist()
        case _:
            return value
    
def from_serializable(value: Any,) -> Any:
    """
    Convert dict from serializable version.

    Args:
        value: To be converted.

    Returns:  Converted value.
    """
    match type(value):
        case builtins.str:
            match value:
                case "D1":
                    return dplvn.D1
                case "D2":
                    return dplvn.D2
                case "D3":
                    return dplvn.D3
                case "RANDOM_UNIFORM":
                    return dplvn.RANDOM_UNIFORM
                case "RANDOM_GAUSSIAN":
                    return dplvn.RANDOM_GAUSSIAN
                case "CONSTANT_VALUE":
                    return dplvn.CONSTANT_VALUE
                case "SINGLE_SEED":
                    return dplvn.SINGLE_SEED
                case "RUNGE_KUTTA":
                    return dplvn.RUNGE_KUTTA
                case "EULER":
                    return dplvn.EULER
                case _:
                    return None
        case builtins.tuple | builtins.list:
            combo: list = []
            if type(value[0])!=builtins.str:
                return tuple(value)
            for value_ in value:
                match value_:
                    case "BOUNDED":
                        combo += [dplvn.BOUNDED]
                        continue
                    case "PERIODIC":
                        combo += [dplvn.PERIODIC]
                        continue
                    case "FLOATING":
                        combo += [dplvn.FLOATING]
                        continue
                    case "FIXED_VALUE":
                        combo += [dplvn.FIXED_VALUE]
                        continue
                    case "FIXED_FLUX":
                        combo += [dplvn.FIXED_FLUX]
                        continue
                    case _:
                        combo += [None]
                        continue
            return tuple(combo)
        case _:
            return value
