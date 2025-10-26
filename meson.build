#
# Configuration file for Meson build system.
#

project(
    'Langevin',
    'cpp',
    version: '2025.10.25a1',
    default_options: ['cpp_std=c++11'],
)
add_project_arguments(
    '-Ofast', '-g3', 
    # '-Doptimization=3', '-Db_lto=true',
    language : 'cpp',
)

cpp_sources = files(
    'cplusplus/langevin_construct_grid.cpp', 
    'cplusplus/langevin_construct_grid1d.cpp', 
    'cplusplus/langevin_construct_grid2d.cpp', 
    'cplusplus/langevin_ic.cpp', 
    'cplusplus/langevin_bc.cpp', 
    'cplusplus/langevin_prepare.cpp', 
    'cplusplus/langevin_integrate_rungekutta.cpp', 
    'cplusplus/langevin_integrate_euler.cpp', 
    'cplusplus/langevin_utilities.cpp', 
    'cplusplus/dp/dplangevin.cpp', 
    'cplusplus/dp/sim_dplangevin.cpp', 
    'cplusplus/dp/sim_dplangevin_private.cpp', 
    'cplusplus/dp/sim_dplangevin_utilities.cpp',
    'cplusplus/dp/wrapper_dplvn.cpp'
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
        'python/file.py', 
        'python/image.py', 
        'python/initialize.py', 
        'python/serialize.py', 
        'python/utils.py', 
        'python/viz.py', 
    ],
    subdir: 'lvn'
)
py.install_sources(
    [
        'python/dp/__init__.py', 
        'python/dp/ensemble.py', 
        'python/dp/simulation.py', 
        'python/dp/title.py', 
        'python/dp/vizdp.py', 
    ],
    subdir: 'lvn/dp'
)

# # Example of making version available for configuration
# conf_data = configuration_data()
# conf_data.set('VERSION', meson.project_version()) # Get version from project() call
# configure_file(output: 'config.h', configuration: conf_data, install: true)