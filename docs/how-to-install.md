# How to install

## Best practice: use **uv**

Using `uv`, the creation of a virtual Python environment, installation of dependent packages, and installation of `langevin` itself is all straightforward.

First, install `uv`
following the [instructions here](https://docs.astral.sh/uv/getting-started/installation/).

Then, depending on your platform:

### macOS and Linux 

After creating and navigating into your Langevin work directory, execute the following in a terminal:

    uv venv --python=3.14
    source .venv/bin/activate
    uv pip install langevin

The first command creates a Python virtual environment in the current directory, forcing a choice of version 3.14. The second activates this virtual environment, ensuring that all subsequent references to Python, and all `pip` installs, etc., take place here only. The third command installs the `langevin` package along with all its dependencies. Note: if you want to generate animations using `ffmpeg-python`, which is one of these dependent packages, you will need to separately install `ffmpeg` itself on your system (this is not a Python thing).

### Windows

Installation on a Windows PC is similar to the macOS/Linux procedure, and involves only one extra step.
Start a PowerShell, create and navigate into a Langevin work folder, and execute:

    uv venv --python=3.14
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    .\.venv\Scripts\Activate.ps1
    uv pip install langevin

The extra command here ensures that PowerShell is allowed to run local scripts.


## Alternative: by hand (instructions for macOS/Linux only)
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