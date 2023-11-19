"""
Basic tests for foobar, using pytest.parametrize.
"""

# 3rd party
import pytest

# My stuff
from cleanpython import foobar


def test_sum_two_numbers():
    """
    Test sum_two_numbers function.
    """
    assert foobar.sum_two_numbers(1, 2) == 3


@pytest.mark.parametrize("num_1, num_2, expected", [(1, 2, 3), (2, 3, 5)])
def test_sum_two_numbers_parametrized(num_1, num_2, expected):
    """
    Test sum_two_numbers function with parameters.
    """
    assert foobar.sum_two_numbers(num_1, num_2) == expected
