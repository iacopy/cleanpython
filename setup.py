# Standard Library
from distutils.core import setup

# 3rd party
from Cython.Build import cythonize

setup(
    name='CleanProject',
    # cythonize all pyx files inside `src`
    ext_modules=cythonize('src/**/*.pyx'),
)
