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
        double f = nonlinear_rhs(i, density_grid);
        aux_grid1[i] = density_grid[i] + f*dt;
        poisson_sampler = poisson_dist_t(lambda_on_explcdt * aux_grid1[i]);
        gamma_sampler = gamma_dist_t(poisson_sampler(rng), 1/lambda);
        aux_grid1[i]= gamma_sampler(rng);
        mean_density += aux_grid1[i];
    }    
    mean_density /= static_cast<double>(n_cells);   
    // Update density field grid with result of integration
    density_grid.swap(aux_grid1); 
}