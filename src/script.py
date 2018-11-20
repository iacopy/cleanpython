"""
A script to use stuff.
"""
# My stuff
from samples import sample_module
from samples import uselib

print(sample_module.reverse_manually('HELLO'))
assert uselib.use(1, 1) == 2, "FAIL: could not use functions inside mylib package"

print("Everything is ok.")
