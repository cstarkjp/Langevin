/**
 * @file langevin_enums.hpp
 * @brief Enumerated parameter options for BaseLangevin integrator.
 * 
 * Parameter options as enums, used in both C++ and Python, used to choose 
 * e.g. suitable grid geometries, topologies, boundary and initial conditions, 
 * and the lowest-level integration method.
 */

#ifndef ENUMS_HPP
#define ENUMS_HPP

//! Density field grid dimension: only 1D or 2D grids implemented so far
enum class GridDimension
{
    D1 = 1,
    D2 = 2,
    D3 = 3
};

//! Classifier for grid edges used in boundary condition handling
enum class GridEdge
{
    lx = 1,
    ux = 2,
    ly = 3,
    uy = 4
    // lz = 5,
    // uz = 6
};

//! Grid boundary topology: only bounded or periodic (along all edges) implemented so far
enum class GridTopology
{
    BOUNDED = 1,
    PERIODIC = 2
};

//! Grid boundary condition: floating/fixed value/fixed flux; application equally to all edges only for now
enum class BoundaryCondition
{
    FLOATING = 1,
    FIXED_VALUE = 2,
    FIXED_FLUX = 3
};

//! Grid density field initial condition: random uniform or Gaussian variates; constant everywhere; or central seed value
enum class InitialCondition
{
    RANDOM_UNIFORM = 1,
    RANDOM_GAUSSIAN = 2,
    CONSTANT_VALUE = 3,
    SINGLE_SEED = 4
};

//! Deterministic integration method: default is 4th-order Runge-Kutta; can be explicit Euler
enum class IntegrationMethod
{
    EULER = 1,
    RUNGE_KUTTA = 2
};

#endif