
"""!
@file test_simdp_run.py
@brief Unit test SimDP execution.
"""

import unittest
import numpy as np
from numpy.typing import NDArray
from langevin.dp import dplvn # type: ignore

def instantiate_sim_specific() -> dplvn.SimDP:
    return dplvn.SimDP(
        linear=1.1895, quadratic=1.0, diffusion=0.04, noise=1.0, 
        t_final=3, 
        dx=1, dt=0.1,
        random_seed=1,
        grid_dimension=dplvn.D2,
        grid_size=(10, 5,),
    )

def run_simdp(
        sim: dplvn.SimDP, n_segments: int, n_segment_epochs: int,
    ) -> bool:
    was_success: bool = True
    for i_segment in range(0, n_segments+1, 1):
        if i_segment>0:
            was_success &= sim.run(n_segment_epochs)
    return was_success

def run_and_postprocess_simdp(
        sim: dplvn.SimDP, n_segments: int, n_segment_epochs: int,
    ) -> tuple[bool, list, list]:
    i_epochs: NDArray = list(np.zeros(n_segments+1))
    t_epochs: NDArray = list(np.zeros(n_segments+1))
    was_success: bool = True
    for i_segment in range(0, n_segments+1, 1):
        if i_segment>0 and not sim.run(n_segment_epochs):
            raise Exception("Failed to run sim")
        was_success &= sim.postprocess()
        i_epochs[i_segment] = int(sim.get_i_current_epoch())
        t_epoch_ = sim.get_t_current_epoch()
        t_epochs[i_segment] = (
            float(np.round(t_epoch_, 5)) if np.abs(t_epoch_)>1e-15
            else 0
        )
        print(i_segment, t_epoch_, float(np.round(t_epoch_, 5)), t_epochs[i_segment])
    return (was_success, i_epochs, t_epochs,)


class TestRunSimDP(unittest.TestCase):

    def test_run_simdp(self):
        sim = instantiate_sim_specific()
        sim.initialize(15)
        n_epochs: int = sim.get_n_epochs()
        n_segments: int = 5
        n_segment_epochs: int = (n_epochs-1) // n_segments
        result = run_simdp(sim, n_segments, n_segment_epochs,)
        self.assertTrue(result)

    def test_run_and_postprocess_simdp(self):
        sim = instantiate_sim_specific()
        sim.initialize(15)
        n_epochs: int = sim.get_n_epochs()
        n_segments: int = 5
        n_segment_epochs: int = (n_epochs-1) // n_segments
        (was_success, i_epochs, t_epochs,) \
            = run_and_postprocess_simdp(sim, n_segments, n_segment_epochs,)
        self.assertTrue(was_success)
        t_epochs[0] = 0
        self.assertEqual(i_epochs, [0, 6, 12, 18, 24, 30])
        print(f"Comparing:  {t_epochs[1:]} {[0.6, 1.2, 1.8, 2.4, 3.0]}")
        self.assertEqual(t_epochs[1:], [0.6, 1.2, 1.8, 2.4, 3.0])

if __name__ == '__main__':
    unittest.main()