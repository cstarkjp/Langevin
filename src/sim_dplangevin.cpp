/**
 * @file sim_dplangevin.cpp
 * @brief Constructor for class that manages simulation of DP Langevin equations.
 */ 

#include "sim_dplangevin.hpp"

/**
 * @details Constructor for class that manages simulation of DP Langevin equations.
 */
 SimDP::SimDP(
    const double linear, const double quadratic,
    const double diffusion, const double noise, 
    const double t_final, 
    const double dx, const double dt, 
    const int random_seed,
    const GridDimension grid_dimension,
    const int_vec_t grid_size,
    const gt_vec_t grid_topologies,
    const bc_vec_t boundary_conditions,
    const dbl_vec_t bc_values,
    const InitialCondition initial_condition,
    const dbl_vec_t ic_values,
    const IntegrationMethod integration_method,
    const bool do_verbose
) : coefficients(linear, quadratic, diffusion, noise),
    p(
        t_final, 
        dx, 
        dt, 
        random_seed,
        grid_dimension, 
        grid_size, 
        grid_topologies,
        boundary_conditions,
        bc_values,
        initial_condition, 
        ic_values, 
        integration_method
    ),
    do_verbose(do_verbose)
{
    rng = new rng_t(p.random_seed); 
    dpLangevin = new DPLangevin(p);
    if (do_verbose) 
    {
        coefficients.print();
        p.print();
    }
}

//! Method to be called first to set up simulation: 
//! a grid is constructed; initial conditions are applied; 
//! the Langevin equation is prepared; the zeroth-epoch 
//! solution state is recorded (after applying boundary conditions).
bool SimDP::initialize(int n_decimals)
{
    if (not dpLangevin->construct_grid(p)) { 
        std::cout 
            << "SimDP::initialize failure: couldn't construct grid" 
            << std::endl;
        return false; 
    }
    if (not dpLangevin->initialize_grid(p, *rng)) { 
        std::cout 
            << "SimDP::initialize failure: couldn't initialize grid" 
            << std::endl;
        return false; 
    }
    dpLangevin->prepare(coefficients);
    this->n_decimals = n_decimals;
    n_epochs = count_epochs();
    t_epochs = dbl_vec_t(n_epochs, 0.0);
    mean_densities = dbl_vec_t(n_epochs, 0.0);
    // Treat epoch#0 as the initial grid state
    // So after initialization, we are nominally at epoch#1
    i_next_epoch = 1;
    t_next_epoch = p.dt;
    if (not choose_integrator())
    { 
        std::cout << "SimDP::initialize failure: unable to choose integrator" << std::endl;
        return false; 
    }        
    if (not dpLangevin->check_boundary_conditions(p))
    {
        std::cout << "SimDP::initialize failure: wrong number of boundary conditions" << std::endl;
        return false;
    }
    is_initialized = true;
    return is_initialized;
}

//! Method to carry out a set of integration steps; can be rerun repeatedly
//! to allow segmentation of the overall simulation and 
//! to allow return of the density grid state to Python 
//! as a series of time slices.
bool SimDP::run(const int n_next_epochs)
{
    if (not is_initialized) 
    { 
        std::cout << "SimDP::run failure: must initialize first" << std::endl;
        return false; 
    }
    did_integrate = integrate(n_next_epochs);
    return did_integrate;
}

//! Method to be called after each `run`: the density grid and grid-average time 
//! series are then packed and made available to Python through the wrapper.
//! This method should be called every time a "snapshot" of the simulation
//! state is desired.
bool SimDP::postprocess()
{
    if (not is_initialized) 
    { 
        std::cout << "SimDP::postprocess failure: no data to process yet" << std::endl;
        return false; 
    }
    bool did_process = (
        pyprep_density_grid() and pyprep_t_epochs() and pyprep_mean_densities() 
    ); 
    return did_process;
}