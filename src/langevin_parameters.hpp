/**
 * @file langevin_parameters.hpp
 * @brief Container for BaseLangevin integrator parameters.
 * 
 * Container for BaseLangevin integrator parameters.
 * Includes method to print most/all of these parameters,
 * using overloaded methods to report struct-type parameters.
 * The constructor does a modicum of computation to deduce grid
 * dimensions.
 */

#ifndef PARAMETERS_HPP
#define PARAMETERS_HPP

/**
 * @brief Container  for BaseLangevin integrator parameters.
 * 
 * 
 */
struct Parameters 
{
public:
    const double t_final=0;
    const double dx=0;
    const double dt=0;
    const int random_seed=0;
    const GridDimension grid_dimension=GridDimension::D1;
    const int_vec_t grid_size={};
    int n_cells=0;
    int n_x=0;
    int n_y=0;
    int n_z=0;
    const gt_vec_t grid_topologies = {};
    const bc_vec_t boundary_conditions = {};
    const dbl_vec_t bc_values={};
    const InitialCondition initial_condition=InitialCondition::RANDOM_UNIFORM;
    const dbl_vec_t ic_values={};
    const IntegrationMethod integration_method=IntegrationMethod::RUNGE_KUTTA;

    Parameters() = default;
    Parameters(
        const double t_final, 
        const double dx, const double dt, 
        const int rs, 
        const GridDimension gd,
        const int_vec_t gs,
        const gt_vec_t gts,
        const bc_vec_t bcs,
        const dbl_vec_t bcv,
        const InitialCondition ic,
        const dbl_vec_t icv,
        const IntegrationMethod im
    ) : 
        t_final(t_final), 
        dx(dx), dt(dt), 
        random_seed(rs),
        grid_dimension(gd), 
        grid_size(gs),
        grid_topologies(gts),
        boundary_conditions(bcs),
        bc_values(bcv),
        initial_condition(ic), 
        ic_values(icv),
        integration_method(im)
    {
        n_x = gs.at(0);
        n_y = (gs.size()>1) ? gs.at(1) : 1;
        n_z = (gs.size()>2) ? gs.at(2) : 1;
        n_cells = n_x * n_y * n_z;
    }

    // Use overloading to provide alternate "printout" commands
    std::string report(GridDimension gd) 
    {
        switch (gd) {
            case GridDimension::D1: return "1d";
            case GridDimension::D2: return "2d";
            case GridDimension::D3: return "3d";
            default: return "Unknown";
        }
    }
    std::string report(GridTopology gt) 
    {
        switch (gt) {
            case GridTopology::BOUNDED: return "bounded";
            case GridTopology::PERIODIC: return "periodic";
            default: return "Unknown";
        }
    }
    std::string report(GridDimension gd, gt_vec_t gts) 
    {
        std::string combo = "x edge:";
        combo.append(report(gts.at(0)));
        if (gd==GridDimension::D2 or gd==GridDimension::D3)
        {
            combo.append("; y edge:");
            combo.append(report(gts.at(1)));
        }
        if (gd==GridDimension::D3)
        {
            combo.append("; z edge:");
            combo.append(report(gts.at(2)));
        }
        return combo;
    }
    std::string report(BoundaryCondition bc) 
    {
        switch (bc) {
            case BoundaryCondition::FLOATING: return "floating";
            case BoundaryCondition::FIXED_VALUE: return "fixed value";
            case BoundaryCondition::FIXED_FLUX: return "fixed flux";
            default: return "Unknown";
        }
    }
    std::string report(GridDimension gd, bc_vec_t bcs) 
    {
        std::string combo = "x0 edge:";
        combo.append(report(bcs.at(0)));
        combo.append(", x1 edge:");
        combo.append(report(bcs.at(1)));
        if (gd==GridDimension::D2 or gd==GridDimension::D3)
        {
            combo.append("; y0 edge:");
            combo.append(report(bcs.at(2)));
            combo.append(", y1 edge:");
            combo.append(report(bcs.at(3)));
        }
        if (gd==GridDimension::D3)
        {
            combo.append("; z0 edge:");
            combo.append(report(bcs.at(2)));
            combo.append(", z1 edge:");
            combo.append(report(bcs.at(2)));
        }
        return combo;
    }
    std::string report(InitialCondition ic) 
    {
        switch (ic) {
            case InitialCondition::RANDOM_UNIFORM: return "uniform random values";
            case InitialCondition::RANDOM_GAUSSIAN: return "Gaussian random values";
            case InitialCondition::CONSTANT_VALUE: return "constant value";
            case InitialCondition::SINGLE_SEED: return "single seed";
            default: return "Unknown";
        }
    }
    std::string report(IntegrationMethod im) 
    {
        switch (im) {
            case IntegrationMethod::EULER: return "Euler";
            case IntegrationMethod::RUNGE_KUTTA: return "Runge-Kutta";
            default: return "Unknown";
        }
    }

    void print() 
    {
            std::cout << std::endl;        
        std::cout << "t_final: " << t_final << std::endl;
        std::cout << "dx: " << dx << std::endl;
        std::cout << "dt: " << dt << std::endl;
            std::cout << std::endl;        
        std::cout << "random_seed: " << random_seed << std::endl;
        std::cout << "grid_dimension: " << report(grid_dimension) << std::endl;
        std::cout << "grid_size: ";
        for (const auto& element : grid_size) {std::cout << element << " ";}
            std::cout << std::endl;        
        std::cout << "n_cells: " << n_cells << std::endl;
        std::cout << "grid_topologies: " 
            << report(grid_dimension, grid_topologies) << std::endl;
        std::cout << "boundary_conditions: " 
            << report(grid_dimension, boundary_conditions) << std::endl;
        std::cout << "bc_values: ";
        for (const auto& element : bc_values) {std::cout << element << " ";}
            std::cout << std::endl;        
        std::cout << "initial_condition: " 
            << report(initial_condition) << std::endl;
        std::cout << "ic_values: ";
        for (const auto& element : ic_values) {std::cout << element << " ";}
            std::cout << std::endl;        
        std::cout << "integration_method: "  
            << report(integration_method) << std::endl;
    }
};

#endif