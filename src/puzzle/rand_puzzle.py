"""
Functions to randomize puzzles
and save them to disk.

Usage::

    python -m src.puzzle.rand_puzzle <image_file_path>
"""
# Standard Library
import sys

# 3rd party
import numpy as np
from PIL import Image

from .puzzle import swap


def get_cell_size(shape, super_shape):
    """
    Get cell sizes given a desired number of cells.

    >>> get_cell_size((10, 10), (2, 2))
    (5, 5)

    >>> get_cell_size((6, 4), (2, 2))
    (3, 2)

    >>> get_cell_size((5, 5), (2, 2))
    (2, 2)
    """
    y_size = int(shape[0] / super_shape[0])
    x_size = int(shape[1] / super_shape[1])
    return y_size, x_size


def rand_cell(shape):
    """
    Get a random 2D-index given a `shape`.
    """
    row = np.random.randint(0, shape[0])
    column = np.random.randint(0, shape[1])
    return row, column


def random_puzzle(ary, cell_size, n_swaps):
    """
    Create a random puzzle from an array representing a grayscale image.
    """
    initial_sum = ary.sum()

    subdivided_shape = (
        int(ary.shape[0] / cell_size),
        int(ary.shape[1] / cell_size)
    )

    for i in range(n_swaps):
        src_cell = rand_cell(subdivided_shape)
        dst_cell = rand_cell(subdivided_shape)
        swap(ary, cell_size, src_cell, dst_cell)

        assert ary.sum() == initial_sum, \
            'Checksum failed after {} swaps! {} -> {}'.format(
                i + 1, initial_sum, ary.sum())


def load_image_as_grayscale(src):
    """
    Open and convert image to 2D grayscale array.
    """
    image = Image.open(src).convert('L')
    ary = np.asarray(image)
    return ary


def load_image(src):
    """
    Open and convert image to array.
    """
    image = Image.open(src)
    ary = np.asarray(image)
    return ary


def save_image(ary, dst):
    """
    Save an `ary` numpy array image to disk in `dst` file path.
    """
    Image.fromarray(ary).save(dst)


def parse_args(args):
    """
    Simple positional cli argument parser.

    >>> parse_args(['pippo', '4', '6', 'out.png'])
    ('pippo', (4, 4), 6, 'out.png')
    >>> parse_args(['pippo', '4', '6'])
    ('pippo', (4, 4), 6, 'outpuzzle.png')
    >>> parse_args(['pippo', '4'])
    ('pippo', (4, 4), 5, 'outpuzzle.png')
    >>> parse_args(['pippo'])
    ('pippo', (3, 3), 5, 'outpuzzle.png')
    >>> try:
    ...     parse_args([])
    ... except Exception as err:
    ...     print(err)
    Unexpected number of arguments: 0
    """
    sub_shape, n_swaps, dst = (3, 3), 5, 'outpuzzle.png'
    n_args = len(args)
    if n_args == 4:
        src, sub_shape, n_swaps, dst = args[0], (int(args[1]), int(args[1])), int(args[2]), args[3]
    elif n_args == 3:
        src, sub_shape, n_swaps = args[0], (int(args[1]), int(args[1])), int(args[2])
    elif n_args == 2:
        src, sub_shape = args[0], (int(args[1]), int(args[1]))
    elif n_args == 1:
        src = args[0]
    else:
        raise Exception('Unexpected number of arguments: {}'.format(n_args))
    n_swaps = int(n_swaps)
    return src, sub_shape, n_swaps, dst


def main(src, sub_shape=(3, 3), n_swaps=5, dst='outpuzzle.png'):
    """
    Create a random puzzle from a source image.
    """
    ary = load_image(src)

    # Let's avoid "ValueError: assignment destination is read-only"
    ary.flags['WRITEABLE'] = True

    cell_sizes = get_cell_size(ary.shape, sub_shape)
    # do not support different sizes (only squares)
    cell_size = max(cell_sizes)

    random_puzzle(ary, cell_size, n_swaps)

    save_image(ary, dst)


if __name__ == '__main__':
    main(*parse_args(sys.argv[1:]))
