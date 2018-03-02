# Standard Library
import os

# 3rd party
import numpy as np
import pytest

# My stuff
from puzzle import util

TEST_IMAGE = './tests/puzzle/wrgb.png'


def test_load_image_grayscale():
    """
    Test png image loading with conversion to grayscale.

    Load a 4 x 4 RGB(A) image with 2x2 subcells like this
    [WHITE][RED]
    [GREEN][BLUE]

    Test exact values.
    """
    ary = util.load_image_as_grayscale(TEST_IMAGE)
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
    ary = util.load_image(TEST_IMAGE)
    assert ary.shape == (4, 4, 4)
    assert ary.tolist() == [
        [[255, 255, 255, 255], [255, 255, 255, 255],
            [255, 0, 0, 255], [255, 0, 0, 255]],
        [[255, 255, 255, 255], [255, 255, 255, 255],
            [255, 0, 0, 255], [255, 0, 0, 255]],
        [[0, 255, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255], [0, 0, 255, 255]],
        [[0, 255, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255], [0, 0, 255, 255]],
    ]


@pytest.mark.parametrize('data', [
    [[10, 12], [16, 18]],
    [[1, 2, 3, 4]],
    [[1, 2, 3], [4, 5, 6], [255, 0, 255]],
])
def test_save_image(data):
    dst = '--testonly--.png'
    ary = np.array(data, np.uint8)
    util.save_image(ary, dst)
    actual = util.load_image_as_grayscale(dst)
    assert np.array_equal(actual, ary)
    os.remove(dst)
