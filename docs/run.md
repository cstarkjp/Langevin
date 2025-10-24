# How to run

1. Navigate to [`Langevin/Simulation/`](https://github.com/cstarkjp/Langevin/tree/main/simulation). There you'll find Jupyter notebooks and Python scripts to run Langevin simulations.

2. Don't run the noteboooks _in-situ_: their output will be written to [`Langevin/experiments/`](https://github.com/cstarkjp/Langevin/tree/main/experiments) which will generate `git` conflicts. 

    Instead, make your own folder elsewhere (e.g., `MyGL/` ), outside of the cloned `lvn.dp` file hierarchy, and copy [`Langevin/Simulation/`](https://github.com/cstarkjp/Langevin/tree/main/simulation) into it.

3. Do the same for the folder [`Langevin/experiments/`](https://github.com/cstarkjp/Langevin/tree/main/experiments), copying it into e.g. `MyGL/`. 

    The [`Langevin/experiments/`](https://github.com/cstarkjp/Langevin/tree/main/experiments) folder has subfolders containing `Info.json` files, each named to refer logically to the model being run; these JSON files are used to drive the Langevin model simulations. 

4. Navigate to your `MyGL/Simulation/` folder and run e.g. [`DPSimulation.ipynb`](DPSimulation-ipynb-reference.md). With this notebook, you can carry out a single integration of the DP Langevin equation. 

    Depending on the name assigned to `sim_name` in this notebook (which specifies a model subfolder in `experiments/`), the appropriate `Info.json` file is parsed for model parameters, a single Langevin integration is performed, and output data files are written to that `experiments/` subfolder.

    For example, if `sim_name = a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1`, the `Info.json` file in `experiments/a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1/` is used to drive the simulation, and output files are written to this folder.