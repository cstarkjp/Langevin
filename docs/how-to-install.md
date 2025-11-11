# How to install

<!-- ## **Step 1:** Set up **langevin** in a custom Python environment -->

### Best practice: use **uv**

Using `uv`, the creation of a virtual Python environment, installation of dependent packages, and installation of `langevin` itself can all be achieved in three simple command lines:

    uv venv
    source .venv/bin/activate
    uv pip install langevin

_Note that before doing this you'll have [to install `uv`](https://docs.astral.sh/uv/getting-started/installation/) on your machine._


### Alternative: by hand
Alternatively, you can employ the following two-step process.

1. Install Python $\geq$ 3.12, ideally in a Python environment; Python 3.14 is recommended, and current development uses this version. 

    The following packages are needed by `langevin`; they can be installed by hand at this point, or left to install automatically during the next step:
    
    - `numpy`
    - `jupyter`
    - `ipython`
    - `matplotlib`  
    - `pandas`
    - `tqdm`
    - `ffmpeg-python`

    If you are using `conda` or `miniconda`, refer to the [`environment.yml`](https://github.com/cstarkjp/Langevin/tree/main/environment.yml) 
    file on the project repo for help here.

2. Install the [Python library `langevin`](https://pypi.org/project/langevin/) using `pip`, hopefully within a Python environment, from PyPI:

        pip install langevin

    _If you already have a pre-existing installation_ of this package, you may need to `upgrade` (update) to the latest version:

        pip install langevin --upgrade

<!-- ## **Step 2:** Make a local copy of the demo scripts

Clone the [Langevin repo](https://github.com/cstarkjp/Langevin/tree/main) to your local machine:

        git clone https://github.com/cstarkjp/Langevin.git

which will create a `Langevin/` folder. 

If you already have a local copy of the repo, update it with `git pull`, making sure you are on the `main` branch (do `git checkout main`). -->