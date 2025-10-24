# Design of `lvn` package

The structure of the DP/APT Langevin-equation integrator package is broadly as follows 
(detailed documentation is available 
[here](https://cstarkjp.github.io/Langevin/doxygen/annotated.html)).

First, there is a wrapper file called [`cplusplus/dp/wrapper_dplvn.cpp`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/dp/wrapper_dplvn.cpp) that uses `pybind11` to link the `C++` code to a Python runtime.

Next, the code is split into a hierarchy of three groups, with each corresponding  file denoted by one of following prefixes: (1) `sim_dplangevin_`, (2) `dplangevin_` and (3) `langevin_`:

   1.   The [`cplusplus/dp/sim_dplangevin_*`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/dp) files provide a `SimDP` class, made available through the wrapper at the Python level, required to manage and execute DP Langevin model integration.  This `SimDP` class instantiates a `Langevin` class integrator to do the hard work of numerical integration of the stochastic differential equation. Langevin field density grids are returned to Python (via the wrapper) as `numpy` arrays
   as are time series of the mean density field and its corresponding epochs.


   2. The [`cplusplus/dp/dplangevin_*`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/dp) files define this `Langevin` integrator class. They inherit the general `BaseLangevin` integrator class and implement several methods left undefined by that parent; most important, they define methods implementing the particular functional form of the directed-percolation Langevin equation and its corresponding nonlinear, deterministic integration step in the split operator scheme.

       Other types of absorbing-phase transition-type Langevin equation could be
       implemented with alternate subclasses of `BaseLangevin` and alternate 
       versions of the `SimDP` class.


   3. The [`cplusplus/langevin_*`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus) source files provide the base `BaseLangevin` class that implements the operator-splitting integration method in a fairly general fashion. Grid geometry and topology, boundary conditions, initial conditions, the integration scheme, and a general form of the Langevin equation are all coded here. The core Dornic-style integrator is a heavily altered version of the Villa-Martín and Buendía code.
