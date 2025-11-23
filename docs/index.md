# [**langevin**](https://pypi.org/project/langevin/)

###  _Tools for integrating the directed-percolation Langevin equation_


[![](https://github.com/cstarkjp/Langevin/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/cstarkjp/Langevin/actions/workflows/publish-pypi.yml)
[![](https://github.com/cstarkjp/Langevin/actions/workflows/publish-testpypi.yml/badge.svg)](https://github.com/cstarkjp/Langevin/actions/workflows/publish-testpypi.yml)
[![](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-macos.yml/badge.svg)](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-macos.yml)
[![](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-linux.yml/badge.svg)](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-linux.yml)
[![](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-windows.yml/badge.svg)](https://github.com/cstarkjp/Langevin/actions/workflows/unittest-windows.yml)


The  [`langevin` package ](https://pypi.org/project/langevin/) provides software tools to integrate a time-dependent density field described by Langevin equations of directed-percolation type. It can be extended to solve Langevin equations of absorbing phase transition (APT) type.

!!! note "This is a work in progress"
    `langevin` is under active development as part of a research effort.
    If you are interested in using it, or even better, interested in
    collaborating in its development, please contact the maintainer cstarkjp@gmail.com.
    
[Directed percolation (DP)](references.md) is the _type example_ of a non-equilibrium, absorbing phase transition. Its Langevin equation is:
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
where $\rho(\mathbf{x},t)$ is a fluctuating meso-scale field  evolving nonlinearly (with coefficients $a$ and $b$) subject to diffusion (with rate $D$) and multiplicative white noise $\sqrt{\rho}\,\xi(\mathbf{x},t)$ (with amplitude $\eta$).

![Plot of grid-averaged density $\overline{\rho}(t)$ versus time, for an ensemble of simulations with $a$ taking values ranging symmetrically about criticality $a_c \approx 1.8857$ by up to $\Delta{a}=\pm 0.01$.](images/ρ_t_loglog_reduced.png)
<!-- /// caption
Plot of grid-averaged density $\overline{\rho}(t)$ versus time, for an ensemble of simulations with $a$ taking values ranging symmetrically about criticality $a_c \approx 1.8857$ by up to $\Delta{a}=\pm 0.01$.
/// -->


The `langevin` integrator employs the operator-splitting method originated largely by [Dornic et al (2005)](references.md). The software tools are implemented as a [`pip`-installable Python package](https://pypi.org/project/langevin/) with a C++ core, a set of [Jupyter notebooks](https://github.com/cstarkjp/Langevin/tree/main/simulation/dp), and related [Python scripts](https://github.com/cstarkjp/Langevin/tree/main/python).

