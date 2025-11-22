
"""!
@file test_simdp_basics.py
@brief Unit test SimDP instantiation and set up.
"""

import unittest
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

class TestCreateSimDP(unittest.TestCase):

    def test_instantiate_sim_defaults(self):
        sim = instantiate_sim_defaults()
        self.assertTrue(type(sim), dplvn.SimDP)

    def test_instantiate_sim_specifics(self):
        sim = instantiate_sim_specific()
        self.assertTrue(type(sim), dplvn.SimDP)

    def test_initialize_sim(self):
        sim = instantiate_sim_specific()
        self.assertTrue(sim.initialize(5))

    def test_count_epochs_round5(self):
        sim = instantiate_sim_specific()
        _ = sim.initialize(5)
        n_epochs: int = sim.get_n_epochs()
        n_segments: int = 5
        n_segment_epochs: int = (n_epochs-1) // n_segments
        self.assertEqual((n_segment_epochs*n_segments+1), n_epochs)

    # def test_count_epochs_round15(self):
    #     sim = instantiate_sim_specific()
    #     _ = sim.initialize(5)
    #     sim.initialize(15)
    #     n_epochs: int = sim.get_n_epochs()
    #     n_segments: int = 5
    #     n_segment_epochs: int = (n_epochs-1) // n_segments
    #     self.assertEqual((n_segment_epochs*n_segments+1), n_epochs)

if __name__ == '__main__':
    unittest.main()