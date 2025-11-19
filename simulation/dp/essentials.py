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
pp = PrettyPrinter(indent=4).pprint

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

fpaths = mpl.font_manager.findSystemFonts()
fonts: list[str] = []
for fpath in fpaths:
    try:
        font = mpl.font_manager.get_font(fpath).family_name
        fonts.append(font)
    except RuntimeError as re:
        pass
font_size = 11
if "Arial" in fonts:
    mpl.rc("font", size=font_size, family="Arial")
elif "DejaVu Sans" in fonts:
    mpl.rc("font", size=font_size, family="DejaVu Sans")
else:
    mpl.rc("font", size=font_size, family="Helvetica")

import warnings
warnings.filterwarnings("ignore")
