# How to install

## **Step 1:** Set up **langevin** in a custom Python environment

### Best practice: use **uv**

Using `uv`, the creation of a virtual Python environment, installation of dependent packages, and installation of `langevin` itself can all be achieved in three simple command lines:

    uv venv
    source .venv/bin/activate
    uv pip install --index https://test.pypi.org/simple/ --default-index https://pypi.org/simple/ langevin

_Note that before doing this you'll have to install `uv` on your machine._


### Alternative: by hand
Alternatively, you can employ the following two-step process.

1. Install Python $\geq$ 3.12, ideally in a Python environment; Python 3.14 is recommended, and current development uses this version. 

    The following packages are needed by `langevin` (`ffmpeg` is optional); they can be installed by hand at this point, or left to install automatically during the next step (by `pip`):
    
    - `numpy`
    - `jupyter`
    - `ipython`
    - `matplotlib`  
    - `pandas`
    - `tqdm`
    - `ffmpeg-python`

2. Install the [Python library `langevin`](https://pypi.org/project/langevin/) using `pip`, hopefully within a Python environment, from TestPyPI:

        pip install --index https://test.pypi.org/simple/ --default-index https://pypi.org/simple/ langevin

    Note: the `--index` argument ensures that any Python install
    dependencies are also sought in the true PyPI repository rather
    than in TestPyPI alone (which generally won't suffice). 

    _If you already have a pre-existing installation_ of this package, you may need to `upgrade` (update) to the latest version:

    
        pip install --index https://test.pypi.org/simple/ --default-index https://pypi.org/simple/ langevin --upgrade

## **Step 2:** Make a local copy of the demo scripts

Clone the [Langevin repo](https://github.com/cstarkjp/Langevin/tree/main) to your local machine:

        git clone https://github.com/cstarkjp/Langevin.git

which will create a `Langevin/` folder. 

If you already have a local copy of the repo, update it with `git pull`, making sure you are on the `main` branch (do `git checkout main`).