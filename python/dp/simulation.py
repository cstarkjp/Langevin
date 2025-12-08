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
try:
    import ffmpeg
except:
    # Quietly fail
    pass
import sys, os
from os.path import join, pardir, isfile
from os import listdir, remove
sys.path.insert(0, join(pardir, "Packages"))
from langevin.base.file import (
    create_directories, export_info, export_plots,
)
from langevin.base.utils import (
    progress, progress_disabled, set_name,
)
from langevin.dp import dplvn
from langevin.dp.vizdp import VizDP

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4).pprint

# Possible fix to Windows issue with printing unicode characters 
import io
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

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
        self.sim = dplvn.SimDP(
            **self.parameters, 
            do_snapshot_grid=self.do_snapshot_grid,
            do_verbose=self.do_verbose,
        )
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
            self.sim.postprocess()
            if not self.sim.postprocess():
                raise Exception("Failed to process sim results")
            t_epoch_ = np.round(
                self.sim.get_t_current_epoch(), 
                self.misc["n_round_Δt_summation"]
            )
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
        self.t_epochs = np.round(
            self.sim.get_t_epochs(), 
            self.misc["n_round_Δt_summation"]
        )
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
        """Plot everything"""
        self.plot_graphs()
        self.plot_images()

    def plot_graphs(self, do_profile: bool=False,) -> None:
        """
        Generate all the required graphs.
        """
        self.graphs: VizDP = VizDP()
        self.graphs.plot_mean_density_evolution(
            "ρ_t_loglog",
            self.parameters, 
            self.analysis, 
            self.misc,
            self.t_epochs, 
            self.mean_densities, 
            do_rescale=False, 
            y_sf=0.75,
        )
        self.graphs.plot_mean_density_evolution(
            "ρ_t_rescaled",
            self.parameters, 
            self.analysis, 
            self.misc,
            self.t_epochs, 
            self.mean_densities, 
            do_rescale=True,
        )
        if do_profile:
            t_final = self.t_epochs[-1]
            self.graphs.plot_density_profile(
                "ρ_y_wall",
                self.parameters, 
                self.analysis, 
                self.density_dict, 
                self.t_epochs, 
                t_final*0.2,
                t_final,
                y_offset=self.parameters["dx"],
                y_sf=0.705,
                y_limits=(3e-3, None,),
        )

    def plot_images(self) -> None:
        """
        Generate all the required images.
        """
        self.images: VizDP = VizDP()
        t_epochs: tuple = tuple(self.density_dict.keys())
        if len(t_epochs)==0: 
            return None
        t_last: float = t_epochs[-1]
        n_digits: int = len(f"{t_last:0{self.misc["n_digits"]}.1f}".replace(".","p"))
        # print(f"ρ_t{0:0{n_digits}.1f}".replace(".","p"))
        # print(f"ρ_t{t_last:0{n_digits}.1f}".replace(".","p"))
        name_: str 
        density_: NDArray
        progress_bar: Callable = (
            progress if self.do_verbose else progress_disabled
        )
        for i_epoch_, t_epoch_ in progress_bar(enumerate(self.density_dict.keys())):
            name_ =  f"ρ_t{t_epoch_:0{n_digits}.1f}".replace(".","p")
            density_ = self.density_dict[t_epoch_]
            # print(i_epoch_, t_epoch_, name_, density_.shape)
            self.density_image_dict[i_epoch_] = self.images.plot_density_image(
                name_, 
                self.parameters, 
                self.analysis,
                t_epoch_, 
                density_, 
                density_max=3,
                tick_Δρ=1,
                do_extend_if_periodic=False,
                n_digits=n_digits,
            )

    def save(
            self, module: Any, do_dummy: bool=False, do_verbose: bool=False,
        ) -> str | None:
        """
        Export outfo JSON, graphs, and data files.

        Args:
            module: dplvn or other class module
            do_dummy: just print (possibly create) the output folders
            do_verbose: report how the exporting is going
        """
        try:
            if self.do_verbose | do_verbose:
                print(f"Outfo|graphs|videos|data path:  {self.misc["path"]}")
        except:
            print(f"Issue printing Outfo|graphs|videos|data path")
        seed_dir_name: str = f"rs{self.parameters["random_seed"]}"
    
        outfo_path: str = \
            create_directories(
                self.misc["path"], seed_dir_name,
            )
        outfo: dict = {
            "Parameters" : self.parameters,
            "Analysis" : self.analysis,
            "Misc" : self.misc
        }        
        if not do_dummy:
            _ = export_info(outfo_path, "Outfo", outfo, module,)

        if self.misc["do_export_data"]:
            data_path: str = \
                create_directories(
                    (*self.misc["path"], seed_dir_name,), ".", 
                )
            if not do_dummy:
                np.savez_compressed(
                    join(data_path, "ρ_t",), 
                    t_epochs=self.t_epochs,
                    mean_densities=self.mean_densities,
                )
                data_npz: NpzFile = np.load(
                    join(data_path, "ρ_t"+".npz",), 
                )
                data_npz["t_epochs"][-10:], data_npz["mean_densities"][-10:]

        if self.misc["do_export_graphs"]:
            graphs_path: str = \
                create_directories(
                    (*self.misc["path"], seed_dir_name,), ".",
                )
            if not do_dummy:
                _ = export_plots(
                        self.graphs.fdict, 
                        graphs_path,
                        do_verbose=self.do_verbose,
                    )

        if "do_export_images" in self.misc and self.misc["do_export_images"]:
            images_path: str = \
                create_directories(
                    (*self.misc["path"], seed_dir_name,), "Images", 
                )
            if not do_dummy:
                # Remove all pre-existing image files, if any
                for filename_ in listdir(images_path):
                    file_path_ = join(images_path, filename_)
                    if isfile(file_path_):
                        remove(file_path_)
                _ = export_plots(
                        self.images.fdict, 
                        images_path,
                        do_verbose=self.do_verbose,
                    )

        if self.misc["do_make_video"]:
            videos_path: str = create_directories(
                (*self.misc["path"], seed_dir_name,), ".",
            )

            video_frame_rate: int = self.misc["video_frame_rate"]
            video_format: str = self.misc["video_format"]
            n_digits: int = self.misc["n_digits"]+1
            # video_images_wildcard: str = "ρ_t"+"?"*n_digits+".png"
            video_images_wildcard: str = "ρ_t*.png"
            # video_images_wildcard: str = f"ρ_t%0{n_digits-2}p0.png"
            try:
                input = ffmpeg.input( 
                    join(images_path, video_images_wildcard), 
                    pattern_type="glob",  
                    framerate=video_frame_rate, 
                    # pix_fmt="yuv420p",
                    analyzeduration="2000000",
                    probesize="2000000",
                )
                print(f"ffmpeg input:   '{input}'")
            except:
                raise Exception("Failed to set ffmpeg input")
            try:
                output = ffmpeg.output(
                    input.video,
                    join(
                        videos_path, 
                        f"ρ_{seed_dir_name}.{video_format}"
                    ),
                    vf="crop=floor(iw/2)*2:floor(ih/2)*2",
                    vcodec="libx264",
                    format=video_format,
                )
                print(f"ffmpeg output:   '{output}'")
            except:
                raise Exception("Failed to set ffmpeg output")
            try:
                stderr_output: str \
                    = output.overwrite_output().run(capture_stderr=True,)
                # print(f"ffmpeg stderr_output:   '{stderr_output}'")
            except:
                raise Exception("Failed to run ffmpeg")
            return None
        
        return None