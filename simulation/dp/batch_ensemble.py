#!/usr/bin/env python3

from essentials import *

def report_computation_times(ensemble: Ensemble) -> None:
    print("Computation times:")
    sim_: Simulation
    for sim_ in ensemble.sim_list:
        print(f"{sim_.misc["name"]}: {sim_.misc["computation_time"]}")

def main() -> None:
    a_critical: str =  "ensemble_ac1p18857"
    sizes: Sequence[int] = (
        # 2000, 1000, 500, 250, 125,
        62, 31,  
    )
    ensemble_name_list: list[str] = [
        f"b1_D0p04_η1_x{size_}_y{size_}_Δx1_Δt0p1"
        for size_ in sizes
    ]

    do_verbose: bool = False
    ensemble_name_: str
    for ensemble_name_ in ensemble_name_list:
        print(f"Executing: {a_critical}/{ensemble_name_}")
        info_path_: list[str] = [
            pardir, pardir, "experiments", a_critical, ensemble_name_
        ]
        ensemble_: Ensemble = Ensemble(info_path_, do_verbose,)
        ensemble_.create()
        ensemble_.exec()
        report_computation_times(ensemble_)
        ensemble_.multi_plot()
        ensemble_.plot()
        ensemble_.save(dplvn)

if __name__ == "__main__":
    main()