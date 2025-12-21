#
# Configuration file for Meson build system.
#

project(
    'Langevin',
    'cpp',
    version: '2025.12.21a1',
    default_options: ['cpp_std=c++11'],
)
add_project_arguments(
    '-Ofast', '-g3', 
    # '-Doptimization=3', '-Db_lto=true',
    language : 'cpp',
)

cpp_sources = files(
    'cplusplus/core/langevin_construct_grid.cpp', 
    'cplusplus/core/langevin_construct_grid1d.cpp', 
    'cplusplus/core/langevin_construct_grid2d.cpp', 
    'cplusplus/core/langevin_ic.cpp', 
    'cplusplus/core/langevin_bc.cpp', 
    'cplusplus/core/langevin_prepare.cpp', 
    'cplusplus/core/langevin_integrate_rungekutta.cpp', 
    'cplusplus/core/langevin_integrate_euler.cpp', 
    'cplusplus/core/langevin_utilities.cpp', 
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
    subdir: 'langevin/dp'
)

# Install Python source files
py.install_sources(
    [
        'python/__init__.py', 
    ],
    subdir: 'langevin'
)
py.install_sources(
    [
        'python/base/__init__.py', 
        'python/base/file.py', 
        'python/base/initialize.py', 
        'python/base/serialize.py', 
        'python/base/utils.py', 
        'python/base/viz.py', 
    ],
    subdir: 'langevin/base'
)
py.install_sources(
    [
        'python/dp/__init__.py', 
        'python/dp/ensemble.py', 
        'python/dp/simulation.py', 
        'python/dp/vizdp.py', 
    ],
    subdir: 'langevin/dp'
)

# # Example of making version available for configuration
# conf_data = configuration_data()
# conf_data.set('VERSION', meson.project_version()) # Get version from project() call
# configure_file(output: 'config.h', configuration: conf_data, install: true)