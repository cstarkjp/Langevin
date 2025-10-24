/**
 * @file sim_dplangevin_private.cpp
 * @brief Class to manage & run DPLangevin model simulation: private methods.
 */ 

#include "sim_dplangevin.hpp"

double round(const double value, const int n_decimals) {
    const double multiplier = std::pow(10, n_decimals);
    return std::round(value * multiplier) / multiplier;
}


//! Count total number of time steps, just in case rounding causes problems
int SimDP::count_epochs() const
{
    int n_epochs;
    double t; 
    for (
        n_epochs=0, t=0; 
        t<p.t_final; 
        t=round(t+p.dt, n_decimals), n_epochs++
    ) {}
    return n_epochs+1;
}

bool SimDP::choose_integrator()
{
    switch (p.integration_method)
    {
        case (IntegrationMethod::RUNGE_KUTTA):
            integrator = &DPLangevin::integrate_rungekutta;
            return true;
        case (IntegrationMethod::EULER):
            integrator = &DPLangevin::integrate_euler;
            return true;
        default:
            return false;
    }
}

bool SimDP::integrate(const int n_next_epochs)
{
    // Check a further n_next_epochs won't exceed total permitted steps
    if (t_epochs.size() < i_next_epoch+n_next_epochs)
    {
        std::cout << "Too many epochs: " 
            << t_epochs.size() 
            << " < " 
            << i_next_epoch+n_next_epochs 
            << std::endl;
        return false;
    }
    
    // Perform (possibly another another) n_next_epochs integration steps
    int i;
    double t; 
    // For the very first epoch, record mean density right now
    if (i_next_epoch==1) { 
        dpLangevin->apply_boundary_conditions(p, 0);
        mean_densities[0] = dpLangevin->get_mean_density(); 
        i_current_epoch = 0;
        t_current_epoch = 0;
    }
    // Loop over integration steps.
    // Effectively increment epoch counter and add to Δt to time counter
    // so that both point the state *after* each integration step is complete.
    // In so doing, we will record t_epochs.size() + 1 total integration steps.
    for (
        i=i_next_epoch, t=t_next_epoch; 
        i<i_next_epoch+n_next_epochs; 
        t=round(t+p.dt, n_decimals), i++
    )
    {
        // Reapply boundary conditions prior to integrating
        dpLangevin->apply_boundary_conditions(p, i);
        // Perform a single integration over Δt
        (dpLangevin->*integrator)(*rng);
        // Record this epoch
        t_epochs[i] = t;
        mean_densities[i] = dpLangevin->get_mean_density();
        i_current_epoch = i;
        t_current_epoch = t;
    };
    // Set epoch and time counters to point to *after* the last integration step
    i_next_epoch = i;
    t_next_epoch = t;
    return true;
}

bool SimDP::pyprep_t_epochs()
{
    py_array_t epochs_array(n_epochs);
    auto epochs_proxy = epochs_array.mutable_unchecked();
    for (auto i=0; i<n_epochs; i++)
    {
        epochs_proxy(i) = t_epochs[i];
    };
    pyarray_t_epochs = epochs_array;
    return true;
}

bool SimDP::pyprep_mean_densities()
{
    py_array_t mean_densities_array(n_epochs);
    auto mean_densities_proxy = mean_densities_array.mutable_unchecked();
    for (auto i=0; i<n_epochs; i++)
    {
        mean_densities_proxy(i) = mean_densities[i];
    };
    pyarray_mean_densities = mean_densities_array;
    return true;
}

bool SimDP::pyprep_density_grid()
{
    if (not (p.n_cells == p.n_x * p.n_y * p.n_z)) 
    { 
        std::cout << "prep_density: grid size problem" << std::endl;
        return false; 
    }
    // Assume we're working with a <=2d grid for now
    py_array_t density_array({p.n_x, p.n_y});
    auto density_proxy = density_array.mutable_unchecked();
    for (auto i=0; i<p.n_cells; i++)
    {
        int x = i % p.n_x;
        int y = i / p.n_x;
        density_proxy(x, y) = dpLangevin->get_density_grid_value(i);
    };
    pyarray_density = density_array;
    return true;
}