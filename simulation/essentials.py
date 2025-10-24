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
import ffmpeg #type: ignore
from lvn.dp import dplvn  #type: ignore
sys.path.insert(0, os.path.join(os.path.pardir, "Packages"))
import lvn.dp.initialize
from lvn.dp.simulation import Simulation
from lvn.dp.ensemble import Ensemble
from lvn.dp.utils import (progress, set_name, make_dataframe, bold)
from lvn.dp.plot import Viz #type: ignore
from lvn.dp.image import fetch_image
from lvn.dp.file import (    
    create_directories, create_dir, 
    import_info, read_info, export_info, export_plots,
)

font_size = 11
font_family = "Arial"
try:
    mpl.rc("font", size=font_size, family=font_family)
except:
    mpl.rc("font", size=font_size, family="")

pp = PrettyPrinter(indent=4).pprint
