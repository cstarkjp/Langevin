# Design of `lvn` package

The structure of the DP/APT Langevin-equation integrator package is broadly as described below. 
Detailed documentation is available 
[here](https://cstarkjp.github.io/Langevin/doxygen/annotated.html). 
The C++ code base is to be found [here](https://github.com/cstarkjp/Langevin/tree/main/cplusplus) and the Python wrapper code is located [here](https://github.com/cstarkjp/Langevin/tree/main/python).

TODO: add info about supporting Python files.

First, there is a wrapper file called [`cplusplus/dp/wrapper_dplvn.cpp`](https://cstarkjp.github.io/Langevin/doxygen/wrapper__dplvn_8cpp.html) that uses [`pybind11`](https://pybind11.readthedocs.io/en/stable/) to link the [`C++` code](https://cstarkjp.github.io/Langevin/cplusplus/) to a Python runtime.

Next, the code is split into a hierarchy of three groups, with each corresponding  file denoted by one of following prefixes: (1) [`sim_dplangevin_`](https://cstarkjp.github.io/Langevin/doxygen/dir_29b47bf0c8dc04d64d9bcc2119390c05.html), (2) [`dplangevin_`](https://cstarkjp.github.io/Langevin/doxygen/dir_29b47bf0c8dc04d64d9bcc2119390c05.html) and (3) [`langevin_`](https://cstarkjp.github.io/Langevin/doxygen/dir_413eba86a22d58dd6c01dd4edd69cedc.html):

   1.   The [`cplusplus/dp/sim_dplangevin_*`](https://cstarkjp.github.io/Langevin/doxygen/dir_29b47bf0c8dc04d64d9bcc2119390c05.html) files provide a [`SimDP` class](https://cstarkjp.github.io/Langevin/doxygen/class_sim_d_p.html), made available through the wrapper at the Python level, required to manage and execute DP Langevin model integration.  This [`SimDP` class](https://cstarkjp.github.io/Langevin/doxygen/class_sim_d_p.html) instantiates a [`DPLangevin` class integrator](https://cstarkjp.github.io/Langevin/doxygen/class_d_p_langevin.html) to do the hard work of numerical integration of the stochastic differential equation. Langevin field density grids are returned to Python [(via the wrapper)](https://cstarkjp.github.io/Langevin/doxygen/wrapper__dplvn_8cpp.html) as `numpy` arrays,
   as are time series of the mean density field and its corresponding epochs.


   2. The [`cplusplus/dp/dplangevin_*`](https://cstarkjp.github.io/Langevin/doxygen/dir_29b47bf0c8dc04d64d9bcc2119390c05.html) files define this [`DPLangevin` integrator class](https://cstarkjp.github.io/Langevin/doxygen/class_d_p_langevin.html). They inherit the general [`BaseLangevin` integrator class](https://cstarkjp.github.io/Langevin/doxygen/class_base_langevin.html)  and implement several methods left undefined by that parent; most important, they define methods implementing the particular functional form of the directed-percolation Langevin equation and its corresponding nonlinear, deterministic integration step in the split operator scheme.

       Other types of absorbing-phase transition-type Langevin equation could be
       implemented with alternate subclasses of [`BaseLangevin`](https://cstarkjp.github.io/Langevin/doxygen/class_base_langevin.html) and alternate 
       versions of the [`SimDP` class](https://cstarkjp.github.io/Langevin/doxygen/class_sim_d_p.html).


   3. The [`cplusplus/langevin_*`](https://cstarkjp.github.io/Langevin/doxygen/dir_413eba86a22d58dd6c01dd4edd69cedc.html) source files provide the base [`BaseLangevin` class](https://cstarkjp.github.io/Langevin/doxygen/class_base_langevin.html) that implements the operator-splitting integration method in a fairly general fashion. Grid geometry and topology, boundary conditions, initial conditions, the integration scheme, and a general form of the Langevin equation are all coded here. The core Dornic-style integrator is a heavily altered version of the [Villa-Martín and Buendía code](references.md).
