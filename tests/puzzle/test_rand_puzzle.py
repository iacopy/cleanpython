# Standard Library
import os
from types import SimpleNamespace
from unittest import mock

# 3rd party
import numpy as np
import pytest
from hypothesis import given
from hypothesis.extra.numpy import array_shapes

# My stuff
from puzzle import rand_puzzle

TEST_IMAGE = './tests/puzzle/wrgb.png'


def test_load_image_grayscale():
    """
    Test png image loading with conversion to grayscale.

    Load a 4 x 4 RGB(A) image with 2x2 subcells like this
    [WHITE][RED]
    [GREEN][BLUE]

    Test exact values.
    """
    ary = rand_puzzle.load_image_as_grayscale(TEST_IMAGE)
    assert ary.shape == (4, 4)
    assert ary.tolist() == [
        [255, 255, 76, 76],
        [255, 255, 76, 76],
        [149, 149, 29, 29],
        [149, 149, 29, 29],
    ]


def test_load_image_rgba():
    """
    Test png image loading to numpy array.
    """
    ary = rand_puzzle.load_image(TEST_IMAGE)
    assert ary.shape == (4, 4, 4)
    assert ary.tolist() == [
        [[255, 255, 255, 255], [255, 255, 255, 255],
            [255, 0, 0, 255], [255, 0, 0, 255]],
        [[255, 255, 255, 255], [255, 255, 255, 255],
            [255, 0, 0, 255], [255, 0, 0, 255]],
        [[0, 255, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255], [0, 0, 255, 255]],
        [[0, 255, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255], [0, 0, 255, 255]],
    ]


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


@pytest.mark.parametrize('case', [
    {
        'description': 'all auto',
        'options': dict(src='x', cells='auto', cell_size='auto', swaps=0, pixel=False, dst='o'),
        'shape': (10, 10),
        'expected': ((3, 3), 9),
    },
    {
        'description': 'cell_size calculation',
        'options': dict(src='x', cells='4x4', cell_size='auto', swaps=0, pixel=False, dst='o'),
        'shape': (10, 10),
        'expected': ((2, 2), 16),
    },
    {
        'description': 'cells calculation',
        'options': dict(src='x', cells='auto', cell_size='4x4', swaps=0, pixel=False, dst='o'),
        'shape': (10, 10),
        'expected': ((4, 4), 4),
    },
    {
        'description': 'cell_size calculation with given swaps',
        'options': dict(src='x', cells='1x6', cell_size='auto', swaps=1, pixel=False, dst='o'),
        'shape': (12, 12),
        'expected': ((12, 2), 1),
    },
    {
        'description': 'pixel option takes the priority',
        'options': dict(src='x', cells='auto', cell_size='12x34', swaps=3, pixel=True, dst='o'),
        'shape': (400, 600),
        'expected': ((1, 1), 3),
    },
    {
        'description': 'incompatible options',
        'options': dict(src='x', cells='1x6', cell_size='2x2', swaps=1, pixel=False, dst='o'),
        'shape': (1, 1),
        'expected': 'Error: is not possible to specify both cells and cell_size',
    }
], ids=lambda case: case['description'])
def test_process_options(case):
    """
    Test ``process_options`` function.
    """
    options = SimpleNamespace(**case['options'])
    try:
        res = rand_puzzle.process_options(options, shape=case['shape'])
    except AssertionError as err:
        assert str(err) == case['expected']
    else:
        assert res == case['expected']


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
