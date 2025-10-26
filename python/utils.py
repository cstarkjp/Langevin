"""
Utility functions.
"""
import warnings
from typing import Callable
from functools import partial
from pandas import DataFrame
from tqdm import tqdm

warnings.filterwarnings("ignore")

__all__ = [
    "progress",
    "bold",
    "set_name",
    "make_multisim_title",
    "make_name_title",
    "make_dataframe",
]

progress: Callable = partial(tqdm, colour="green",)
progress_disabled: Callable = partial(tqdm, colour="green", disable=True,)

def bold(string: str) -> str: 
    """Boldify a string for printing in a terminal"""
    return ("\033[1m" + string + "\033[0m")

def set_name(
    p: dict,
    a: dict,
    field_name: str | None=None,
    suffix: str="",
    t_epoch: float | None=None,
    do_parent: bool=False,
    do_dir: bool=False,
) -> str:
    """
    Define a simulation name string that includes model parameters for info.

    Args:
        p: parameters dictionary
        a: analysis dictionary
        field_name: name (e.g. 'ρ') of Langevin field variable
        suffix: optional
        t_epoch: time slice of sim
        do_parent: generate a 'parent' folder name
        do_dir: generate a detailed folder name
    
    Returns:
        name string
    """
    to = lambda x: ((f"{x}").replace(".","p",)).replace("-","neg",)
    to5 = lambda x: ((f"{x:0.5f}").replace(".","p",)).replace("-","neg",)
    name: str
    if do_dir:
        name = f"a{to5(p["linear"])}"
    else:
        name = \
            (field_name+"_" if field_name is not None else "") \
            + (f"" if do_parent else f"a{to5(p["linear"])}_") \
            + f"b{to(p["quadratic"])}" \
            + f"_D{to(p["diffusion"])}" \
            + f"_η{to(p["noise"])}" \
            + f"_x{p["grid_size"][0]}" \
            + f"_y{p["grid_size"][1]}" \
            + f"_Δx{to(p["dx"])}" \
            + f"_Δt{to(p["dt"])}" \
            + (to(f"_t{t_epoch:08.2f}") if t_epoch is not None else "") \
            + suffix
            # + f"_rs{to(p["random_seed"])}" 
    return name

def make_multisim_title(
    p: dict,
    analysis: dict,
    a_range: tuple[float, float] | None,
) -> str:
    """
    Define a title string to use when annotating plots.
    
    Args:
        p: parameters dictionary
        analysis: analysis dictionary
        a_range: span of values of linear coefficient "a"

    Returns:
        title string
    """
    # a_range may be in reverse order
        # + r"$n_\mathsf{sims}$"+f"={p.n_sims}   " \
    title: str = ""\
        + (
            rf"$a \in $[{min(a_range):0.4f}, {max(a_range):0.4f}]   " 
            if a_range is not None else ""
        ) \
        + rf"$b$={p["linear"]}   "  \
        + rf"$D$={p["diffusion"]}   " \
        + rf"$ς$={p["noise"]}   " \
        + "\n" \
        + rf"$a_c$={(analysis["a_c"]):0.4f}    " \
        + rf"$n_x$={p["n_x"]}   " \
        + rf"$n_y$={p["n_y"]}   "   \
        + rf"$\Delta$$x$={p["Δx"]}   " \
        + rf"$\Delta$$t$={p["Δt"]}   " \
        + rf"$t$={p["t_total"]:g}"
    return title

def make_name_title(
    field_name: str, 
    p: dict,
    analysis: dict,
    t_total: float | None = None,
    a_range: tuple[float, float] | None = None,
    do_multisim: bool = False,
) -> tuple[str,str]:
    """
    Define (file) name and (plot) title strings.

    Args:
        p: parameters dictionary
        analysis: analysis dictionary
        t_total: time span of simulation
        a_range: span of values of linear coefficient "a"
        do_multisim: flag if doing multiple simulations
        
    Returns:
        name and title strings as tuple
    """
    set_name_: Callable = partial(
        set_name,
        p,
        analysis,
        field_name,
    )
    name:str  = (
        set_name_(t_total=t_total, do_multisim=True,) 
        if do_multisim 
        else set_name_()
    )
    title: str = (
        make_multisim_title(p, analysis, a_range,) if do_multisim
        else make_sim_title(p, analysis, )
    )
    return (name, title,)
    
def make_dataframe(p: dict) -> DataFrame:
    """
    Convert a dictionary into a pandas dataframe to prettify it.

    The keys becomes the "index" column.
    The dictionary values become a column labeled "value".

    Args:
        p: input dictionary

    Returns:
        dataframe conversion
    """
    df: DataFrame \
        = DataFrame.from_dict(p, orient="index").rename_axis("name")
    df.rename(columns={0:"value"}, inplace=True,)
    return df
