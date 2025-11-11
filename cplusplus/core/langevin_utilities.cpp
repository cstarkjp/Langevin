/**
 * @file langevin_utilities.cpp
 * @brief Utility methods to process the Langevin field grid.
 */

#include "langevin_types.hpp"
#include "langevin_base.hpp"

//! Return the Langevin density field grid value at a given "node"
double BaseLangevin::get_density_grid_value(const int i) const 
{
    return density_grid[i];
}

//! Return the grid-averaged Langevin field mean value
double BaseLangevin::get_mean_density() const
{
    return mean_density;
}

//! Compute the mean field density times "lamba_product", 
//! which should be equal to the Poisson distribution mean
double BaseLangevin::get_poisson_mean() const
{
    return lambda_on_explcdt * mean_density;
}