# How to run

![](https://raw.githubusercontent.com/cstarkjp/Langevin/main/images/ρ_a1p18950_b1_D0p04_η1_x100_y50_Δx1_Δt0p1_rs1.gif
 "Density field evolution over time")

1. Navigate to [`Langevin/simulation/dp/`](https://github.com/cstarkjp/Langevin/tree/main/simulation/dp). There you'll find Jupyter notebooks and Python scripts to run DP-type Langevin simulations.

2. Don't run the noteboooks _in-situ_: their output will be written to [`Langevin/experiments/`](https://github.com/cstarkjp/Langevin/tree/main/experiments) which will generate `git` conflicts. 

    Instead, make your own folder elsewhere (e.g., `MyDPLangevin/` ), outside of the cloned `langevin.dp` file hierarchy, and copy [`Langevin/simulation/`](https://github.com/cstarkjp/Langevin/tree/main/simulation) into it.

3. Do the same for the folder [`Langevin/experiments/`](https://github.com/cstarkjp/Langevin/tree/main/experiments), copying it into e.g. `MyDPLangevin/`. 

    The [`Langevin/experiments/`](https://github.com/cstarkjp/Langevin/tree/main/experiments) folder has subfolders containing `Info.json` files, each named to refer logically to the model being run; these JSON files are used to drive the Langevin model simulations. 

4. Navigate to your `MyDPLangevin/simulation/` folder and run e.g. [`Simulation.ipynb`](dp-Simulation-ipynb-reference.md). With this notebook, you can carry out a single integration of the DP Langevin equation. 

    Depending on the name assigned to `sim_name` in this notebook (which specifies a model subfolder in `experiments/`), the appropriate `Info.json` file is parsed for model parameters, a single Langevin integration is performed, and output data files are written to that `experiments/` subfolder.

    For example, if `sim_name = a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1`, the `Info.json` file in `experiments/a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1/` is used to drive the simulation, and output files are written to this folder.