/**
 * @file langevin_integrate_euler.cpp
 * @brief Methods to carry out integration by explicit-Euler time-stepping.
 */ 

#include "langevin_types.hpp"
#include "langevin_base.hpp"

//! Perform explicit-Euler then stochastic integration steps, then update grid
void BaseLangevin::integrate_euler(rng_t& rng)
{
    mean_density = 0.0;
    for (auto i=0; i<n_cells; i++)
    {
        double f = ddensitydt_nonlinear(i, density_grid);
        density_plusk1_grid[i] = density_grid[i] + f*dt;
        poisson_sampler = poisson_dist_t(lambda_scaled * density_plusk1_grid[i]);
        gamma_sampler = gamma_dist_t(poisson_sampler(rng), 1/lambda);
        density_plusk1_grid[i]= gamma_sampler(rng);
        mean_density += density_plusk1_grid[i];
    }    
    mean_density /= static_cast<double>(n_cells);   
    // Update density field grid with result of integration
    density_grid.swap(density_plusk1_grid); 
}