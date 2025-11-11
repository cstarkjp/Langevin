#!/usr/bin/env python3

from essentials import *

#  "b1_D0p04_η1_x62_y62_Δx1_Δt0p1"
#  "b1_D0p04_η1_x125_y125_Δx1_Δt0p1"
#  "b1_D0p04_η1_x250_y250_Δx1_Δt0p1"
#  "b1_D0p04_η1_x500_y500_Δx1_Δt0p1"
#  "b1_D0p04_η1_x1000_y1000_Δx1_Δt0p1"
#  "b1_D0p04_η1_x2000_y2000_Δx1_Δt0p1"

def main() -> None:
    a_critical = "ac1p18857"
    ensemble_name = "b1_D0p04_η1_x31_y31_Δx1_Δt0p1"
    info_path: list[str] = [pardir, "experiments", a_critical, ensemble_name]
    do_verbose: bool = True
    
    ensemble = Ensemble(info_path, do_verbose,)
    ensemble.info["Misc"]
    ensemble.create()
    ensemble.exec()
    print("Computation times:")
    for sim_ in ensemble.sim_list:
        print(f"{sim_.misc["name"]}: {sim_.misc["computation_time"]}")
    ensemble.multi_plot()
    ensemble.plot()
    ensemble.save(dplvn, do_dummy=False)

if __name__ == "__main__":
    main()
