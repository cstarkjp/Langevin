# Testing

A simple demo of `langevin.dplvn` integration of a directed-percolation Langevin equation
 is provided in the Python script:

    python dp_periodic.py

This script runs a short simulation on a small rectangular 2D grid with periodic edge topology (aka a toroidal grid) and
floating boundary conditions. The grid-averaged mean density 
is written out as a time series into a text file named "solution.txt" for 
all simulation time steps ("epochs"). 
Time slices of the density grid are printed for selected epochs.

A second demo shows how to simulate a 2d grid with both periodic and bounded
grid edge topologies (aka a cylindrical grid) and mixed boundary conditions 
(constant flux b.c.s along the bounded edges):

    python dp_mixed.py

The following Jupyter notebook has cells that do both of the above and more
(just uncomment/comment out as needed):

    ipython DP.ipynb  

In this notebook, the final density grid is rendered as an image, and the mean-density time series is graphed. Both plots are exported to PNG files. 


If you build from source, and don't install `langevin` in the Python environment's standard package path, you will need to point Python to this local build. 
Uncomment the following lines in the demo scripts/notebook:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.pardir, "build"))

and check that Python can find your local copy of the `langevin` package:

    import langevin
    print(langevin.__file__)
