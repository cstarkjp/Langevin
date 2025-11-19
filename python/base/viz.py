"""
Base data visualization class.
"""
import warnings
import logging
from itertools import cycle
import operator as op
from typing import Any, List, Callable
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.axes import Axes

warnings.filterwarnings("ignore")

__all__ = ["Viz"]

class Viz:
    """
    Provide a visualization base class.

    Args:
        dpi:
            resolution for rasterized images
        font_size:
            general font size

    Attributes:
        dpi:
            resolution for rasterized images
        font_size:
            general font size
        fdict:
            dictionary to which each figure is appended as it is generated
        colors:
            list of colors
        n_colors:
            number of colors
        color_cycle:
            color property cycle
        markers:
            list of markers
        n_markers:
            number of markers
        marker_cycle:
            cycle of markers
        linestyle_list:
            list of line styles (solid, dashdot, dashed, custom dashed)
        color:
            return i^th color
        marker:
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
        font_size = 11
        fonts = self.get_fonts()
        if "Arial" in fonts:
            self.font_family="Arial"
        elif "DejaVu Sans" in fonts:
            self.font_family="DejaVu Sans"
        else:
            self.font_family="Helvetica"
        mpl.rc("font", size=font_size, family=self.font_family)

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
        Initialize a `MatPlotLib` figure.

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
            reference to figure
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

    def get_aspect(self, axes: Axes) -> float: #type: ignore
        """
        Get aspect ratio of graph.

        Args:
            axes:
                the `axes` object of the figure

        Returns:
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
        axes: Axes = fig.gca() #type: ignore
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
        axes: Axes = fig.gca() #type: ignore
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

