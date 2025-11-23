
"""!
@file test_simdp_basics.py
@brief Unit test SimDP instantiation and set up.
"""

import unittest
import os
import sys
# dp_dir = os.path.abspath("C:\\hostedtoolcache\\windows\\Python\\3.14.0\\x64\\Lib\\site-packages\\langevin\\dp")
# if sys.platform == "win32" and os.path.exists(dp_dir):
#     os.add_dll_directory(dp_dir)
#     sys.path.insert(0, dp_dir)
#     print
#     print(sys.path)
#     print
from langevin.dp import dplvn # type: ignore

def instantiate_sim_defaults() -> dplvn.SimDP:
    return dplvn.SimDP()

def instantiate_sim_specific() -> dplvn.SimDP:
    return dplvn.SimDP(
        linear=1.1895, quadratic=1.0, diffusion=0.04, noise=1.0, 
        t_final=3, 
        dx=1, dt=0.1,
        random_seed=1,
        grid_dimension=dplvn.D2,
        grid_size=(10, 5,),
    )

def instantiate_sim_verbose() -> dplvn.SimDP:
    return dplvn.SimDP(
        linear=1.1895, quadratic=1.0, diffusion=0.04, noise=1.0, 
        t_final=3, 
        dx=1, dt=0.1,
        random_seed=1,
        grid_dimension=dplvn.D2,
        grid_size=(10, 5,),
        do_verbose=True,
    )

class TestCreateSimDP(unittest.TestCase):

    def test_instantiate_sim_defaults(self):
        sim = instantiate_sim_defaults()
        self.assertIsInstance(sim, dplvn.SimDP)

    def test_instantiate_sim_specifics(self):
        sim = instantiate_sim_specific()
        self.assertIsInstance(sim, dplvn.SimDP)

    def test_initialize_sim(self):
        sim = instantiate_sim_specific()
        self.assertTrue(sim.initialize(5))

    def test_count_epochs_round5(self):
        sim = instantiate_sim_verbose()
        _ = sim.initialize(5)
        n_epochs: int = sim.get_n_epochs()
        n_segments: int = 5
        n_segment_epochs: int = (n_epochs-1) // n_segments
        self.assertEqual((n_segment_epochs*n_segments+1), n_epochs)

if __name__ == '__main__':
    unittest.main()