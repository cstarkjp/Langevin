/**
 * @file langevin_bc.cpp
 * @brief Methods for setting boundary conditions for Langevin model.
 */

#include "langevin_types.hpp"
#include "langevin_base.hpp"

//! Check that 2x bcs are specified for each grid dimension, one for each edge
bool BaseLangevin::check_boundary_conditions(const Parameters p)
{
    switch (p.grid_dimension)
    {
        case (GridDimension::D1):
            return (p.bc_values.size()==2);
        case (GridDimension::D2):
            return (p.bc_values.size()==4);
        case (GridDimension::D3):
            return (p.bc_values.size()==6);
        default:
            return false;
    }
}

//! Apply boundary conditions along each edge in turn 
void BaseLangevin::apply_boundary_conditions(const Parameters p, int i_epoch)
{
    auto i_from_xy = [&](int x, int y) -> int { return x + y*p.n_x; };
    auto add_to_density = [&](int x, int y, double value)
    {
        density_grid[i_from_xy(x, y)] 
            = fmax(density_grid[i_from_xy(x, y)] + value*p.dt, 0.0);

    };
    auto apply_bc_to_edge_2d = [&] (
        GridEdge grid_edge, BoundaryCondition bc, double value
    ) 
    {
        if (bc==BoundaryCondition::FIXED_VALUE) 
        {
            switch (grid_edge)
            {
                case (GridEdge::lx):
                    for (auto x=0; x<p.n_x; x++){
                        density_grid[i_from_xy(x,0)] = value;
                    }
                    break;
                case (GridEdge::ux):
                    for (auto x=0; x<p.n_x; x++){
                        density_grid[i_from_xy(x, p.n_y-1)] = value;
                    }
                    break;
                case (GridEdge::ly):
                    for (auto y=0; y<p.n_y; y++){
                        density_grid[i_from_xy(0, y)] = value;
                    }
                    break;
                case (GridEdge::uy):
                    for (auto y=0; y<p.n_y; y++){
                        density_grid[i_from_xy(p.n_x-1, y)] = value;
                    }
                    break;
            }
        }
        // Don't "add flux" if we're at epoch#0
        else if (bc==BoundaryCondition::FIXED_FLUX and i_epoch>0) 
        {
            switch (grid_edge)
            {
                case (GridEdge::lx):
                    for (auto x=0; x<p.n_x; x++){
                        auto y = 0;
                        add_to_density(x, y, value);
                    }
                    break;
                case (GridEdge::ux):
                    for (auto x=0; x<p.n_x; x++){
                        auto y = p.n_y-1;
                        add_to_density(x, y, value);
                    }
                    break;
                case (GridEdge::ly):
                    for (auto y=0; y<p.n_y; y++){
                        auto x = 0;
                        add_to_density(x, y, value);
                    }
                    break;
                case (GridEdge::uy):
                    for (auto y=0; y<p.n_y; y++){
                        auto x = p.n_x-1;
                        add_to_density(x, y, value);
                    }
                    break;
            }
        }
    };
    auto apply_boundary_conditions_1d = [&]()
    {
        // apply_bc_to_edge_1d(GridEdge::lx, p.boundary_conditions.at(0), p.bc_values.at(0));
        // apply_bc_to_edge_1d(GridEdge::ux, p.boundary_conditions.at(1), p.bc_values.at(1));
    };
    auto apply_boundary_conditions_2d = [&]()
    {
        apply_bc_to_edge_2d(
            GridEdge::lx, p.boundary_conditions.at(0), p.bc_values.at(0)
        );
        apply_bc_to_edge_2d(
            GridEdge::ux, p.boundary_conditions.at(1), p.bc_values.at(1)
        );
        apply_bc_to_edge_2d(
            GridEdge::ly, p.boundary_conditions.at(2), p.bc_values.at(2)
        );
        apply_bc_to_edge_2d(
            GridEdge::uy, p.boundary_conditions.at(3), p.bc_values.at(3)
        );
    };
    auto apply_boundary_conditions_3d = [&]()
    {
        // apply_bc_to_edge(GridEdge::lx, p.boundary_conditions.at(0), p.bc_values.at(0));
        // apply_bc_to_edge(GridEdge::ux, p.boundary_conditions.at(1), p.bc_values.at(1));
        // apply_bc_to_edge(GridEdge::ly, p.boundary_conditions.at(2), p.bc_values.at(2));
        // apply_bc_to_edge(GridEdge::uy, p.boundary_conditions.at(3), p.bc_values.at(3));
    };

    switch (p.grid_dimension)
    {
        case (GridDimension::D1):
            apply_boundary_conditions_1d();
            break;
        case (GridDimension::D2):
            apply_boundary_conditions_2d();
            break;
        case (GridDimension::D3):
            apply_boundary_conditions_3d();
            break;
    }
}
