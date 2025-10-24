/**
 * @file sim_dplangevin_utilities.cpp
 * @brief Utility interface functions provided to the Python module.
 */ 

#include "sim_dplangevin.hpp"

int SimDP::get_n_epochs() const { return n_epochs; }
int SimDP::get_i_current_epoch() const { return i_current_epoch; }
int SimDP::get_i_next_epoch() const { return i_next_epoch; }
double SimDP::get_t_current_epoch() const { return t_current_epoch; }
double SimDP::get_t_next_epoch() const { return t_next_epoch; }
py_array_t SimDP::get_t_epochs() const { return pyarray_t_epochs; }
py_array_t SimDP::get_mean_densities() const { return pyarray_mean_densities; }
py_array_t SimDP::get_density() const { return pyarray_density; }

