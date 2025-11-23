
"""!
@file test_langevin_version.py
@brief Unit test Langevin package version number.
"""

import unittest
import langevin
import os
import sys
# lvn_dir = os.path.abspath("C:\hostedtoolcache\windows\Python\3.14.0\x64\Lib\site-packages\langevin")
dp_dir = os.path.abspath("C:\hostedtoolcache\windows\Python\3.14.0\x64\Lib\site-packages\langevin\dp")
if sys.platform == "win32" and os.path.exists(dp_dir):
    os.add_dll_directory(dp_dir)
    # os.add_dll_directory(lvn_dir)

class TestLangevinVersion(unittest.TestCase):

    def test_langevin_version(self):
        self.assertIn("__version__", langevin.__dict__)
        print(f"langevin version:  {langevin.__version__}")

if __name__ == '__main__':
    unittest.main()