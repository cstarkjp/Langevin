"""
Utility functions.
"""
import warnings
from lvn.dp import dplvn

warnings.filterwarnings("ignore")

__all__ = [
    "make_sim_title",
]

def make_sim_title(
    p: dict,
    analysis: dict,
    do_omit_a: bool=False,
) -> str:
    """
    Define a title string to use when annotating plots.
  
    Args:
        p: parameters dictionary
        analysis: analysis dictionary
        do_omit_a: skip linear coefficient "a" in string

    Returns:
        title string
    
    """
    def grid_topology(i: int) -> str:
        return "bnd" if p["grid_topologies"][i]==dplvn.BOUNDED else "pdc"

    def boundary_condition(i: int) -> str:
        match p["boundary_conditions"][i]:
            case dplvn.FIXED_VALUE:
                return "fxd"
            case dplvn.FIXED_FLUX:
                return "flx"
            case dplvn.FLOATING:
                return "flt"
            case _:
                return "";
        
    title: str = ""\
        + (
            rf"$a$={p["linear"]:0.5f}   " if not do_omit_a 
            else rf"$a_c \approx ${analysis["a_c"]:0.5f}              "
        ) \
        + rf"$b$={p["quadratic"]}   " \
        + rf"$D$={p["diffusion"]}   " \
        + rf"$η$={p["noise"]}" \
        + (
            rf"      $rs$={p["random_seed"]}      " if not do_omit_a 
            else "          "
        ) \
        + (
            rf"$a_c \approx ${analysis["a_c"]:0.5f}" if not do_omit_a 
            else ""
        ) \
        + "\n" \
        + rf"$n_x$={p["grid_size"][0]}  " \
        + rf"$n_y$={p["grid_size"][1]}   "   \
        + rf"$\Delta$$x$={p["dx"]}   " \
        + rf"$\Delta$$t$={p["dt"]}   " \
        + rf"gt:({grid_topology(0)}, {grid_topology(1)})  " \
        + rf"bc:({boundary_condition(0)}, {boundary_condition(1)}, " \
            +rf"{boundary_condition(2)}, {boundary_condition(3)})   " 
        # + (rf"$t$={t_epoch:08.2f}     " if t_epoch is not None else "")
    return title