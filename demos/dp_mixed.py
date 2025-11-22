#!/usr/bin/env python3

"""!
@file dp_mixed.py
@brief Demo 2d DP Langevin simulation with mixed grid topology and boundary conditions.
"""

# import sys, os
# sys.path.insert(0, os.path.join(os.path.pardir, "build"))
import numpy as np
from numpy.typing import NDArray
from langevin.dp import dplvn # type: ignore

def main() -> None:
    bold = lambda str: ("\033[1m" + str + "\033[0m")

    print()
    print(bold(f"dplvn version:  {dplvn.__version__}"))
    print()

    sim = dplvn.SimDP(
        linear=1.0, quadratic=2.0, diffusion=0.1, noise=1.0, 
        t_final=30.0-1e-10, 
        # t_final=300.0-1e-8, 
        dx=0.5, dt=0.01,
        random_seed=2,
        grid_dimension=dplvn.D2,
        grid_size=(12,8,),
        # grid_size=(100,60,),
        grid_topologies=(dplvn.BOUNDED, dplvn.PERIODIC,),
        # boundary_condition=dplvn.FLOATING,
        boundary_conditions=(
            # dplvn.FLOATING, dplvn.FLOATING, dplvn.FLOATING, dplvn.FLOATING,
            # dplvn.FIXED_VALUE, dplvn.FIXED_VALUE, dplvn.FLOATING, dplvn.FLOATING,
            dplvn.FIXED_FLUX, dplvn.FIXED_FLUX, dplvn.FLOATING, dplvn.FLOATING,
        ),
        # bc_values=(-0, +2, 0, 0,),
        bc_values=(-1e+1, +1e+1, 0, 0,),
        initial_condition=dplvn.RANDOM_UNIFORM,
        ic_values=(0, 1,),
        integration_method=dplvn.RUNGE_KUTTA,
        do_snapshot_grid=True,
        do_verbose=True,
    )

    if not sim.initialize(5):
        raise Exception("Failed to initialize sim")
    n_epochs: int = sim.get_n_epochs()
    print()
    print(f"Number of sim epochs = {n_epochs}")
    print()

    n_segments: int = 5
    n_segment_epochs: int = (n_epochs-1) // n_segments
    if (n_segment_epochs*n_segments+1)!=n_epochs:
        raise Exception(
            f"Failed to segment sim with {n_epochs} epochs "
            + "into {n_segments} segment(s)"
        )

    print(bold(f"Integrating:  {n_epochs} epochs in {n_segments} segment(s)"))
    print()

    density_dict: dict[float, NDArray] = {}
    for i_segment in range(0, n_segments+1, 1):
        if i_segment>0 and not sim.run(n_segment_epochs):
            raise Exception("Failed to run sim")
        if not sim.postprocess():
            raise Exception("Failed to process sim results")
        i_epoch = sim.get_i_current_epoch()
        t_epoch = np.round(sim.get_t_current_epoch())
        density_dict[t_epoch] = sim.get_density()
        print(bold(
            f"segment={i_segment}/{n_segments}  "
            + f"i={i_epoch} t={t_epoch}"
        ))
        # print(f"t epochs:  {sim.get_t_epochs()}")
        # print(f"mean densities:  {sim.get_mean_densities()}")
        print("cell density grid:")
        print(np.round(density_dict[t_epoch].T, 2))
        print(flush=True)

if __name__ == "__main__":
    main()