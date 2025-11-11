# How to run


## Setting up

1. If you haven't done this already, clone or download/unzip the project repository from GitHub:

        git clone https://github.com/cstarkjp/Langevin.git

    This will create a folder called `Langevin/`.
    We are going to use its subfolders `tests/`, `simulations/`, and `experiments/`.

1. Elsewhere, out of this folder hierarchy, create your own "work" folder. Let's say you call it `MyDPLangevin/`. Copy the three subfolders into it. Your folder should now look like this:

    ![](images/how_to_run1.jpg)

1. _Optional, but strongly advised:_ create a Python environment for work in this folder.
If you're using `uv`, all you need to do here is:

        uv venv
        source .venv/bin/activate

    Then install the `langevin` package as explained on the [How to install](how-to-install.md) page, ideally using `uv`

        uv pip install langevin

    Now you have a _local_ Python environment for work with the `langevin` package.
    Remember to always first `source .venv/bin/activate` from the command line when
    working here.

If you choose not to set up a virtual environment, you will need to install the `langevin` package in the usual way for your default Python. 

## Test scripts

<!-- ![](https://raw.githubusercontent.com/cstarkjp/Langevin/main/images/ρ_a1p18950_b1_D0p04_η1_x100_y50_Δx1_Δt0p1_rs1.gif
 "Density field evolution over time") -->

Navigate to the `tests/` folder. Run the demo scripts there as explained on the [Tests page](tests-reference.md).

## Full simulations

### Organization

Navigate to the `simulation/dp/` folder. There you'll find Jupyter notebooks and Python scripts to run more substantial DP-type Langevin simulations:

![](images/how_to_run5.jpg)

These notebooks and scripts can be run using `ipython` and `python` respectively (`ipython` can run both). The notebooks can also be run in `jupyter`.

Now take a look at your copy of the `experiments/` folder. It should look something like this:

![](images/how_to_run2.jpg)

Simulations work with `Info.json` parameters files in correspondingly named folders, and write their results into subfolders within them. Further explanation is provided below. The naming convention is a bit awkward, but it's tough to come up with a perfect solution to organizing simulations with myriad coefficients and model variables. This is what we have.


### Running a simulation for fixed grid size

Consider the notebook [`Simulation.ipynb`](dp-Simulation-ipynb-reference.md), which runs a job entitled `a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1`. 

This cumbersome name is a concatenation of the key DP model parameters employed in this particular simulation. 
It corresponds to a subfolder in `experiments/` called `a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1/`. 

_This subfolder is used both for model parameter input ***and*** for results output._

Look in this subfolder of `experiments/` for `Info.json`: this JSON file contains all the parameters used by the notebook to run a single integration of the DP Langevin equation on a 2D grid with the model coefficients reflected in the job name.

Run the simulation:

        ipython Simulation.ipynb

and you should see text output in your terminal reporting integration of a 2D Langevin equation — on a small grid
with periodic boundary topology in the $x$ direction and "free" edges
in the $y$ direction.

It should write output files to the `experiments/a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1/` folder like this:

![](images/how_to_run3.jpg)

All the output files are written to a subfolder `rs1/`, which corresponds to the random seed (of value one) chosen for this particular simulation. If you want to run different realizations for different random number seeds, change the `Info.json` file as appropriate.

Looking at each of the output files in turn:

   - `Outfo.json`  = a copy of `Info.json` extended with results data and model run information
   - `ρ_t.npz` = a compressed `numpy`-format data file containing a collection of model results arrays; these may include
     - a tuple of the simulation time "epochs"
     - a tuple of the grid-averaged "mean density" of the order parameter field at each of these epochs
     - a set of "segment" time slices of the order-parameter density grid $\rho(\mathbf{x},t)$ (if this option is chosen in the `Info.json` file; by default here it is not)
   - `ρ_t_loglog.png` = a graph of mean density over time 
   - `ρ_t_rescaled.png` = a DP-model rescaled version of this graph

_In summary: if you want to run single-grid simulations, with a single set of Langevin coefficients and model parameters, use this notebook as your template._

### Running an ensemble of simulations for fixed grid size

If instead you want to run an ensemble of simulations for a _range_ of Langevin equation coefficients, look at [`EnsembleSimulation.ipynb`](dp-EnsembleSimulation-ipynb-reference.md).

        ipython EnsembleSimulation.ipynb

This will run a set of simulations for different size grids:

TBD...

### Running a batch of ensemble simulations for several grid sizes

For substantial ensemble simulations in which the grid size is varied as well as the model coefficients, a batch Python script is provided. 
This script hard-codes some parameter choices, loops across a set of grid sizes, and constructs a list of ensemble job names from a tuple of grid size choices. These names must correspond to a "root" folder and a set of subfolders:

![](images/how_to_run6.jpg)

It then executes each ensemble job in turn:

![](images/how_to_run9.jpg)


For this example batch script, the batch root folder (in `experiments/`) is assumed to be named `ac1p18857`, corresponding to the known critical value $a_c$  (from previous simulations) of the DP Langevin parameter $a$; its subfolders follow the pattern `b1_D0p04_η1_x{size_}_y{size_}_Δx1_Δt0p1`, i.e. the other DP Langevin parameters are $b=1$, $D=0.04$, and $\eta=1$, for grid spacing $\Delta{x}=1$ and time step $\Delta{t}=0.1$. There must be `Info.json` files in each of these subfolders with model parameters to match:

![](images/how_to_run7.jpg)

Run the batch job using either `ipython` or `python`:

        python batch_ensemble.py

In your terminal, you should see summary reports of each ensemble of simulations, two sets of 15 in total, including the name of each simulation job and its computation time.
Each set of 15 jobs would have been executed in parallel processes spawned by Python's `multiprocessing` tool.

The directory tree for this run should now look like this:

![](images/how_to_run8.jpg)

where you can see that each set of results files has been placed in parallel with the corresponding `Info.json` file for that grid size. The `combo_ρ_t.npz` file in each case is the compressed `numpy` data file containing a single `t_epochs.npy` array and a tuple of `mean_densities.npy` arrays, one for each value of Langevin parameter $a$ used in the ensemble of simulations. The `Outfo.json` file records this set of $a$ values and all the other model variable choices for each simulation.

To run for a wider range of grid sizes, simply modify the list in `batch_ensemble.py`; if you want to choose different sizes, or different model parameters, you will have to modify the whole `ac1p18857/` folder hierarchy, its subfolder names, and the constituent `Info.json1` files to match. This is a bit ungainly, but it keeps the organization of simulations coherent.









