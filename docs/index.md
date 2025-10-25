# Langevin

 _Tools for integrating APT-type Langevin equations._

The package `lvn` provides software tools to help integrate the evolving density field described by Langevin equations of absorbing phase transition (APT) type.
Directed percolation is the type-example of such an absorbing phase transition. Its Langevin equation is:
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
which describes a fluctuating meso-scale field $\rho(\mathbf{x},t)$ evolving nonlinearly (with coefficients $a$ and $b$) subject to diffusion (with rate $D$) and multiplicative white noise $\sqrt{\rho}\,\xi(\mathbf{x},t)$ (with amplitude $\eta$).

![Plot of grid-averaged density $\overline{\rho}(t)$ versus time, for an ensemble of simulations with $a$ taking values ranging symmetrically about criticality $a_c \approx 1.8857$ by up to $\Delta{a}=\pm 0.01$:](images/ρ_t_loglog_reduced.png)

The `lvn` Langevin integrator employs the operator-splitting method originated largely by [Dornic et al (2005)](references.md). The software tools are implemented as a `pip`-installable Python package with a C++ core, a set of Jupyter notebooks, and related Python scripts.


