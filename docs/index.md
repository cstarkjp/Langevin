# Langevin


 _Tools for integrating the DP Langevin equation — implemented as a Python package `lvn`, a set of Jupyter notebooks, and related Python scripts._


The directed-percolation (DP) Langevin equation is:
$$
    \partial_t\rho
    =
    a \rho
    -
    b \rho^2
    +
    D \nabla^2 \rho
    +
    \eta\sqrt{\rho}\,\xi
$$
which describes a field $\rho(\mathbf{x},t)$ evolving nonlinearly (with coefficients $a$ and $b$) subject to diffusion (with rate $D$) and multiplicative white noise $\sqrt{\rho}\,\xi(\mathbf{x},t)$ (with amplitude $\eta$).

![Plot of grid-averaged density $\overline{\rho}(t)$ versus time, for an ensemble of simulations with $a$ taking values ranging symmetrically about criticality $a_c \approx 1.8857$ by up to $\Delta{a}=\pm 0.01$:](images/ρ_t_loglog.png)


[Installation notes are available here](installation.md).

[Rough notes on how to run simulations are available here.](run.md) The only awkward aspect is the organization of [`Info.json`](info-reference.md) files and the naming of their parent folders.

Head to the links under  "Notebooks" or "Python scripts" in the sidebar/menu for demos.

Refer to the links under "Modules" to see documentation of the `lvn` Python package.

`lvn` relies heavily on the C++ based Python library `dpvln`, which is currently only available on TestPyPI at [https://test.pypi.org/project/dplvn/](https://test.pypi.org/project/dplvn/) and documented at [https://cstarkjp.github.io/DPLangevin/md_README.html](https://cstarkjp.github.io/DPLangevin/md_README.html)


***This is a work in progress.***
