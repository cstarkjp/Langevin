# **langevin**

[![PyPI](https://github.com/cstarkjp/Langevin/actions/workflows/publish-pypi.yml/badge.svg?style=cache-control=no-cache)](https://github.com/cstarkjp/Langevin/actions/workflows/publish-pypi.yml)
[![TestPyPi](https://github.com/cstarkjp/Langevin/actions/workflows/publish-testpypi.yml/badge.svg?style=cache-control=no-cache)](https://github.com/cstarkjp/Langevin/actions/workflows/publish-testpypi.yml)
[![macOS](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-macos.yml/badge.svg?style=cache-control=no-cache)](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-macos.yml)
[![Linux](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-linux.yml/badge.svg?style=cache-control=no-cache)](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-linux.yml)
[![Windows](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-windows.yml/badge.svg?style=cache-control=no-cache)](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-windows.yml)

Tools to integrate Langevin equations of absorbing phase transition (APT) type — with a focus on solution of the directed percolation (DP) Langevin equation.

![](https://raw.githubusercontent.com/cstarkjp/Langevin/main/images/ρ_a1p18950_b1_D0p04_η1_x100_y50_Δx1_Δt0p1_rs1.gif
 "Density field evolution over time")

 <!-- ![](https://raw.githubusercontent.com/cstarkjp/Langevin/main/images/density_grid.png
 "Density grid") -->

The `langevin` package implements the operator-splitting method originally developed by Dornic et al (2005), Pechenik & Levine (1999) and others, and improved upon by Weissmann et al (2018).
It provides a Python wrapper around core C++ heavily adapted from a code base written by [Paula Villa Martín](https://github.com/pvillamartin), extended by [Victor Buendía](https://github.com/VictorSeven) ("VMB"), and arising from earlier efforts by Ivan Dornic and Juan Bonachela. The wrapper provides easy access to the Langevin integrator, and broad opportunity to experiment, adapt, and extend it further. 

The current C++ implementation extends the VMB code to allow run-time specification of 
grid dimension and size, boundary topology (bounded or periodic), boundary conditions, and initial conditions. It further provides tools for running model integration 
in batches, time-slicing the Langevin field grid, and recording of time-series
of grid properties.

![](https://raw.githubusercontent.com/cstarkjp/Langevin/main/images/meandensity_time.png
 "Mean density over time")

The equation solved in the demo here is the DP Langevin for a 2D grid with initial values sampled from U[0,1]: 

![](https://raw.githubusercontent.com/cstarkjp/Langevin/main/images/dplangevin_equation3.png
 "DP Langevin equation")


<!-- $`\partial_t \rho = a\rho - b\rho^2 + D \nabla^2 \rho + \gamma \sqrt{\rho} \, \eta`$ -->

where *ρ(**x**,t)* is the order parameter field, *a* and *b* are rate constants, *D* is the diffusion rate over **_x_**, *ξ(**x**,t)* is Gaussian white noise (uncorrelated, zero mean, unit variance), and *η* is the "demographic" noise amplitude.

See 
[Victor Buendía's fork of Paula Villa Martín's repo](https://github.com/VictorSeven/Dornic_et_al_integration_class/tree/victor-update)
 for details on more general applications and on how the integration scheme is implemented.

## Software design

The structure of the DP/APT Langevin-equation integrator package is broadly as follows 
(detailed documentation is available 
[here](https://cstarkjp.github.io/Langevin/doxygen/annotated.html)).

First, there is a wrapper file called [`cplusplus/dp/wrapper_dplvn.cpp`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/dp/wrapper_dplvn.cpp) that uses `pybind11` to link the `C++` code to a Python runtime.

Next, the code is split into a hierarchy of three groups, with each corresponding  file denoted by one of following prefixes: (1) `sim_dplangevin_`, (2) `dplangevin_` and (3) `langevin_`:

   1.   The [`cplusplus/dp/sim_dplangevin_*`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/dp) files provide a `SimDP` class, made available through the wrapper at the Python level, required to manage and execute DP Langevin model integration.  This `SimDP` class instantiates a `DPLangevin` class integrator to do the hard work of numerical integration of the stochastic differential equation. Langevin field density grids are returned to Python (via the wrapper) as `numpy` arrays
   as are time series of the mean density field and its corresponding epochs.


   2. The [`cplusplus/dp/dplangevin_*`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/dp) files define this `DPLangevin` integrator class. They inherit the general `BaseLangevin` integrator class and implement several methods left undefined by that parent; most important, they define methods implementing the particular functional form of the directed-percolation Langevin equation and its corresponding nonlinear, deterministic integration step in the split operator scheme.

       Other types of absorbing-phase transition-type Langevin equation could be
       implemented with alternate subclasses of `BaseLangevin` and alternate 
       versions of the `SimDP` class.


   3. The [`cplusplus/langevin_*`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus) source files provide the base `BaseLangevin` class that implements the operator-splitting integration method in a fairly general fashion. Grid geometry and topology, boundary conditions, initial conditions, the integration scheme, and a general form of the Langevin equation are all coded here. The core Dornic-style integrator is a heavily altered version of the Villa-Martín and Buendía code.


## Installation

### Python environment 
First, set up a suitable Python environment. 
The simplest tool is `uv`, but there are several other options. 
If you use `conda` or `miniconda`, take a look at the `environment.yml` file provided.

We recommend installing Python 3.14 since development of `langevin` uses this version.

For example, if you're using `uv`, all that's needed is to create an
appropriately named folder, navigate to it, and execute:

    uv venv --python=3.14
    source .venv/bin/activate

where the `--python` option forces `uv` to choose that version of the Python intepreter.

### Package from PyPI

Then, install the `langevin` package from PyPI:

    pip install langevin

if you're using `uv`, this command will be

    uv pip install langevin

This step should automatically install all the dependencies as well. 
If it does not, see below.

### Alternative: Package from TestPyPI

If you want to access more regular updates, you can install from TestPyPI:

    [uv] pip install --index https://test.pypi.org/simple/ \
                --default-index https://pypi.org/simple/  langevin

Note: the `--default-index` ensures that package dependencies are fetched from the main PyPI repository where needed.

### Dependencies

At minimum, `langevin` needs Python≥3.12 and the package `pybind11`. To run the demos, you will also need `numpy`, `matplotlib`, `jupyter`, `ipython`, along with `pandas`, `tqdm`, and  `ffmpeg-python`. 
If you are using `conda` or `miniconda`, it would be best to install them using
the `environment.yml` file, instead of relying on `pip` to do the job (mixing `pip` and `conda` is not a great idea anyway, but `langevin` is not yet available on `conda`).

If you want to build locally, you will also need `meson-python`, `wheel`, `pybind11`, and `ninja`.

To turn density field image sequences into animations, `langevin` uses `ffmpeg-python`, which assumes that `ffmpeg` is itself installed on your system. 

On Linux platforms, `matplotlib` has a tendency to complain about missing fonts, e.g., Arial, generating large numbers of warnings in some of the notebooks. This can be fixed by installing the missing fonts and ensuring that `matplotlib`'s cache is refreshed.

### Platform support

We currently have pre-built binary wheels macOS 14, macOS 15, the latest macOS build, and multiple flavors of Linux (most of which have been tested), as well as Windows (but not yet tested). 

## Build from source

If your platform is not explicitly supported with a pre-built binary, the following will force a build from source:

    [uv] pip install -v langevin --no-binary langevin

    
The package can also be built "by hand."
Some build info is provided in the [`cplusplus/`](https://github.com/cstarkjp/Langevin/tree/main/cplusplus/README.md) directory. The build system is [meson-python](https://mesonbuild.com/meson-python/), using [pybind11](https://pybind11.readthedocs.io/en/stable/) as the C++ wrapper. 


## Usage

Simple demonstration scripts are provided in [`demos/`](https://github.com/cstarkjp/Langevin/tree/main/demos/README.md). More complete examples are provided in the [`simulation/`](https://github.com/cstarkjp/Langevin/tree/main/simulation/dp/) directory. The easiest route is to `git` clone the repo to get these files, or you can download one-by-one.


## References

   - [Buendía, 2019: "Dornic integration method for multipicative [sic] noise" (fork of GitHub repo by Villa Martín)](https://github.com/VictorSeven/Dornic_et_al_integration_class/tree/victor-update)  
   <!-- [[shared PDF]](https://www.dropbox.com/scl/fi/jzu0hxbifu8g8njglwfh1/VillaMartin_2014_CatastrophicShiftsLangevinSimulation2D.pdf?rlkey=i9s6s1i19jtgk6pua7xwdaa1a&st=qpfzqyyw&dl=0)  -->

   - [Buendía et al, 2020: "Feedback mechanisms for self-organization to the edge of a phase transition"](https://www.frontiersin.org/journals/physics#editorial-board)  
   <!-- [[shared PDF]](https://www.dropbox.com/scl/fi/oh7j5goqeggfmrc5414ir/Buendia_2020_FeedbackSelfOrganizationPhaseTransitions.pdf?rlkey=ot37k7mw7iaymcgs3g9jg4yhu&st=5stsyu8m&dl=0)  -->

   - [Dornic et al, 2005: "Integration of Langevin equations with multiplicative noise and the viability of field theories for absorbing phase transitions"](https://doi.org/10.1103/PhysRevLett.94.100601)   
   <!-- [[shared PDF]](https://www.dropbox.com/scl/fi/g0h355kxiq47zmxyxlxue/Dornic_2005_MultiplicativenoiseLangevinIntegrationDirectedPercolation.pdf?rlkey=aj5k6zekitc02lno0b50yhjbx&st=vzd5hdfz&dl=0) -->

   - [Pechenik & Levine, 1999: "Interfacial velocity corrections due to multiplicative noise"](https://doi.org/10.1103/PhysRevE.59.3893)   
   <!-- [[shared PDF]](https://www.dropbox.com/scl/fi/ylu6r5vk34r9sdv8aoiqh/PechenikLevine_1999_MultiplicativeNoiseNonequilibriumPhaseTransitionSDE.pdf?rlkey=90ncj263w5n41hncosiww5n41&st=7uuvp79z&dl=0) -->

   - [Villa Martín et al, 2014: "Eluding catastrophic shifts"](https://doi.org/10.1073/pnas.1414708112)   
   <!-- [[shared PDF]](https://www.dropbox.com/scl/fi/jzu0hxbifu8g8njglwfh1/VillaMartin_2014_CatastrophicShiftsLangevinSimulation2D.pdf?rlkey=i9s6s1i19jtgk6pua7xwdaa1a&st=qpfzqyyw&dl=0)  -->

   - [Villa Martín, 2019  (GitHub repo): "Dornic integration method for multipicative [sic] noise"](https://github.com/pvillamartin/Dornic_et_al_integration_class)   [[shared PDF]](https://www.dropbox.com/scl/fi/sdeiwyxjpyx6a2tv5vibr/VillaMartin_2019_DornicMethod.pdf?rlkey=wykox7ifyu0ms4pd3hokp1d4u&st=xir9d3vt&dl=0) 

   - [Weissmann et al, 2018: "Simulation of spatial systems with demographic noise"](https://doi.org/10.1103/PhysRevE.98.022131)   
