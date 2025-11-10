# Build notes

The first build step is to set up a Python environment (see `environment.yml` for  a `conda` install, and refer to `requirements.txt` for a definitive but overly strict list of "dependencies"). 
The second build step uses `meson-python` to compile and link the `C++` source to generate a Python-importable executable, and (optionally) deploy in the usual way as a Python package within that environment.

First step: having cloned the repo, enter the root directory; don't try to build from the `src/` directory.

Second step: build and deploy as a Python package:

    rm -rf build; pip install .

or just build and _not_ deploy:

    rm -rf build; meson setup build; meson compile -C build   

Then, test your build/deployment using the Python script and Jupyter notebook in `tests/`. See the
[README](https://github.com/cstarkjp/Langevin/tree/main/tests/README.md) there for more details. 

If you choose to build the `langevin` package and subsequently use it in-place, without deployment, you will need something like the following in all your Python scripts:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.pardir, "build"))

Here, the assumption is you're running the script from a directory parallel with `build/`, such as in `tests/`.
