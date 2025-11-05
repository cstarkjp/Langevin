/**
 * @file langevin_integrate_rungekutta.cpp
 * @brief Methods to carry out 4th-order Runge-Kutta integration.
 */

#include "langevin_types.hpp"
#include "langevin_base.hpp"

//! Runge-Kutta integration of the nonlinear and diffusion terms 
//! in the Langevin equation.
//! Update of cells is done in the same loop as last Runge-Kutta step 
//! for efficiency.
void BaseLangevin::integrate_rungekutta(rng_t& rng)
{
    auto step1 = [&](grid_t& aux_grid, grid_t& k1_grid, const double dtf)
    {
        for (auto i=0; i<n_cells; i++)
        {
            k1_grid[i] = nonlinear_rhs(i, density_grid);
            aux_grid[i] = density_grid[i] + k1_grid[i]*dtf;
        }
    };
    auto step2or3 = [&](
        const grid_t& aux_grid_in, grid_t& aux_grid_out, grid_t& k23_grid, 
        const double dtf)
    {
        for (auto i=0; i<n_cells; i++)
        {
            k23_grid[i] = nonlinear_rhs(i, aux_grid_in);
            aux_grid_out[i] = density_grid[i] + k23_grid[i]*dtf;
        }
    };
    auto step4 = [&](
        const grid_t& aux_grid, const grid_t& k1_grid, const grid_t& k2_grid, 
        const grid_t& k3_grid, rng_t& rng, const double dtf)
    {
        mean_density = 0.0;
        for (auto i=0; i<n_cells; i++)
        {
            // Runge-Kutta 4th step
            auto k4 = nonlinear_rhs(i, aux_grid);
            density_grid[i] += (k1_grid[i] + 2*(k2_grid[i]+k3_grid[i]) +k4)*dtf;
            // Stochastic step
            poisson_sampler = poisson_dist_t(lambda_on_explcdt*density_grid[i]);
            gamma_sampler = gamma_dist_t(poisson_sampler(rng), 1/lambda);
            density_grid[i] = gamma_sampler(rng);
            // Incrementally compute mean density
            mean_density += density_grid[i];
        }    
        mean_density /= static_cast<double>(n_cells);    
    };

    step1(aux_grid1, k1_grid, dt/2);
    step2or3(aux_grid1, aux_grid2, k2_grid, dt/2);
    step2or3(aux_grid2, aux_grid1, k3_grid, dt);
    step4(aux_grid1, k1_grid, k2_grid, k3_grid, rng, dt/6);
}