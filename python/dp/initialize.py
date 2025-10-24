"""
Configure to run in `IPython`_.

---------------------------------------------------------------------

Sets up `IPython`_ environment if we're running
in a `Jupyter notebook`_ or `Jupyter QtConsole`_.

 - prepares Matplotlib to display inline and (for Macs)
   at a 'retina' resolution -- if this
   is not available, a benign error report (currently disabled)
   is made and progress continues
 - enables automatic reloading (in case the code has been modded) 
   when a notebook is re-run in-situ

---------------------------------------------------------------------

Requires `Matplotlib`_ and `IPython`_.

Uses IPython extensions `autoreload`_.

The  `autoreload`_ extension forces the parent package to be reloaded on
restart. This makes code modding and subsequent rerunning of a notebook
smooth and seamless. It is not needed for normal operation, and if
unavailable processing continues regardless.

---------------------------------------------------------------------

.. _Matplotlib: https://matplotlib.org/
.. _autoreload:
    https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html
.. _IPython: https://ipython.readthedocs.io/en/stable/
.. _Jupyter notebook: https://jupyter-notebook.readthedocs.io/en/stable/
.. _Jupyter QtConsole: https://qtconsole.readthedocs.io/en/stable/
"""

# Jupyter `%magic` commands `%load_ext`, `%aimport`, and `%autoreload`
#  are needed here to force the notebook to reload the package,
#  and its constituent modules, as changes are made to it.
# Force module to reload

# https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.getipython.html
# <ipython-input-2-5aa624c5c899>:1:   
#    DeprecationWarning: `magic(...)` is deprecated since IPython 0.13 
#    (warning added in 8.1), use run_line_magic(magic_name, parameter_s).

from IPython import get_ipython #type: ignore

def check_is_ipython() -> bool:
    """Check if we are running an IPython kernel from Jupyter etc."""
    try:
        if "IPKernelApp" not in get_ipython().config:   #type: ignore
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True

if check_is_ipython():
    try:
        get_ipython().run_line_magic(  #type: ignore
            "config", 
            "InlineBackend.figure_format = 'retina'",
        )
        # print("Retina backend enabled")
    except NameError:
        # print("Retina backend not enabled")
        pass

    try:
        get_ipython().run_line_magic("matplotlib", "inline",) #type: ignore
    except NameError:
        pass


    try:
        get_ipython().run_line_magic("load_ext", "autoreload",) #type: ignore
        get_ipython().run_line_magic("autoreload", "2",) #type: ignore
    except NameError as error:
        print(
            "Error trying to invoke get_ipython(), "
            + "possibly because not running IPython:",
            error,
        )
    # except:
    #     print('Possibly benign error trying to config autoreload')
