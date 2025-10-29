"""
Simulation of Langevin eqn evolution.
"""
import warnings
from collections.abc import Callable, Sequence
from typing import Any
from multiprocessing.pool import Pool as Pool
from time import perf_counter
from datetime import datetime, timedelta
from numpy.typing import NDArray
import numpy as np
from numpy.lib.npyio import NpzFile
import sys, os
sys.path.insert(0, os.path.join(os.path.pardir, "Packages"))
from lvn.file import (
    create_directories, export_info, export_plots,
)
from lvn.utils import (
    progress, progress_disabled, set_name,
)
from lvn.dp import dplvn
from lvn.dp.vizdp import VizDP

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4).pprint
warnings.filterwarnings("ignore")

__all__ = [
    "Simulation", 
]
class Simulation:
    """
    Class to manage a single DP Langevin field integration.
    """
    def __init__(
            self, 
            name: str | None, 
            path: list[str], 
            info: dict, 
            do_snapshot_grid: bool=False,
            do_verbose: bool=True,
        ) -> None:
        """
        Constructor.

        Args:
            name: of sim constructed from parameters etc
            path: path to file
            info: dictionary containing sim coefficients, model parameters, etc
            do_snapshot_grid: flag whether to copy out final time-slice
                density grid into numpy array
            do_verbose: flag whether to use tqdm progress bar, report 
                from `dplvn.SimDP`
        """
        self.analysis: dict = info["Analysis"]
        self.parameters: dict = info["Parameters"]
        self.misc: dict = info["Misc"]

        # Henkel et al, 2008
        self.analysis.update({
            "dp_β": 0.5834,
            "dp_ν_pp": 0.7333,
            "dp_ν_ll": 1.2950,
            "dp_δ": 0.4505,
            "dp_z": 1.7660,
        })
        self.misc["path"] = path + [set_name(
            self.parameters, self.analysis, do_dir=True,
        )]
        if name is None:
            self.misc["name"] = set_name(
                self.parameters, self.analysis, do_dir=False,
            )
        # elif name!=set_name(self.parameters, self.analysis,):
        #     raise NameError(f"Problem with {name}")
        else:
            self.misc["name"] = name
            self.misc["path"] = path
        # else:
        #     raise NameError(f"Problem with {name}")
        self.misc["dplvn_version"] = dplvn.__version__
        self.misc["date_time"] \
            = datetime.now().replace(microsecond=0).isoformat(sep=" ")

        self.do_snapshot_grid: bool = do_snapshot_grid
        self.do_verbose: bool = do_verbose
        self.t_epochs: NDArray = np.empty([])
        self.mean_densities: NDArray= np.empty([])
        self.density_dict: dict[float, NDArray] = {}
        self.density_image_dict: dict[int, Any] = {}
    
    def initialize(self) -> None:
        """
        Create and initialize a `dpvln.SimSP` class instance.
        """
        self.sim = dplvn.SimDP(**self.parameters, do_verbose=self.do_verbose,)
        if not self.sim.initialize(self.misc["n_round_Δt_summation"]):
            raise Exception("Failed to initialize sim")
        self.analysis["n_epochs"] = self.sim.get_n_epochs()
                
    def run(self) -> None:
        """
        Execute a `dpvln.SimSP` simulation.
        """
        n_segments: int = self.misc["n_segments"]
        n_epochs: int = self.analysis["n_epochs"]
        n_segment_epochs: int = (n_epochs-1) // n_segments
        if (n_segment_epochs*n_segments+1)!=n_epochs:
            raise Exception(
                f"Failed to segment sim with {n_epochs} epochs "
                + f"into {n_segments} segment(s)"
            )
        progress_bar: Callable = (
            progress if self.do_verbose else progress_disabled
        )
        def step(i_segment_: int,):
            if i_segment_>0 and not self.sim.run(n_segment_epochs):
                raise Exception("Failed to run sim")
            if not self.sim.postprocess():
                raise Exception("Failed to process sim results")
            t_epoch_ = self.sim.get_t_current_epoch()
            if self.do_snapshot_grid:
                self.density_dict[t_epoch_] = self.sim.get_density()
        # This ridiculous verbiage is needed because tqdm, even when
        #   disabled, generates some "leaked semaphore objects" errors
        #   when invoked in a `multiprocessing` process
        i_segment_: int
        if self.do_verbose:
            for i_segment_ in progress_bar(range(0, n_segments+1, 1)):
                step(i_segment_)
        else:
            for i_segment_ in range(0, n_segments+1, 1):
                step(i_segment_)
        self.t_epochs = self.sim.get_t_epochs()
        self.mean_densities = self.sim.get_mean_densities()

    def run_wrapper(self) -> str:
        """
        Wrapper around `dpvln.SimSP` run to provide timing.

        Returns:
            printable string describing computation (sim run) time
        """
        tick: float = perf_counter()
        self.run()
        tock: float = perf_counter()
        self.misc["computation_time"] = f"{timedelta(seconds=round(tock-tick))}"
        return (f"Computation time = {self.misc["computation_time"]}")

    def exec(self) -> Sequence[tuple]:
        """
        Carry out all simulation steps, including initialization & running.

        Returns:
            serialized versions of sim epoch times, mean grid densities, and 
            computation run time.
        """
        self.initialize()
        computation_time_report: str = self.run_wrapper()
        if self.do_verbose:
            print(computation_time_report)
        return (
            tuple(self.t_epochs.tolist()), 
            tuple(self.mean_densities.tolist()),
            self.misc["computation_time"],
        )

    def plot(self) -> None:
        """
        Generate all the required graphs and images.
        """
        self.graphs: VizDP = VizDP()
        self.images: VizDP = VizDP()
        self.graphs.plot_mean_density_evolution(
            "ρ_t_loglog",
            self.parameters, self.analysis, self.misc,
            self.t_epochs, self.mean_densities, 
            do_rescale=False, y_sf=0.75,
        )
        self.graphs.plot_mean_density_evolution(
            "ρ_t_rescaled",
            self.parameters, self.analysis, self.misc,
            self.t_epochs, self.mean_densities, 
            do_rescale=True,
        )

    def save(
            self, 
            module: Any,
            do_dummy: bool=False, 
            do_verbose: bool=False,
        ) -> None:
        """
        Export outfo JSON, graphs, and data files.

        Args:
            module: dplvn or other class module
            do_dummy: just print (possibly create) the output folders
            do_verbose: report how the exporting is going
        """
        if self.do_verbose | do_verbose:
            print(f"Outfo/graph/data path:  {self.misc["path"]}")
        seed_dir_name: str = f"rs{self.parameters["random_seed"]}"
    
        outfo_path: str = \
            create_directories(
                (os.path.pardir, *self.misc["path"]), seed_dir_name,
            )
        outfo: dict = {
            "Parameters" : self.parameters,
            "Analysis" : self.analysis,
            "Misc" : self.misc
        }        
        if not do_dummy:
            _ = export_info(outfo_path, "Outfo", outfo, module,)

        if self.misc["do_export_graphs"]:
            graphs_path: str = \
                create_directories(
                    (os.path.pardir,  *self.misc["path"], seed_dir_name,), ".",
                )
            if not do_dummy:
                _ = export_plots(
                        self.graphs.fdict, 
                        graphs_path,
                        do_verbose=self.do_verbose,
                    )

        if self.misc["do_export_data"]:
            data_path: str = \
                create_directories(
                    (os.path.pardir, *self.misc["path"], seed_dir_name,), ".", 
                )
            if not do_dummy:
                np.savez_compressed(
                    os.path.join(data_path, "ρ_t",), 
                    t_epochs=self.t_epochs,
                    mean_densities=self.mean_densities,
                )
                data_npz: NpzFile = np.load(
                    os.path.join(data_path, "ρ_t"+".npz",), 
                )
                data_npz["t_epochs"][-10:], data_npz["mean_densities"][-10:]
