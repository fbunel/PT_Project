from distutils.core import setup
from Cython.Build import cythonize

setup(
            ext_modules = cythonize("Lattice.pyx")
            )
setup(
            ext_modules = cythonize("MonteCarlo.pyx")
            )
