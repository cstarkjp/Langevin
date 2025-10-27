/**
 * @file sim_dplangevin.hpp
 * @brief Class that manages simulation of DPLangevin equation.
 */ 

#ifndef SIMDP_HPP
#define SIMDP_HPP

#include "dplangevin.hpp"

/**
 * @brief Class that manages simulation of DPLangevin equation.
 *
 * Manages & executes model simulation using instances of 
 * the DPLangevin integrator class, the Coefficients struct, and the 
 * Parameters struct.
 */
class SimDP 
{
private:
    //! Langevin equation coefficients
    Coefficients coefficients;
    //! Model simulation parameters
    Parameters p;
    //! Random number generation function (Mersenne prime) (pointer to RNG)
    rng_t *rng; 
    //! Instance of DP Langevin integrator class (pointer to instance)
    DPLangevin *dpLangevin;
    //! Integrator: either a Runge-Kutta or an Euler method
    void (DPLangevin::*integrator)(rng_t&);
    
    //! Total number of simulation time steps aka "epochs"
    int n_epochs;
    //! Index of current epoch aka time step
    int i_current_epoch;
    //! Index of next epoch aka time step
    int i_next_epoch;
    //! Time of current epoch
    double t_current_epoch;
    //! Time of next epoch
    double t_next_epoch;
    //! Vector time-series of epochs
    dbl_vec_t t_epochs;
    //! Truncation number of decimal places when summing Δt
    int n_decimals;
    //! Vector time-series of grid-averaged field density values
    dbl_vec_t mean_densities;
    //! Python-compatible array of epochs time-series
    py_array_t pyarray_t_epochs;
    //! Python-compatible array of mean density time-series
    py_array_t pyarray_mean_densities;
    //! Python-compatible array of current density grid
    py_array_t pyarray_density;
    //! Flag whether integration step was successful or not
    bool did_integrate = false;
    //! Flag whether simulation has been initialized or not
    bool is_initialized = false;
    //! Flag whether to take density grid snapshots
    bool do_snapshot_grid = true;
    //! Flag whether to report sim parameters etc
    bool do_verbose = false;

    //! Count upcoming number of epochs by running a dummy time-stepping loop
    int count_epochs() const;
    //! Chooses function implementing either Runge-Kutta or Euler integration methods
    bool choose_integrator();
    //! Perform Dornic-type integration of the DP Langevin equation for `n_next_epochs`
    bool integrate(const int n_next_epochs);

    //! Generate a Python-compatible version of the epochs time-series vector
    bool pyprep_t_epochs();
    //! Generate a Python-compatible version of the mean densities time-series vector
    bool pyprep_mean_densities();
    //! Generate a Python-compatible version of the current density grid
    bool pyprep_density_grid();

public:
    //! Constructor
    SimDP(
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
        const bool do_snapshot_grid,
        const bool do_verbose
    );
    //! Initialize the model simulation
    bool initialize(int n_decimals);
    //! Execute the model simulation for `n_next_epochs`
    bool run(const int n_next_epochs);
    //! Process the model results data if available
    bool postprocess();

    // Utilities provided to Python via the wrapper

    //! Fetch the total number of simulation epochs
    int get_n_epochs() const;
    //! Fetch the index of the current epoch of the simulation
    int get_i_current_epoch() const;
    //! Fetch the index of the next epoch of the simulation
    int get_i_next_epoch() const;
    //! Fetch the current epoch (time) of the simulation
    double get_t_current_epoch() const;
    //! Fetch the next epoch (time) of the simulation
    double get_t_next_epoch() const;
    //! Fetch a times-series vector of the simulation epochs as a Python array
    py_array_t get_t_epochs() const;
    //! Fetch a times-series vector of the grid-averaged density field over time as a Python array
    py_array_t get_mean_densities() const;
    //! Fetch the current Langevin density field grid as a Python array
    py_array_t get_density() const;
};


#endif
