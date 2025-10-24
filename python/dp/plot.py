"""
Provide a data visualization class.
"""
import warnings
import logging
from itertools import cycle
import operator as op
from typing import Any, Sequence, List, Callable
import numpy as np
from numpy.typing import NDArray
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import ticker
from matplotlib.colors import ListedColormap, Colormap
from lvn.dp.utils import (
    progress, make_sim_title, make_name_title, make_multisim_title,
)
from lvn.dp.dplvn import PERIODIC   #type: ignore

warnings.filterwarnings("ignore")

__all__ = [
    "GraphingBase", 
    "Viz"
]

class GraphingBase:
    """
    Provide a visualization base class.

    Args:
        dpi:
            resolution for rasterized images
        font_size:
            general font size

    Attributes:
        dpi (int):
            resolution for rasterized images
        font_size (int):
            general font size
        fdict  (dict):
            dictionary to which each figure is appended as it is generated
        colors  (list):
            list of colors
        n_colors  (int):
            number of colors
        color_cycle  (:obj:`itertools cycle <itertools.cycle>`):
            color property cycle
        markers  (list):
            list of markers
        n_markers  (:obj:`itertools cycle <itertools.cycle>`):
            number of markers
        marker_cycle  (int):
            cycle of markers
        linestyle_list  (list):
            list of line styles (solid, dashdot, dashed, custom dashed)
        color (:obj:`lambda(i) <lambda>`):
            return i^th color
        marker (:obj:`lambda(i) <lambda>`):
            return i^th marker
    """

    dpi: int
    font_size: int
    fdict: dict[Any, Any]
    colors: Callable
    n_colors: int
    color_cycle: Callable
    markers: tuple
    n_markers: int
    marker_cycle: cycle
    linestyle_list: tuple
    color: Callable
    marker: Callable
    font_family: str

    def __init__(self, dpi: int = 100, font_size: int = 11) -> None:
        """Initialize."""
        self.dpi = dpi
        self.font_size = font_size
        self.fdict = {}
        prop_cycle = plt.rcParams["axes.prop_cycle"]
        self.colors = prop_cycle.by_key()["color"]  # type: ignore
        self.n_colors = len(self.colors)  # type: ignore
        self.color_cycle = cycle(self.colors)  # type: ignore
        self.markers = ("o", "s", "v", "p", "*", "D", "X", "^", "h", "P")
        self.n_markers = len(self.markers)
        self.marker_cycle = cycle(self.markers)
        self.linestyle_list = ("solid", "dashdot", "dashed", (0, (3, 1, 1, 1)))

        color_ = lambda i_: self.colors[i_ % self.n_colors]  # type: ignore
        marker_ = lambda i_: self.markers[i_ % self.n_markers]  # type: ignore
        self.color = color_  # type: ignore
        self.marker = marker_  # type: ignore
        self.font_family = "Arial" #if "Arial" in self.get_fonts() else "Helvetica"
        try:
            mpl.rc("font", size=self.font_size, family=self.font_family)
        except:
            mpl.rc("font", size=self.font_size, family="")

    def get_fonts(self) -> List[str]:
        """Fetch the names of all the font families available on the system."""
        fpaths = matplotlib.font_manager.findSystemFonts()
        fonts: list[str] = []
        for fpath in fpaths:
            try:
                font = matplotlib.font_manager.get_font(fpath).family_name
                fonts.append(font)
            except RuntimeError as re:
                logging.debug(f"{re}: failed to get font name for {fpath}")
                pass
        return fonts

    def create_figure(
        self,
        fig_name: str,
        fig_size: tuple[float, float] | None = None,
        dpi: int | None = None,
    ) -> Figure:
        """
        Initialize a :mod:`Pyplot <matplotlib.pyplot>` figure.

        Set its size and dpi, set the font size,
        choose the Arial font family if possible,
        and append it to the figures dictionary.

        Args:
            fig_name:
                name of figure; used as key in figures dictionary
            fig_size:
                optional width and height of figure in inches
            dpi:
                rasterization resolution

        Returns:
            :obj:`Pyplot figure <matplotlib.figure.Figure>`:
                reference to :mod:`MatPlotLib/Pyplot <matplotlib.pyplot>`
                figure
        """
        fig_size_: tuple[float, float] = (
            (8, 8) if fig_size is None else fig_size
        )
        dpi_: float = self.dpi if dpi is None else dpi
        logging.info(
            "gmplib.plot.GraphingBase:\n   "
            + f"Creating plot: {fig_name} size={fig_size_} @ {dpi_} dpi"
        )
        fig = plt.figure()
        self.fdict.update({fig_name: fig})
        if fig_size_ is not None:
            fig.set_size_inches(*fig_size_)
        fig.set_dpi(dpi_)
        return fig

    def get_aspect(self, axes: plt.Axes) -> float: #type: ignore
        """
        Get aspect ratio of graph.

        Args:
            axes:
                the `axes` object of the figure

        Returns:
            float:
                aspect ratio
        """
        # Total figure size
        figWH: tuple[float, float] \
            = tuple(axes.get_figure().get_size_inches())  #type: ignore
        figW, figH = figWH
        # Axis size on figure
        bounds: tuple[float, float, float, float] = axes.get_position().bounds
        _, _, w, h = bounds
        # Ratio of display units
        disp_ratio: float = (figH * h) / (figW * w)
        # Ratio of data units
        # Negative over negative because of the order of subtraction
        # logging.info(axes.get_ylim(),axes.get_xlim())
        data_ratio: float = op.sub(*axes.get_ylim()) / op.sub(*axes.get_xlim())
        aspect_ratio: float = disp_ratio / data_ratio
        return aspect_ratio

    def naturalize(self, fig: Figure) -> None:
        """Adjust graph aspect ratio into 'natural' ratio."""
        axes: plt.Axes = fig.gca() #type: ignore
        # x_lim, y_lim = axes.get_xlim(), axes.get_ylim()
        # axes.set_aspect((y_lim[1]-y_lim[0])/(x_lim[1]-x_lim[0]))
        axes.set_aspect(1 / self.get_aspect(axes))

    def stretch(
        self,
        fig: Figure,
        xs: tuple[float, float] | None = None,
        ys: tuple[float, float] | None = None,
    ) -> None:
        """Stretch graph axes by respective factors."""
        axes: plt.Axes = fig.gca() #type: ignore
        if xs is not None:
            x_lim = axes.get_xlim()
            x_range = x_lim[1] - x_lim[0]
            axes.set_xlim(
                x_lim[0] - x_range * xs[0], x_lim[1] + x_range * xs[1]
            )
        if ys is not None:
            y_lim = axes.get_ylim()
            y_range = y_lim[1] - y_lim[0]
            axes.set_ylim(
                y_lim[0] - y_range * ys[0], y_lim[1] + y_range * ys[1]
            )

class Viz(GraphingBase):
    """
    Visualization class.
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
        fig_size: tuple[float,float] = (6.5, 6.5,)
        fig = self.create_figure(fig_name=name, fig_size=fig_size,)

        prefix: str = (
            r"$\rho(\mathbf{x},t=$" + f"{t_epoch:0{n_digits+2}.1f}" + r"$)$  "
        )
        title = make_sim_title(
            parameters, analysis,
        )
        plt.title(prefix+title, fontdict={"size":10},)

        color_palette: str = "inferno_r"
        color_map: Colormap = plt.get_cmap(color_palette) #type: ignore
        grid_: NDArray = np.flipud(density.T)
        n_pad_ud: int
        n_pad_lr: int
        if (
            do_extend_if_periodic 
            and parameters["grid_topologies"][0]==PERIODIC
        ):
            n_pad_ud = max(grid_.shape[0]//5, 10)
            grid_ = np.vstack([grid_, grid_[:n_pad_ud]])
        if (
            do_extend_if_periodic 
            and parameters["grid_topologies"][1]==PERIODIC
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
        color_bar: Any = plt.colorbar(
            shrink=0.35, pad=0.05, aspect=12, ticks=ticks, extend="max",
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
            parameters, analysis,
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
            parameters_list[0], analysis_list[0], do_omit_a=True,
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
                f"{round(Δ*1e3,n_digits-3):01.1f}" if do_label_Δ 
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
            title=r"$10^3(a-a_c)$", title_fontsize=8,
            loc=("upper left" if do_rescale else "lower left"),
        )
        plt.grid(ls=":")
        plt.close()
        return fig