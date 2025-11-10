"""
Serialization of dictionary items.
"""
import warnings
from typing import Any
import builtins
import numpy as np
from json import dumps

warnings.filterwarnings("ignore")

__all__ = [
    "is_serializable",
    "to_serializable",
    "from_serializable",
]

def is_serializable(value: Any,) -> bool:
    """
    Check value is serializable and can be written to a JSON file.

    Args:
        value: to be checked.

    Returns: 
        true if value is serializable.
    """
    try:
        dumps(value)
        return True
    except TypeError:
        return False

def to_serializable(value: Any, module: Any,) -> Any:
    """
    Convert value into serializable version.

    Args:
        value: to be converted.
        module: dplvn or other class module

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
        case module.GridDimension:
            match value:
                case module.D1:
                    return "D1"
                case module.D2:
                    return "D2"
                case module.D3:
                    return "D3"
                case _:
                    return None
        case module.InitialCondition:
            match value:
                case module.RANDOM_UNIFORM:
                     return "RANDOM_UNIFORM"
                case module.RANDOM_GAUSSIAN:
                     return "RANDOM_GAUSSIAN"
                case module.CONSTANT_VALUE:
                     return "CONSTANT_VALUE"
                case module.SINGLE_SEED:
                     return "SINGLE_SEED"
                case _:
                    return None
        case module.IntegrationMethod:
            match value:
                case module.RUNGE_KUTTA:
                    return "RUNGE_KUTTA"
                case module.EULER:
                    return "EULER"
                case _:
                    return None
        case builtins.tuple:
            if is_serializable(value[0]) and is_serializable(value):
                return value
            combo: list = []
            for value_ in value:
                match value_:
                    case module.BOUNDED:
                        combo += ["BOUNDED"]
                        continue
                    case module.PERIODIC:
                        combo += ["PERIODIC"]
                        continue
                    case module.FLOATING:
                        combo += ["FLOATING"] 
                        continue
                    case module.FIXED_VALUE:
                        combo += ["FIXED_VALUE"] 
                        continue
                    case module.FIXED_FLUX :
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
    
def from_serializable(value: Any, module: Any) -> Any:
    """
    Convert dict from serializable version.

    Args:
        value: to be converted.
        module: dplvn or other class module

    Returns:  converted value.
    """
    match type(value):
        case builtins.str:
            match value:
                case "D1":
                    return module.D1
                case "D2":
                    return module.D2
                case "D3":
                    return module.D3
                case "RANDOM_UNIFORM":
                    return module.RANDOM_UNIFORM
                case "RANDOM_GAUSSIAN":
                    return module.RANDOM_GAUSSIAN
                case "CONSTANT_VALUE":
                    return module.CONSTANT_VALUE
                case "SINGLE_SEED":
                    return module.SINGLE_SEED
                case "RUNGE_KUTTA":
                    return module.RUNGE_KUTTA
                case "EULER":
                    return module.EULER
                case _:
                    return None
        case builtins.tuple | builtins.list:
            combo: list = []
            if type(value[0])!=builtins.str:
                return tuple(value)
            for value_ in value:
                match value_:
                    case "BOUNDED":
                        combo += [module.BOUNDED]
                        continue
                    case "PERIODIC":
                        combo += [module.PERIODIC]
                        continue
                    case "FLOATING":
                        combo += [module.FLOATING]
                        continue
                    case "FIXED_VALUE":
                        combo += [module.FIXED_VALUE]
                        continue
                    case "FIXED_FLUX":
                        combo += [module.FIXED_FLUX]
                        continue
                    case _:
                        combo += [None]
                        continue
            return tuple(combo)
        case _:
            return value
