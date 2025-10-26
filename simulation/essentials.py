from typing import Any, Sequence, Callable
import time
from time import perf_counter
from datetime import datetime, timedelta
import sys, os
from shutil import rmtree
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.colors import ListedColormap, Colormap
import numpy as np
from numpy.typing import NDArray
from numpy.lib.npyio import NpzFile
from pprint import PrettyPrinter
import ffmpeg
sys.path.insert(0, os.path.join(os.path.pardir, "Packages"))
import lvn.initialize
from lvn.image import fetch_image
from lvn.utils import (
    progress, set_name, make_dataframe, bold
)
from lvn.file import (    
    create_directories, create_dir, 
    import_info, read_info, export_info, export_plots,
)
from lvn.dp import dplvn
from lvn.dp.simulation import Simulation
from lvn.dp.ensemble import Ensemble
from lvn.dp.vizdp import VizDP
from lvn.serialize import from_serializable, to_serializable

font_size = 11
font_family = "Arial"
try:
    mpl.rc("font", size=font_size, family=font_family)
except:
    mpl.rc("font", size=font_size, family="")

pp = PrettyPrinter(indent=4).pprint
