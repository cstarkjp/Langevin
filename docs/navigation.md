# Navigation

The structure of this software package is described on the ["Software design"](software-design.md) page, which is also accessible via the sidebar.

Installation notes are available on the ["How to install"](how-to-install.md) page.
Notes on running simulations are available on the corresponding ["How to run"](how-to-run.md) page. 

Links to demo scripts are provided under ["Demos"](demos-reference.md).
See [Simulation tools](simulation-tools/index.md) for more complete examples and further information.

The key driver of a simulation is the [`Info.json`](simulation-tools/info-reference.md) file: care must be taken to match the "job name" implied by this file (a string constructed from the model coefficients and parameters specified by it) with its parent folder name, such that output files are placed correctly.

Refer to the links under "Python modules" to see documentation of the 
[`langevin` Python package](https://pypi.org/project/langevin/). The underlying `C++` core is documented under ["C++ source"](cplusplus-source/index.md) using `Doxygen`.
