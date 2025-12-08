"""
Provide a data visualization class.
"""
import warnings
from typing import Any
from functools import reduce
import numpy as np
from numpy.typing import NDArray
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap, Colormap
from langevin.base.viz import Viz
from langevin.base.utils import make_sim_title
from langevin.dp import dplvn

warnings.filterwarnings("ignore")

__all__ = ["VizDP"]

class VizDP(Viz):
    """
    Visualization class for directed percolation simulations.
    """
    def plot_density_image(
            self,
            name: str, 
            parameters: dict,
            analysis: dict,
            t_epoch: float, 
            density: NDArray,
            density_max: float=5,
            tick_Δρ: float=0.5,
            do_extend_if_periodic: bool=False,
            n_digits: int=6,
        ) -> Figure:
        """
        Generate an image grid of the Langevin density field.

        Args:
            name: of figure to be used as key in viz dictionary
            parameters: sim parameters dictionary
            analysis: sim analysis dictionary
            t_epoch: time slice of density grid
            density: the sliced density field
            density_max: upper bound for rendering density
            tick_Δρ: step in density colorbar labeling
            do_extend_if_periodic: artificially extend grid by ~20% in periodic directions
            n_digits: number of digits to be used in title when printing linear coefficient a

        Returns:
            Matplotlib figure instance.
        """
        aspect_ratio: float = reduce(lambda nx, ny: nx/ny, parameters["grid_size"])
        sf: float = (aspect_ratio)**(0.3)/1.15
        fig_size: tuple[float,float] = (6.5*sf, 6.5/sf,)
        fig = self.create_figure(fig_name=name, fig_size=fig_size,)

        prefix: str = (
            r"$\rho(\mathbf{x},t=$" + f"{t_epoch:0{n_digits-1}.0f}" + r"$)$  "
            # r"$\rho(\mathbf{x},t=$" + f"{t_epoch:0{n_digits+2}.1f}" + r"$)$  "
        )
        title = make_sim_title(
            parameters, analysis, dplvn,
        )
        plt.title(prefix+title, fontdict={"size":10},)

        color_palette: str = "inferno_r"
        color_map: Colormap = plt.get_cmap(color_palette) #type: ignore
        grid_: NDArray = np.flipud(density.T)
        n_pad_ud: int
        n_pad_lr: int
        if (
            do_extend_if_periodic 
            and parameters["grid_topologies"][0]==dplvn.PERIODIC
        ):
            n_pad_ud = max(grid_.shape[0]//5, 10)
            grid_ = np.vstack([grid_, grid_[:n_pad_ud]])
        if (
            do_extend_if_periodic 
            and parameters["grid_topologies"][1]==dplvn.PERIODIC
        ):
            n_pad_lr = max(grid_.shape[1]//5, 10)
            grid_ = np.hstack([grid_, grid_[:,:n_pad_lr]])
        (n_ud, n_lr,) = grid_.shape
        # print((n_ud, n_lr,))
        plt.imshow(
            grid_,  
            extent=(0, n_lr, 0, n_ud), 
            cmap=color_map,
            vmin=0, vmax=density_max,
        )
        ticks: NDArray = np.arange(0, density_max+1, tick_Δρ,)
        bar_shrink: float
        if n_lr/n_ud<3:
            bar_shrink = 0.35 
        elif n_lr/n_ud<4:
            bar_shrink = 0.23
        else:
            bar_shrink = 0.23 #0.17
        color_bar: Any = plt.colorbar(
            shrink=bar_shrink, pad=0.05, aspect=12, ticks=ticks, extend="max",
        )
        color_bar.set_label(r"$\rho(\mathbf{x},t)$  [-]")
        plt.xlabel(r"$x$   [-]")
        plt.ylabel(r"$y$   [-]")
        plt.close()
        return fig

    def plot_mean_density_evolution(
            self,
            name: str, 
            parameters: dict,
            analysis: dict,
            misc: dict,
            t_epochs: NDArray,
            mean_densities: NDArray,
            do_rescale: bool=False,
            do_loglog: bool=True,
            y_sf: float=1,
            n_digits: int=6,
        ) -> Figure:
        """
        Plot a graph of the mean density ρ(t) versus time t.

        Depending on the arguments, the graph may plot DP-rescaled values, 
        and may have log-log axes.

        Args:
            name: of figure to be used as key in viz dictionary
            parameters: sim parameters dictionary
            analysis: sim analysis dictionary
            misc: sim miscellaneous dictionary
            t_epochs: time slices of simulation
            mean_densities: grid-averaged density field during simulation
            do_rescale: plot DP-rescaled values
            do_loglog: use log axes
            y_sf: scale ρ values by this amount
            n_digits: number of digits to be used in title when printing linear coefficient a

        Returns:
            Matplotlib figure instance.
        """
        fig_size: tuple[float,float] = (6, 4,)
        fig = self.create_figure(fig_name=name, fig_size=fig_size,)
        title = make_sim_title(
            parameters, analysis, dplvn,
        )
        plt.title(title, fontdict={"size":11},)

        # See Hinrichsen 2010, table 2; Henkel et al 2008, tables 4.1, 4.3
        dp_β: float    = analysis["dp_β"]
        dp_ν_pp: float = analysis["dp_ν_pp"]
        dp_ν_ll: float = analysis["dp_ν_ll"]
        dp_δ: float    = analysis["dp_δ"]

        t : NDArray= t_epochs[mean_densities>0]
        md: NDArray = mean_densities[mean_densities>0]
        md = md[t>=5e-1]
        t = t[t>=5e-1]

        t_: NDArray
        md_: NDArray
        Δ_: float = np.abs(parameters["linear"]-analysis["a_c"])
        Δ: float = (Δ_ if np.abs(Δ_)>1e-20 else 10**(-n_digits))
        if do_rescale:
            # print(f"Δ={Δ}")
            t_ = Δ * t**(dp_ν_ll)
            md_ = md * t**(dp_β/dp_ν_ll)
            # md_ = md * t**(dp_δ)
        else:
            t_ = t
            md_ = md

        t_trend: NDArray 
        if do_loglog:
            t_trend = 10**np.arange(
                np.log10(t_[0]), max(5.0, np.log10(t_[-1]))+0.1, 0.1,
            )
        else:
            t_trend = t_
        md_trend: NDArray = (t_trend)**(-dp_δ) * (md_[0])

        plt.plot(t_, md_, "-", lw=0.5,)
        if not do_rescale:
            plt.plot(t_trend, md_trend*y_sf, "-",  lw=1, alpha=0.5,)

        if do_rescale:
            plt.xlabel(r"Rescaled time $|a-a_c|^{\nu_{||}}\, t$  [-]")
            plt.ylabel(
                r"Rescaled grid-mean density  "
                + r"$t^{\beta/\nu_{\perp}}\overline{\rho} $  [-]"
            )
            if do_loglog:
                plt.ylim(misc["ylimits_rescaled"])
                plt.xlim(misc["xlimits_rescaled"])
            else:
                plt.ylim(0, None,)
                plt.xlim(1e0, None,)
        else:
            plt.xlabel(r"Time $t$  [-]")
            plt.ylabel(r"Grid-mean density  $\overline{\rho}(t)$  [-]")
            if do_loglog:
                plt.ylim(misc["ylimits_log"])
                plt.xlim(misc["xlimits_log"])
            else:
                plt.autoscale(
                    enable=True, axis='both', tight=True,
                )
                plt.ylim(0, None,)
        if do_loglog:
            plt.loglog()

        plt.grid(ls=":")
        plt.close()
        return fig
    
    def multiplot_mean_density_evolution(
            self,
            name: str, 
            sims_info: dict,
            sims_list: list[Any],
            do_loglog: bool=True,
            do_rescale: bool=False,
            y_sf: float=1,
            n_digits: int=6,
            do_label_Δ: bool=True,
        ) -> Figure:
        """
        Plot an ensemble graph of the mean density ρ(t) versus time t for all sims.

        Depending on the arguments, the graph may plot DP-rescaled values, 
        and may have log-log axes.

        Args:
            name: of figure to be used as key in viz dictionary
            sims_info: dictionary of ensemble
            sims_list: list of all sim instances in the ensemble
            do_rescale: plot DP-rescaled values
            do_loglog: use log axes
            y_sf: scale ρ values by this amount
            n_digits: number of digits to be used in title when printing linear coefficient a
            do_label_Δ: compute Δ=a-a_c and label curves with it, instead of just a

        Returns:
            Matplotlib figure instance.

        """
        fig_size: tuple[float,float] = (6, 4,)
        fig = self.create_figure(fig_name=name, fig_size=fig_size,)
        sim_: Any
        parameters_list: list[dict] = [
            sim_.parameters for sim_ in sims_list
        ]
        analysis_list: list[dict] = [
            sim_.analysis for sim_ in sims_list
        ]
        t_epochs_list: list[NDArray] = [
            sim_.t_epochs for sim_ in sims_list
        ]
        mean_densities_list: list[NDArray] = [
            sim_.mean_densities for sim_ in sims_list
        ]
        title = make_sim_title(
            parameters_list[0], analysis_list[0], dplvn, do_omit_a=True,
        )
        plt.title(title, fontdict={"size":11},)

        # See Hinrichsen 2010, table 2; Henkel et al 2008, tables 4.1, 4.3
        dp_β: float    = analysis_list[0]["dp_β"]
        dp_ν_pp: float = analysis_list[0]["dp_ν_pp"]
        dp_ν_ll: float = analysis_list[0]["dp_ν_ll"]
        dp_δ: float    = analysis_list[0]["dp_δ"]
        dp_z: float    = analysis_list[0]["dp_z"]

        n_sims: int = len(sims_list)
        color_palette: str = "coolwarm" #"viridis_r"
        cmap: ListedColormap = mpl.colormaps[color_palette] #type: ignore
        color_list: NDArray = cmap(np.linspace(0, 1, n_sims,))*0.75 #type: ignore
        i_: int
        for (i_, (
            parameters_, analysis_, t_epochs_, mean_densities_, 
            color_
        )) in enumerate(zip(
            parameters_list, 
            analysis_list, 
            t_epochs_list, 
            mean_densities_list,
            color_list[::-1],
        )):
            t : NDArray= t_epochs_[mean_densities_>0]
            md: NDArray = mean_densities_[mean_densities_>0]
            md = md[t>=5e-1]
            t = t[t>=5e-1]

            t_: NDArray
            md_: NDArray
            Δ: float = parameters_["linear"]-analysis_["a_c"]
            # n_x: int = parameters_["grid_size"][0]
            # n_y: int = parameters_["grid_size"][1]
            # t_ = t**(dp_ν_ll)/(float(n_x*n_y))**dp_z
            if do_rescale:
                t_ = np.abs(Δ) * t**(dp_ν_ll)
                md_ = md * t**(dp_β/dp_ν_ll)
            else:
                t_ = t
                md_ = md

            if not do_rescale and np.abs(Δ)<1e-10:
                plt.plot(
                    t_trend, md_trend*y_sf, "k-",  lw=2, alpha=0.4,
                    zorder=10,
                )
            if np.abs(Δ)<1e-10 and do_rescale:
                continue

            t_trend: NDArray 
            if do_loglog:
                t_trend = 10**np.arange(
                    np.log10(t_[0]), max(5.0, np.log10(t_[-1]))+0.1, 0.1,
                )
            else:
                t_trend = t_
            md_trend: NDArray = (t_trend)**(-dp_δ) * (md_[0])

            label_: str = (
                f"{round(Δ*100,n_digits-2):01.1f}" if do_label_Δ 
                else f"{parameters_["linear"]:01.6f}"
            )
            plt.plot(
                t_, md_, "-", 
                color=color_, lw=0.5, alpha=0.7, zorder=n_sims-i_,
            )
            plt.plot(
                0*t_, 0*md_, "-", 
                color=color_, lw=1.5, alpha=1, label=label_, zorder=n_sims-i_,
            )

        if do_rescale:
            plt.xlabel(r"Rescaled time $|a-a_c|^{\nu_{||}}\, t$  [-]")
            plt.ylabel(
                r"Rescaled grid-mean density  "
                + r"$t^{\beta/\nu_{\perp}}\overline{\rho} $  [-]"
            )
            if do_loglog:
                plt.ylim(sims_info["Misc"]["ylimits_rescaled"])
                plt.xlim(sims_info["Misc"]["xlimits_rescaled"])
            else:
                plt.ylim(0, None,)
                plt.xlim(1e0, None,)
        else:
            plt.xlabel(r"Time $t$  [-]")
            plt.ylabel(r"Grid-mean density  $\overline{\rho}(t)$  [-]")
            if do_loglog:
                plt.ylim(sims_info["Misc"]["ylimits_log"])
                plt.xlim(sims_info["Misc"]["xlimits_log"])
            else:
                plt.autoscale(
                    enable=True, axis='both', tight=True,
                )
                plt.ylim(0, None,)
        if do_loglog:
            plt.loglog()

        plt.legend(
            fontsize=7, 
            title=r"$100(a-a_c)$", title_fontsize=8,
            loc=("upper left" if do_rescale else "lower left"),
        )
        plt.grid(ls=":")
        plt.close()
        return fig
    
    def plot_density_profile(
            self,
            name: str, 
            parameters: dict,
            analysis: dict,
            density_dict: dict,
            t_epochs: NDArray,
            t_begin: float,
            t_end: float,
            y_offset: float,
            do_loglog: bool=True,
            y_sf: float=0.71,
            y_limits: tuple[float|None, float|None] = (1e-2, None,),
        ) -> Figure:
        """
        Plot a graph of the time- and transverse-mean density ρ(t) versus wall distance.

        Args:
            name: of figure to be used as key in viz dictionary
            parameters: sim parameters dictionary
            analysis: sim analysis dictionary
            density_dict: density field snapshots
            t_epochs: time slices of simulation
            t_begin: when to begin time integration
            t_end: when to end time integration
            y_offset: effective distance of wall cell from boundary condition
            do_loglog: use log axes
            y_sf: scale ρ values by this amount
            y_limits: optionally control y axis limits

        Returns:
            Matplotlib figure instance.
        """
        fig_size: tuple[float,float] = (6, 4,)
        fig = self.create_figure(fig_name=name, fig_size=fig_size,)

        title = make_sim_title(
            parameters, analysis, dplvn,
        )
        plt.title(title, fontdict={"size":11},)

        dp_β: float    = analysis["dp_β"]
        dp_ν_pp: float = analysis["dp_ν_pp"]

        t_final = t_epochs[-1]
        subset_t_epochs = tuple(
            filter(lambda t: t>=t_begin and t<=t_end, density_dict.keys())
        )
        n_x, n_y = parameters["grid_size"]
        density_profile = reduce(
            lambda x, y: x + y, 
            [np.sum(density_dict[t_epoch_], axis=0,) 
            for t_epoch_ in subset_t_epochs]
        )/(len(subset_t_epochs)*n_x)
        dy = parameters["dx"]
        y_ = np.arange(n_y, 0, -1)*dy - dy/2 + y_offset
        plt.plot(
            y_, density_profile, "-", 
            label=r"DP simulation"
        )
        plt.plot(
            y_, y_**(-dp_β/dp_ν_pp)*y_sf, ":", 
            label=r"$\widebar\rho \sim y^{-\beta/\nu_{\!\perp}} \sim y^{-0.796}$"
        )
        if do_loglog:
            axes = plt.gca()
            axes.set_yscale("log")
            axes.set_xscale("log")
        plt.autoscale(enable=True, axis="x", tight=True,)
        plt.ylim(*y_limits)
        plt.ylabel(r"Time- & wall-parallel-averaged density  $\rho$")
        plt.xlabel(r"Distance from wall $y$")
        plt.legend(fontsize=11,)
        plt.grid(ls=":")
        plt.close()
        return fig