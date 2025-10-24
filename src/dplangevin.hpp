/**
 * @file dplangevin.hpp
 * @brief DPLangevin model application of BaseLangevin class integrator.
 */

#ifndef DPLANGEVIN_HPP
#define DPLANGEVIN_HPP

#include "langevin_types.hpp"
#include "langevin_base.hpp"

/**
 * @brief DPLangevin model application of BaseLangevin class integrator.
 */
class DPLangevin : public BaseLangevin 
{
public:
    //! Constructor assuming default model parameters
    DPLangevin() = default;
    //! Constructor when model parameters are passed by the user
    DPLangevin(Parameters p);

    //! Coefficient in nonlinear term -bρ² in DP-Langevin equation
    double quadratic_coefficient;
    //! Diffusion coefficient D in DP-Langevin equation
    double diffusion_coefficient;
    
    //! Method to set nonlinear coefficients for deterministic integration step
    void set_nonlinear_coefficients(const Coefficients& coefficients);
    //! Method to set nonlinear RHS of Langevin equation for deterministic integration step
    double nonlinear_rhs(const int i_cell, const grid_t& density) const;
};

#endif
