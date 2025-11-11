/**
 * @file langevin_construct_grid1d.cpp
 * @brief Method for setting up a 1D grid for the model Langevin field.
 */

#include "langevin_types.hpp"
#include "langevin_base.hpp"

//! Construct 1D density field ρ(x,t) grid and corresponding cell-cell topologies
bool BaseLangevin::construct_1D_grid(const Parameters p)
{
    const auto n_x = p.n_x;
    grid_wiring = grid_wiring_t(n_x, neighborhood_t(2));

    // Everywhere except the grid ends
    for (auto i=1; i<n_x-1; i++)
    {
        // Each cell has a L and R neighbor whose indexes are specified here
        grid_wiring[i][0] = i-1;
        grid_wiring[i][1] = i+1;
    }

    // Grid ends
    switch (p.grid_topologies.at(0))
    {
        case GridTopology::PERIODIC:
            // Each end cell neighbor is the other end cell, so wrap the indexes
            grid_wiring[0][0] = n_x-1;      // left-end left
            grid_wiring[0][1] = 1;          // left-end right
            grid_wiring[n_x-1][0] = n_x-2;  // right-end left VMB: [n_x-1][0] = n_x-2;
            grid_wiring[n_x-1][1] = 0;      // right-end right
            return true;
            
        case GridTopology::BOUNDED:
            // Link each end cell to its adjacent cell only
            grid_wiring[0] = neighborhood_t(1, 1);
            grid_wiring[n_x-1] = neighborhood_t(1, n_x-2);
            return true;

        default:
            return false;
    }
}