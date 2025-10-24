/**
 * @file langevin_construct_grid.cpp
 * @brief Wrapper around 1D or 2D grid construction methods.
 */

#include "langevin_types.hpp"
#include "langevin_base.hpp"

bool BaseLangevin::construct_grid(const Parameters p)
{
    switch (p.grid_dimension)
    {
        case (GridDimension::D1):
            return construct_1D_grid(p);
        case (GridDimension::D2):
            return construct_2D_grid(p);
        case (GridDimension::D3):
            return false; // NYI
        default:
            return false;
    }    
}