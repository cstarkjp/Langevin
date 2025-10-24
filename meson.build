#
# Configuration file for Meson build system.
#

project(
    'Langevin',
    'cpp',
    version: '2025.10.23a4',
    default_options: ['cpp_std=c++11'],
)
add_project_arguments(
    '-Ofast', '-g3', 
    # '-Doptimization=3', '-Db_lto=true',
    language : 'cpp',
)

cpp_sources = files(
    'src/langevin_construct_grid.cpp', 
    'src/langevin_construct_grid1d.cpp', 
    'src/langevin_construct_grid2d.cpp', 
    'src/langevin_ic.cpp', 
    'src/langevin_bc.cpp', 
    'src/langevin_prepare.cpp', 
    'src/langevin_integrate_rungekutta.cpp', 
    'src/langevin_integrate_euler.cpp', 
    'src/langevin_utilities.cpp', 
    'src/dp/dplangevin.cpp', 
    'src/dp/sim_dplangevin.cpp', 
    'src/dp/sim_dplangevin_private.cpp', 
    'src/dp/sim_dplangevin_utilities.cpp',
    'src/dp/wrapper_dplvn.cpp'
)
pybind11_dep = dependency('pybind11')

# pure: false <=> package includes compiled binary file
py = import('python').find_installation(pure: false)

py.extension_module(
    'dplvn',
    cpp_sources,
    install: true,
    dependencies : [pybind11_dep],
    subdir: 'lvn/dp'
)

# Install Python source files
py.install_sources(
    [
        'python/__init__.py', 
    ],
    subdir: 'lvn'
)
py.install_sources(
    [
        'python/dp/__init__.py', 
        'python/dp/ensemble.py', 
        'python/dp/file.py', 
        'python/dp/image.py', 
        'python/dp/initialize.py', 
        'python/dp/plot.py', 
        'python/dp/simulation.py', 
        'python/dp/utils.py', 
    ],
    subdir: 'lvn/dp'
)

# # Example of making version available for configuration
# conf_data = configuration_data()
# conf_data.set('VERSION', meson.project_version()) # Get version from project() call
# configure_file(output: 'config.h', configuration: conf_data, install: true)