# Standard Library
import os
from unittest import mock

# 3rd party
import numpy as np
import pytest
from hypothesis import given
from hypothesis.extra.numpy import array_shapes

# My stuff
from puzzle import rand_puzzle

TEST_IMAGE = './tests/puzzle/wrgb.png'


def test_load_image():
    """
    Test png image loading with conversion to grayscale.

    Load a 4 x 4 RGB(A) image with 2x2 subcells like this
    [WHITE][RED]
    [GREEN][BLUE]

    Test exact values.
    """
    ary = rand_puzzle.load_image_as_grayscale(TEST_IMAGE)
    assert ary.shape == (4, 4)
    # Test white quadrant (top-left)
    assert ary[:2, :2].tolist() == [[255, 255], [255, 255]]
    # Test red quadrant (top-right)
    assert ary[:2, 2:].tolist() == [[76, 76], [76, 76]]
    # Test green quadrant (bottom-left)
    assert ary[2:, :2].tolist() == [[149, 149], [149, 149]]
    # Test blue quadrant (bottom-right)
    assert ary[2:, 2:].tolist() == [[29, 29], [29, 29]]


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


@pytest.mark.parametrize('data', [
    [[10, 12], [16, 18]],
    [[1, 2, 3, 4]],
    [[1, 2, 3], [4, 5, 6], [255, 0, 255]],
])
def test_save_image(data):
    dst = '--testonly--.png'
    ary = np.array(data, np.uint8)
    rand_puzzle.save_image(ary, dst)
    actual = rand_puzzle.load_image_as_grayscale(dst)
    assert np.array_equal(actual, ary)
    os.remove(dst)


def test_main():
    dst = 'testout.png'
    original = rand_puzzle.load_image_as_grayscale(TEST_IMAGE)
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
        rand_puzzle.main(TEST_IMAGE, (2, 2), n_swaps=2, dst=dst)

    ary = rand_puzzle.load_image_as_grayscale(dst)
    expected = [
        [29, 29, 149, 149],
        [29, 29, 149, 149],
        [76, 76, 255, 255],
        [76, 76, 255, 255],
    ]
    assert ary.tolist() == expected

    # cleanup artifacts
    os.remove(dst)
