"""
Test stuff
"""


import pytest  # type: ignore

from samples.module import add


@pytest.mark.parametrize('num_1,num_2,expected', [
    [1, 1, 2],
    [1, 2, 3],
    [-1, 2, 1],
])
def test_add(num_1, num_2, expected):
    """
    Just test add function in different cases
    """
    assert add(num_1, num_2) == expected
