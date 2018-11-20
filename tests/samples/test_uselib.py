"""
Uselib module tests.
"""
# My stuff
from samples import uselib


def test_uselib():
    """test"""
    assert uselib.use(1, 2) == 3
