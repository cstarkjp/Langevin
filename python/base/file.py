"""
Write to files.
"""
import warnings
import logging
from typing import Any, Callable, Sequence, List
from os.path import exists, join, realpath, pardir
from os import mkdir
from shutil import rmtree
from json import dump, load
from io import TextIOWrapper
from langevin.base.serialize import (
    from_serializable, to_serializable,
)
from langevin.base.utils import progress, progress_disabled

warnings.filterwarnings("ignore")

__all__ = [
    "create_dir",
    "create_directories",
    "import_info",
    "export_info",
    "read_info",
    "export_plots",
    "export_plot"
]

def create_directories(
        results_path: Sequence = ("..", "experiments",), 
        results_dir: str = "Demo",
        do_clean: bool=False,
    ) -> str:
    """
    Create results parent and target directory.

    Args:
        results_path: path to parent results directory
            (to be created if necessary)
        results_dir: target results directory (to be created)

    Returns:
        path to target results directory.
    """
    results_path_ = ["."] + list(results_path)
    create_dir(join(*results_path_))
    results_dir_ = results_path_ + [results_dir]
    if do_clean and exists(join(*results_dir_)):
        rmtree(join(*results_dir_))
    return create_dir(join(*results_dir_))

def create_dir(dir: str) -> str:
    """
    Try to create an output directory if one doesn't exist.

    Throws an exception if the directory cannot be created.
    Returns quietly if the directory already exists.

    Args:
        dir: 
            name of directory

    Returns:
        path to directory.
    """
    try:
        if not exists(dir):
            mkdir(dir)
        else:
            return dir
    except OSError:
        print(f'Cannot create directory "{realpath(dir)}"')
        raise
    except Exception:
        print(Exception)
        raise
    return dir

def import_info(
        info_dir: str, 
        file_name: str,
        module: Any,
        # encoding: str = "utf-8",
    ) -> dict:
    """
    Read and adapt parameters specified in a JSON file.

    Args:
        info_dir: parent folder of JSON file
        file_name:  JSON file name.
        module: dplvn or other class module

    Returns: info as dictionary.
    """
    file: TextIOWrapper
    raw_info: dict
    info_path = [str(info_dir)] + [f"{file_name}.json"]
    with open(join(*info_path), "rb",) as file:
        raw_info = load(file)
    parameters: dict = {}
    for item_ in raw_info["Parameters"].items():
        parameters.update({item_[0]: from_serializable(item_[1], module)})
    info: dict = {
        "Analysis": raw_info["Analysis"],
        "Parameters": parameters,
        "Misc":  raw_info["Misc"]
    }
    return info

def export_info(
        info_dir: str, 
        file_name: str, 
        source_dict: dict, 
        module: Any,
        suffix: str | None = None,
        encoding: str = "utf-8", #"latin-1"
    ) -> tuple[dict, str]:
    """
    Export results dictionary to JSON file.

    Tries to ensure all dictionary entries are
    serializable by running `latex`
    on keys and converting values to floats.

    Args:
        info_dir: target parent folder
        file_name: name of output JSON file
        module: dplvn or other class module
        source_dict: dictionary of results, possibly requiring conversion
            from latex form such that serialization into a JSON file
            is possible
        suffix: to append to filename prior to addition of '.json' extension
    
    Returns:
        serialized dictionary and the file path string
    """
    # A bit of recursion for a change
    def render_serializable(source, module,) -> dict:
        serialized: dict = {}
        for item_ in source.items():
            if type(item_[1]) is dict:
                serialized.update(
                    {item_[0]: render_serializable(item_[1], module,)}
                )
            else:
                serialized.update(
                    {item_[0]: to_serializable(item_[1], module,)}
                )
        return serialized

    serializable_dict: dict = render_serializable(source_dict, module,)
    info_path = [str(info_dir)] + [
        str(file_name) + ("_"+suffix if suffix is not None else "") + ".json"
    ]

    file: TextIOWrapper
    with open(join(*info_path), "w", encoding=encoding,) as file:
        logging.info(join(*info_path))
        dump(serializable_dict, file, indent=4, ensure_ascii=False,) #separators=(", \n", ": ")
    return (serializable_dict, info_dir,)

def read_info(
        path: Sequence[str],
        module: Any,
        # encoding: str = "utf-8",
    ) -> tuple[str, dict]:
    """
    Wrapper around method to import info dictionary.

    Args:
        path: to info JSON file.
        module: dplvn or other class module

    Returns:
        path to file and imported dictionary
    """
    full_path: str = join(*path,)
    info: dict = import_info(full_path, "Info", module,)
    return (full_path, info,)

def export_plots(
        fig_dict: dict,
        results_dir: str,
        file_types: list[str] | tuple[str] | str = "png",
        suffix: str = "",
        dpi: int = 150,
        do_verbose: bool=False,
    ) -> str:
    """
    Export plots to PDF or other format files.

    Args:
        fig_dict: dictionary of figures
        results_dir: name of output directory
        file_types: file format (or list of file formats)
        suffix: filename suffix
        dpi: output image resolution
        do_verbose: use tqdm progress bar to track 

    Returns:
        the supplied export directory
    """
    results_path: str = realpath(results_dir)
    logging.info(
        "gmplib.save.export_plots:\n   " + f'Writing to dir: "{results_path}"'
    )
    file_types_: List[str] = (
        file_types if isinstance(file_types, list) else [str(file_types)]
    )
    progress_bar: Callable = (
        progress if do_verbose else progress_disabled
    )
    for file_type in file_types_:
        # logging.info(f'Image file type: "{file_type}"')
        for fig_name, fig in progress_bar(fig_dict.items(),):
            export_plot(
                fig_name, fig,
                results_path,
                file_type=file_type,
                suffix=suffix,
                dpi=dpi,
            )
    return results_dir

def export_plot(
        fig_name: str,
        fig: Any,
        results_dir: str,
        file_type: str = "pdf", 
        suffix: str = "",
        dpi: int | None = None,
    ) -> None:
    """
    Export plot to PDF or other format file.

    Args:
        fig_name: name to be used for file (extension auto-appended)
        fig: figure object
        results_dir: name of output directory
        file_type: file format
        suffix: filename suffix
        dpi: output image resolution
    """
    fig_name_ = f"{fig_name}{suffix}.{file_type.lower()}"
    # print(f"{fig_name_} exists: {exists(join(results_dir, fig_name_))}")
    try:
        # logging.info(f'dpi={dpi}')
        fig.savefig(
            join(results_dir, fig_name_),
            bbox_inches="tight",
            pad_inches=0.05,
            dpi=dpi,
            format=file_type,
        )
        logging.info(f'export_plot: Exported "{fig_name_}"')
    except OSError:
        logging.info(
            f'export_plot: Failed to export figure "{fig_name_}"'
        )
        raise
    except:
        raise
