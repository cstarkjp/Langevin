"""
Ensemble simulation of Langevin eqn evolution.
"""
import warnings
from typing import Any
from collections.abc import Callable, Sequence
from multiprocessing.pool import Pool as Pool
from multiprocessing import cpu_count
from copy import deepcopy
import numpy as np
from numpy.typing import NDArray
import os
from langevin.base.file import (
    create_directories, export_info, read_info, export_plots
)
from langevin.dp import dplvn
from langevin.dp.simulation import Simulation
from langevin.dp.vizdp import VizDP #type: ignore

warnings.filterwarnings("ignore")

__all__ = [
    "Ensemble"
]

class Ensemble:
    """
    Multiprocessing wrapper class to batch run Langevin integrations.
    """
    def __init__(
            self, info_path: Sequence[str], do_verbose: bool=False,
        ) -> None:
        """
        Constructor.

        Args:
            info_path: 
                file path to `Info.json` broken up into tuple/list of strings
            do_verbose: 
                flag whether to use `tqdm` progress bar, and report operations
        """
        self.info: dict
        _, self.info = read_info(info_path, dplvn)
        self.info["Misc"]["path"] = info_path
        self.do_verbose =  do_verbose
        if do_verbose:
            print(f"Ensemble results path:  {self.info["Misc"]["path"]}")

        # n_max_cores: int = self.misc["n_max_cores"]
        n_cores: int = cpu_count()
        self.info["Misc"]["n_cores"] = n_cores
        n_sims: int = self.info["Misc"]["n_sims"]
        n_subcritical: int = (n_sims//2)
        n_supercritical: int = n_sims - n_subcritical
        Δa: float = self.info["Misc"]["Δa_range"]/n_subcritical
        a_c: float = self.info["Analysis"]["a_c"]
        n_round: int = self.info["Misc"]["n_digits"]

        a_list: list[float] = list(filter(lambda a: a>=0, (
            [round(a_c-Δa*i_, n_round) for i_ in range(n_subcritical, 0, -1)]
            +
            [round(a_c+Δa*i_, n_round) for i_ in range(0, n_supercritical)]
        )))[::-1]
        b_list: list[float] = [self.info["Parameters"]["quadratic"]]*n_sims
        seed_list: list[int] = [
            self.info["Parameters"]["random_seed"]*(i_+1) 
            for i_ in range(n_sims)
        ]
        assert n_sims==len(a_list)

        self.info_list: list[dict] = [
            deepcopy(self.info) for _ in range(n_sims)
        ]
        for (info_, a_, b_,seed_) in zip(
            self.info_list, a_list, b_list, seed_list,
        ):
            info_["Parameters"]["linear"] = a_
            info_["Parameters"]["quadratic"] = b_
            info_["Parameters"]["random_seed"] = seed_
        if self.do_verbose:
            print(f"a: {[round(a_,5) for a_ in a_list]}")
            print(f"b: {[round(b_,5) for b_ in b_list]}")
            print(f"seeds: {[seed_ for seed_ in seed_list]}")
        
        self.graphs: VizDP

    def create(self) -> None:
        """
        Generate list of [`Simulation`][langevin.dp.simulation.Simulation] instances.
        """
        self.sim_list: list[Simulation] = []
        sim_: Simulation
        keys: Sequence[str] = (
            "linear", "quadratic", "diffusion", "noise", "random_seed",
        )
        for key_ in keys:
            self.info["Parameters"][key_+"_list"] = []
            del self.info["Parameters"][key_]
        n_sims: int = self.info["Misc"]["n_sims"]
        n_cores: int = self.info["Misc"]["n_cores"]
        for i_, info_ in enumerate(self.info_list):
            # Progress bar only for the last in each n_core batch
            do_verbose_: bool = (
                self.do_verbose 
                if i_%n_cores==0
                # if i_%n_cores==n_cores-1 or i_==n_sims-1
                else False
            )
            sim_ = \
                Simulation(
                    name=None,
                    path=info_["Misc"]["path"], 
                    # Don't send a reference to the source info!
                    info=deepcopy(info_), 
                    do_verbose=do_verbose_,
                )
            self.sim_list += [sim_]
            if self.do_verbose:
                print(f"Simulation#{i_+1} path:  {sim_.misc["path"]}")
            for key_ in keys:
                self.info["Parameters"][key_+"_list"] +=[sim_.parameters[key_]]

    def initialize(self) -> None:
        """
        Carry out initialization of each 
        [`Simulation`][langevin.dp.simulation.Simulation] instance.
        """
        for sim_ in self.sim_list:
            sim_.initialize()

    @staticmethod
    def sim_exec_wrapper(sim: Simulation) -> Sequence[tuple]:
        """
        Pool wrapper to execute a specific sim instance.

        Returns:
            serialized output returned by the completed sim.
        """
        result: Sequence[tuple]
        try:
            if sim.do_verbose:
                print(f"Sim exec starting: {sim}")
            result = sim.exec()
        except:
            print(f"Sim exec error: {sim}")
        finally:
            if sim.do_verbose:
                print(f"Sim exec completion: {sim}")
        return result
    
    def exec_multiple_sims(self, function: Callable,) -> list[Sequence[tuple]]:
        """
        Carry out the `multiprocessing` parallelization of the ensemble of sims.

        Args:
            function: wrapper passed to pool to act on each sim instance.

        Returns:
            list of serialized outputs returned by each completed sim.
        """
        ensemble_results: list[Sequence[tuple]]
        with Pool(processes=self.info["Misc"]["n_cores"]) as pool:
            ensemble_results = (pool.map(function, self.sim_list,))
        return ensemble_results

    def exec(self) -> None:
        """
        Execute an ensemble of sims in parallel using `multiprocessing`.
        """
        ensemble_results: list[Sequence[tuple]] \
            = self.exec_multiple_sims(self.sim_exec_wrapper)
        for (sim_results_, sim_,) in zip(ensemble_results, self.sim_list):
            sim_.t_epochs = np.array(sim_results_[0])
            sim_.mean_densities = np.array(sim_results_[1])
            sim_.misc["computation_time"] = sim_results_[2]
            self.info["Misc"]["computation_time"] = sim_results_[2]
        self.info["Misc"]["dplvn_version"] \
            = self.sim_list[0].misc["dplvn_version"]
        self.info["Misc"]["date_time"] \
            = self.sim_list[0].misc["date_time"]

    def multi_plot(self) -> None:
        """
        Generate graphs of the ensemble results.
        """
        if not hasattr(self, "graphs"):
            self.graphs = VizDP()
        self.graphs.multiplot_mean_density_evolution(
            "ρ_t_loglog",
            self.info, self.sim_list,
            do_rescale=False, y_sf=0.75,
        )
        self.graphs.multiplot_mean_density_evolution(
            "ρ_t_rescaled",
            self.info, self.sim_list,
            do_rescale=True,
        )
        # self.graphs.multiplot_mean_density_evolution(
        #     "ρ_t_finitesize",
        #     self.info, self.list,
        #     do_rescale=True,
        #     do_finitesize=True,
        # )

    def plot(self) -> None:
        """
        Generate graphs for results from a single sim.
        """
        for sim_ in self.sim_list:
            sim_.plot()

    def save(self, module: Any, do_dummy: bool=False,) -> None:
        """
        Export Outfo.json, graphs, and data files.

        Args:
            do_dummy: only create & report anticipated output folders.

        Depending on Info.json settings, output also may be carried out 
        for all simulations into separate folders.
        """
        outfo_path: str = \
            create_directories(self.info["Misc"]["path"], "",)
        if self.do_verbose:
            print(f"experiments outfo path:  {outfo_path}")
        if not do_dummy:
            _ = export_info(outfo_path, "Outfo", self.info, module,)

        graphs_path: str = \
            create_directories(self.info["Misc"]["path"], "",)
        if self.do_verbose:
            print(f"Combo graph path:  {graphs_path}")
        if self.info["Misc"]["do_export_combo_graphs"] and not do_dummy:
            _ = export_plots(
                self.graphs.fdict, 
                graphs_path,
                do_verbose=False,
            )

        data_path: str = \
            create_directories(self.info["Misc"]["path"], "",)
        if self.do_verbose:
            print(f"Combo data path:  {outfo_path}")
        if self.info["Misc"]["do_export_combo_data"]:
            t_epochs: NDArray = self.sim_list[0].t_epochs
            mean_densities: NDArray = np.array([
                sim_.mean_densities for sim_ in self.sim_list
            ])
        if not do_dummy:
            np.savez_compressed(
                os.path.join(data_path, "combo_ρ_t",), 
                t_epochs=t_epochs,
                mean_densities=mean_densities,
            )

        if self.info["Misc"]["do_export_data"]:
            for (i_, sim_) in enumerate(self.sim_list):
                sim_.save(dplvn, do_dummy, do_verbose=True,)
