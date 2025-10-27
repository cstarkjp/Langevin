# Navigation

The structure of this software package is described on the ["Software design"](software-design.md) page, which is also accessible via the sidebar.

Installation notes are available on the ["How to install"](how-to-install.md) page.
Notes on running simulations are available on the corresponding ["How to run"](how-to-run.md) page. 

Links to test scripts are provided under [`Tests`](tests-reference.md).
Look under under "Simulation tools" in the sidebar for more complete examples and further information.

The key driver of a simulation is the [`Info.json`](info-reference.md) file: care must be taken to match the "job name" implied by this file (a string constructed from the model coefficients and parameters specified by it) with its parent folder name, such that output files are placed correctly.

Refer to the links under "Python modules" to see documentation of the `lvn` Python package. The underlying `C++` core is documented under "C++ source" using `Doxygen`.
