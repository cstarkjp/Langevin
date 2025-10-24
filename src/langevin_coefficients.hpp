/**
 * @file langevin_coefficients.hpp
 * @brief Container for nonlinear Langevin equation coefficients.
 */

#ifndef COEFFICIENTS_HPP
#define COEFFICIENTS_HPP

/**
 * @brief Container for nonlinear Langevin equation coefficients.
 *
 * Container for the set of coefficients in the nonlinear Langevin 
 * equation to be integrated, which here is the directed percolation (DP)
 * Langevin equation.
 * Includes a method to print out all coefficient values.
 *
 * @param linear Coefficient a in linear term +aρ.
 * @param quadratic  Coefficient b in nonlinear term -bρ².
 * @param diffusion Diffusion rate D in diffusion term D∇²ρ.
 * @param noise Noise amplitude γ in noise term γ√(ρ)η.
 * 
 */
struct Coefficients 
{
public:
    double linear;
    double quadratic;
    double diffusion;
    double noise;
    
    Coefficients(
        double linear, double quadratic, double diffusion, double noise
    ) : linear(linear), quadratic(quadratic), diffusion(diffusion), noise(noise) {}

    void print() {
        std::cout << "linear: " << linear << std::endl;
        std::cout << "quadratic: " << quadratic << std::endl;
        std::cout << "diffusion: " << diffusion << std::endl;
        std::cout << "noise: " << noise << std::endl;
    }
};

#endif