from typing import Any, Sequence, Callable
import time
from time import perf_counter
from datetime import datetime, timedelta
import sys, os
from os.path import pardir, join
from shutil import rmtree
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.colors import ListedColormap, Colormap
import numpy as np
from numpy.typing import NDArray
from numpy.lib.npyio import NpzFile
from pprint import PrettyPrinter

try:
    import ffmpeg
except:
    print("ffmpeg not installed: videos cannot be generated")
sys.path.insert(0, join(pardir, "Packages"))
import langevin.base.initialize
from langevin.base.utils import (
    progress, set_name, make_dataframe, bold, fetch_image
)
from langevin.base.serialize import from_serializable, to_serializable
from langevin.base.file import (    
    create_directories, create_dir, 
    import_info, read_info, export_info, export_plots,
)
from langevin.dp import dplvn
from langevin.dp.simulation import Simulation
from langevin.dp.ensemble import Ensemble
from langevin.dp.vizdp import VizDP

font_size = 11
font_family = "Arial"
try:
    mpl.rc("font", size=font_size, family=font_family)
except:
    mpl.rc("font", size=font_size, family="")

pp = PrettyPrinter(indent=4).pprint
