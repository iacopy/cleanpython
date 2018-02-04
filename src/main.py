"""
Just import things.
"""

# Standard Library
import sys

# My stuff
from samples import sample_module

if __name__ == '__main__':  # pragma: no cover
    print(sample_module.reverse_manually(sys.argv[1]))
