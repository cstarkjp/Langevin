/**
 * @file langevin_base.hpp
 * @brief Base class for Langevin equation integrator.
 */

#ifndef BASE_HPP
#define BASE_HPP

#include "langevin_coefficients.hpp"
#include "langevin_parameters.hpp"

/**
 * @brief Base class for Langevin equation integrator.
 */
class BaseLangevin
{
protected:
    //! Total number of cells in n-D grid
    int n_cells;
    //! Density field grid
    grid_t density_grid;
     //! Neighorhood topology for all grid cells
    grid_wiring_t grid_wiring;
   
    //! Time step, i.e, epoch-to-epoch Δt
    double dt;
    //! Grid spacing, i.e., spacing Δx between cell centers in all directions
    double dx;
    //! Grid-average of density field
    double mean_density;

    //! Function generating Poisson variates
    poisson_dist_t poisson_sampler;
    //! Function generating gamma variates
    gamma_dist_t gamma_sampler;
    //! Function generating normal variates
    gaussian_dist_t gaussian_sampler;

    //! Dornic method coefficient
    double linear_coefficient;
    //! Dornic method coefficient
    double noise_coefficient;
    //! Dornic method stochastic-step variable
    double lambda;
    //! Dornic method stochastic-step variable
    double lambda_on_explcdt;

    //! Runge-Kutta variable grid #1
    grid_t k1_grid;
    //! Runge-Kutta variable grid #2
    grid_t k2_grid;
    //! Runge-Kutta variable grid #3
    grid_t k3_grid;
    //! Temporary density grid used to perform an integration step
    grid_t aux_grid1;
    //! Temporary density grid used to perform an integration step
    grid_t aux_grid2;

public:
    //! Default constructor
    BaseLangevin() = default;
    //! Construct Langevin density field grid of appropriate n-D dimension
    bool construct_grid(const Parameters parameters);
    //! Build 1d Langevin density field grid & topology
    bool construct_1D_grid(const Parameters parameters);
    //! Build 2d Langevin density field grid & mixed topology
    bool construct_2D_grid(const Parameters parameters);
    //! Initial condition for density field: uniformly random
    bool initialize_grid(const Parameters parameters, rng_t& rng);
    //! Set initial condition of Langevin density field grid
    void prepare(const Coefficients& coefficients);
    //! Check we have 2N boundary conditions for an N-dimensional grid
    bool check_boundary_conditions(const Parameters parameters);
    //! Set density field values only the grid edges per bc specs
    void apply_boundary_conditions(const Parameters parameters, int i_epoch);
    //! Runge-Kutta + stochastic integration + grid update
    void integrate_rungekutta(rng_t& rng);
    //! Explicit Euler + stochastic integration + grid update
    void integrate_euler(rng_t& rng);
    double get_density_grid_value(const int) const;
    //! Expose mean density
    double get_mean_density() const;
    //! Compute Poisson RNG mean
    double get_poisson_mean() const;

    //! Method to set nonlinear coefficients for deterministic integration step: to be defined by application
    virtual void set_nonlinear_coefficients(const Coefficients& coefficients) {};
    //! Method to set nonlinear RHS of Langevin equation for deterministic integration step: to be defined by application
    virtual double nonlinear_rhs(const int i_cell, const grid_t& field) const 
        { return 0; };
};

#endif