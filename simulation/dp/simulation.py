#!/usr/bin/env python3

from essentials import *

#  "a1p18855_b1_D0p04_η1_x62_y62_Δx1_Δt0p1"
#  "a1p18855_b1_D0p04_η1_x125_y125_Δx1_Δt0p1"
#  "a1p18855_b1_D0p04_η1_x250_y250_Δx1_Δt0p1"
#  "a1p18855_b1_D0p04_η1_x500_y500_Δx1_Δt0p1"
#  "a1p18855_b1_D0p04_η1_x1000_y1000_Δx1_Δt0p1"
#  "a1p18855_b1_D0p04_η1_x2000_y2000_Δx1_Δt0p1"

def main() -> None:
    sim_name: str = "a1p18855_b1_D0p04_η1_x31_y31_Δx1_Δt0p1"
    info_path: list[str] = [pardir, "experiments", sim_name]
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
