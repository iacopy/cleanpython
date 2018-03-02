# Standard Library
import os
from types import SimpleNamespace
from unittest import mock

# 3rd party
import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import array_shapes

# My stuff
from puzzle import rand_puzzle
from puzzle import util

TEST_IMAGE = './tests/puzzle/wrgb.png'


@given(shape=array_shapes(min_dims=2, max_dims=2))
def test_rand_cell(shape):
    height, width = rand_puzzle.rand_cell(shape)
    assert height < shape[0]
    assert width < shape[1]


def test_random_puzzle():
    """
    Test randomize array with 2 swaps and mocked
    random calls.
    """
    ary = np.array(
        [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ]
    )

    with mock.patch('puzzle.rand_puzzle.rand_cell') as get_rand_cell:
        get_rand_cell.side_effect = [
            (0, 0), (1, 1),
            (0, 1), (0, 0),
        ]
        rand_puzzle.random_puzzle(ary, 2, 2)

    expected = [
        [2, 3, 10, 11],
        [6, 7, 14, 15],
        [8, 9, 0, 1],
        [12, 13, 4, 5],
    ]
    assert ary.tolist() == expected


def test_main():
    dst = 'testout.png'
    original = util.load_image_as_grayscale(TEST_IMAGE)
    assert original.tolist() == [
        [255, 255, 76, 76],
        [255, 255, 76, 76],
        [149, 149, 29, 29],
        [149, 149, 29, 29],
    ]

    with mock.patch('puzzle.rand_puzzle.rand_cell') as get_rand_cell:
        get_rand_cell.side_effect = [
            [0, 1], [1, 0],
            [0, 0], [1, 1],
        ]
        rand_puzzle.main(
            SimpleNamespace(
                src=TEST_IMAGE,
                cells='2x2',
                swaps=2,
                dst=dst,
                # default
                cell_size='auto',
                pixel=False
            )
        )

    ary = util.load_image_as_grayscale(dst)
    expected = [
        [29, 29, 149, 149],
        [29, 29, 149, 149],
        [76, 76, 255, 255],
        [76, 76, 255, 255],
    ]
    assert ary.tolist() == expected

    # cleanup artifacts
    os.remove(dst)


def test_main_random():
    """
    This test was created to cover the non-squared ``cell_size`` option branch.

    TODO: add more detailed checks.
    """
    dst = 'testout.png'

    rand_puzzle.main(SimpleNamespace(
        src=TEST_IMAGE,
        cell_size='1x2',
        # default
        dst=dst,
        cells='auto',
        swaps=0,
        pixel=False,
    ))

    # cleanup artifacts
    os.remove(dst)
