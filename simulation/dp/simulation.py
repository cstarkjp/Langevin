#!/usr/bin/env python3

from essentials import *

def main() -> None:
    sim_name: str = "a1p19050_b1_D0p04_η1_x250_y250_Δx1_Δt0p1"
    info_path: list[str] = [pardir, pardir, "experiments", sim_name]
    info: dict
    _, info = read_info(info_path, dplvn)

    sim = Simulation(
        name=sim_name, path=info_path, info=info, 
        do_snapshot_grid=False, do_verbose=True,
    )    
    sim.initialize()
    sim.analysis["n_epochs"]
    sim.run()
    sim.plot()
    sim.save(dplvn, do_verbose=True,)

if __name__ == "__main__":
    main()
