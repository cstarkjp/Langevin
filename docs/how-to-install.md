# How to install

0. *Experimental*: using `uv`, the creation of a virtual Python environment, installation of dependent packages, and installation of `lvn` itself can all be achieved in three simple command lines:

        uv venv

        source .venv/bin/activate

        uv pip install --index-url https://test.pypi.org/simple/ \
                       --extra-index-url https://pypi.org/simple/  lvn

    Alternatively, follow the more standard approach as outlined below.

1. Install Python $\geq$ 3.12, ideally in a Python environment; Python 3.14 is recommended, and current development uses this version. 

    The following packages are needed by `lvn` (`ffmpeg` is optional); they can be installed by hand at this point, or left to install automatically during the next step (by `pip`):
    
    - `numpy`
    - `jupyter`
    - `ipython`
    - `matplotlib`  
    - `pandas`
    - `tqdm`
    - `ffmpeg-python`

    

2. Install the [Python library `lvn`](https://test.pypi.org/project/lvn/) using `pip`, hopefully within a Python environment, from TestPyPI:

        pip install --index-url https://test.pypi.org/simple/ \
                    --extra-index-url https://pypi.org/simple lvn

    Note: the `--extra-index-url` argument ensures that any Python install
    dependencies are also sought in the true PyPI repository rather
    than in TestPyPI alone (which generally won't suffice). 

    _If you already have a pre-existing installation_ of this package, you may need to `upgrade` (update) to the latest version:

    
        pip install -i https://test.pypi.org/simple/ lvn --upgrade

3. Clone the [Langevin repo](https://github.com/cstarkjp/Langevin/tree/main) to your local machine:

        git clone https://github.com/cstarkjp/Langevin.git

    which will create a `Langevin/` folder. 

    If you already have a local copy of the repo, update it with `git pull`, making sure you are on the `main` branch (do `git checkout main`).
