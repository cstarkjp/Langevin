/**
 * @file langevin_integrate_rungekutta.cpp
 * @brief Methods to carry out 4th-order Runge-Kutta integration.
 */

#include "langevin_types.hpp"
#include "langevin_base.hpp"

//! 4th-order Runge-Kutta integration of the nonlinear and diffusion terms
//! of the Langevin equation dρ/dt = linear + nonlinear + diffusion + noise.

// Parallelizing this is going to be complicated by the fact that each
// call to ddensitydt_nonlinear() entails reference to the neighboring cells
// of density_grid[i], which gets fiddly at the grid boundaries.
// Don't know how all this will map onto a GPU treatment.
// Maybe I'll need to implement a get_neighboring_cells().
void BaseLangevin::integrate_rungekutta(rng_t& rng)
{
    int i;
    // Runge-Kutta 1st step
    for (i=0; i<n_cells; i++)
    {
        // k1 = dρ/dt at start-interval t
        k1_grid[i] = ddensitydt_nonlinear(i, density_grid)*dt;
        density_plusk1_grid[i] = density_grid[i] + k1_grid[i]/2;
    }
    // Runge-Kutta 2nd step
    for (i=0; i<n_cells; i++)
    {
        // k2 = dρ/dt at mid-interval t+Δt/2 using k1
        k2_grid[i] = ddensitydt_nonlinear(i, density_plusk1_grid)*dt;
        density_plusk2_grid[i] = density_grid[i] + k2_grid[i]/2;
    }
    // Runge-Kutta 3rd step
    for (i=0; i<n_cells; i++)
    {
        // k3 = dρ/dt at mid-interval t+Δt/2 using k2
        k3_grid[i] = ddensitydt_nonlinear(i, density_plusk2_grid)*dt;
        density_plusk3_grid[i] = density_grid[i] + k3_grid[i];
    }
    // Runge-Kutta 4th step    
    for (i=0; i<n_cells; i++)
    {
        // k4 = dρ/dt at end-interval t+Δt using k3
        k4_grid[i] = ddensitydt_nonlinear(i, density_plusk3_grid)*dt;
        // Estimate for ρ(t+Δt) = ρ(t) + (k1 + 2*k2 + 2*k3 + k4)/6
        density_grid[i] += (k1_grid[i]+2*(k2_grid[i]+k3_grid[i])+k4_grid[i])/6;
    }  
    // Stochastic step - strictly local to each i.
    // This step combines the linear and noise terms in the Langevin equation.
    mean_density = 0.0;
    for (i=0; i<n_cells; i++)
    {
        // Generate a random sample from the FPE-derived noise PDF
        // whose form is a kind of modified Bessel function,
        // which is also a Poisson-randomized gamma distribution.
        // Do so by sampling: (1) a Poisson variate; (2) a gamma variate
        // whose shape parameter is that Poisson sample (an integer).
        poisson_sampler = poisson_dist_t(lambda_scaled*density_grid[i]);
        gamma_sampler = gamma_dist_t(poisson_sampler(rng), 1/lambda);
        // Update density value at this grid location i
        density_grid[i] = gamma_sampler(rng);
        // Incrementally compute mean density
        mean_density += density_grid[i];
    }    
    mean_density /= static_cast<double>(n_cells);    
}

// //! Runge-Kutta integration of the nonlinear and diffusion terms 
// //! in the Langevin equation.
// //! Update of cells is done in the same loop as last Runge-Kutta step 
// //! for efficiency.
// void BaseLangevin::integrate_rungekutta_revised(rng_t& rng)
// {
//     // step1(rho_grid_aux1, k1_grid, dt/2);
//     for (auto i=0; i<n_cells; i++)
//     {
//         k1_grid[i] = ddensitydt_nonlinear(i, density_grid);
//         rho_grid_aux1[i] = density_grid[i] + k1_grid[i]*dt/2;
//     }

//     // step2or3(rho_grid_aux1, rho_grid_aux2, k2_grid, dt/2);
//     for (auto i=0; i<n_cells; i++)
//     {
//         k2_grid[i] = ddensitydt_nonlinear(i, rho_grid_aux1);
//         rho_grid_aux2[i] = density_grid[i] + k2_grid[i]*dt/2;
//     }

//     // step2or3(rho_grid_aux2, rho_grid_aux1, k3_grid, dt);
//     for (auto i=0; i<n_cells; i++)
//     {
//         k3_grid[i] = ddensitydt_nonlinear(i, rho_grid_aux2);
//         rho_grid_aux3[i] = density_grid[i] + k3_grid[i]*dt;
//     }

//     // step4(rho_grid_aux1, k1_grid, k2_grid, k3_grid, rng, dt/6);
//     mean_density = 0.0;
//     for (auto i=0; i<n_cells; i++)
//     {
//         // Runge-Kutta 4th step
//         auto k4 = ddensitydt_nonlinear(i, rho_grid_aux3);
//         density_grid[i] += (k1_grid[i]+2*(k2_grid[i]+k3_grid[i])+k4)*dt/6;
//         // Stochastic step
//         poisson_sampler = poisson_dist_t(lambda_scaled*density_grid[i]);
//         gamma_sampler = gamma_dist_t(poisson_sampler(rng), 1/lambda);
//         density_grid[i] = gamma_sampler(rng);
//         // Incrementally compute mean density
//         mean_density += density_grid[i];
//     }    
//     mean_density /= static_cast<double>(n_cells);    
// }

// //! Runge-Kutta integration of the nonlinear and diffusion terms 
// //! in the Langevin equation.
// //! Update of cells is done in the same loop as last Runge-Kutta step 
// //! for efficiency.
// void BaseLangevin::integrate_rungekutta_old(rng_t& rng)
// {
//     auto step1 = [&](grid_t& aux_grid, grid_t& k1_grid, const double dtf)
//     {
//         for (auto i=0; i<n_cells; i++)
//         {
//             k1_grid[i] = ddensitydt_nonlinear(i, density_grid);
//             aux_grid[i] = density_grid[i] + k1_grid[i]*dtf;
//         }
//     };
//     auto step2or3 = [&](
//         const grid_t& aux_grid_in, grid_t& aux_grid_out, grid_t& k23_grid, 
//         const double dtf)
//     {
//         for (auto i=0; i<n_cells; i++)
//         {
//             k23_grid[i] = ddensitydt_nonlinear(i, aux_grid_in);
//             aux_grid_out[i] = density_grid[i] + k23_grid[i]*dtf;
//         }
//     };
//     auto step4 = [&](
//         const grid_t& aux_grid, const grid_t& k1_grid, const grid_t& k2_grid, 
//         const grid_t& k3_grid, rng_t& rng, const double dtf)
//     {
//         mean_density = 0.0;
//         for (auto i=0; i<n_cells; i++)
//         {
//             // Runge-Kutta 4th step
//             auto k4 = ddensitydt_nonlinear(i, aux_grid);
//             density_grid[i] += (k1_grid[i]+2*(k2_grid[i]+k3_grid[i])+k4)*dtf;
//             // Stochastic step
//             poisson_sampler = poisson_dist_t(lambda_scaled*density_grid[i]);
//             gamma_sampler = gamma_dist_t(poisson_sampler(rng), 1/lambda);
//             density_grid[i] = gamma_sampler(rng);
//             // Incrementally compute mean density
//             mean_density += density_grid[i];
//         }    
//         mean_density /= static_cast<double>(n_cells);    
//     };

//     step1(aux_grid1, k1_grid, dt/2);
//     step2or3(aux_grid1, aux_grid2, k2_grid, dt/2);
//     step2or3(aux_grid2, aux_grid1, k3_grid, dt);
//     step4(aux_grid1, k1_grid, k2_grid, k3_grid, rng, dt/6);
// }