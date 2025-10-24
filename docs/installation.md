# How to install

1. Install Python $\geq$ 3.12 and the following packages, ideally in a Python environment:
    - `numpy`
    - `jupyter`
    - `ipython`
    - `matplotlib`  
    - `pandas`
    - `tqdm`
    - `ffmpeg-python`

2. Install the [Python library `lvn`](https://test.pypi.org/project/lvn/) using `pip`, hopefully within a Python environment, from TestPyPI:

        pip install -i https://test.pypi.org/simple/ lvn

    _If you already have a pre-existing installation_ of this package, you may need to `upgrade` (update) to the latest version:

        pip install -i https://test.pypi.org/simple/ lvn --upgrade

3. Clone the [`lvn.dp` repo](https://github.com/cstarkjp/Langevin/tree/main) to your local machine:

        git clone https://github.com/cstarkjp/Langevin.git

    which will create a `Langevin/` folder. 

    If you already have a local copy of the repo, update it with `git pull`, making sure you are on the `main` branch (do `git checkout main`).
