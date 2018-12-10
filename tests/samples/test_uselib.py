"""
Uselib module tests.
"""
# 3rd party
import pytest

# My stuff
from samples import uselib


def test_uselib():
    """test"""
    assert uselib.use(1, 2) == 3


@pytest.mark.xfail
def test_fail():
    import notexist
    for i in range(notexist.nothing):
        assert i == 0
