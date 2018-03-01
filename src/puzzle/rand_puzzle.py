"""
Functions to randomize puzzles
and save them to disk.

Usage::

    python -m src.puzzle.rand_puzzle <image_file_path>
"""
# 3rd party
import numpy as np
from PIL import Image

from . import cli
from .puzzle import swap


def rand_cell(shape):
    """
    Get a random 2D-index given a `shape`.
    """
    row = np.random.randint(0, shape[0])
    column = np.random.randint(0, shape[1])
    return row, column


def random_puzzle(ary, cell_size, swaps):
    """
    Create a random puzzle from an array representing a grayscale image.
    """
    initial_sum = ary.sum()

    subdivided_shape = (
        int(ary.shape[0] / cell_size),
        int(ary.shape[1] / cell_size)
    )

    for i in range(swaps):
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


def main(options):
    """
    Create a random puzzle from a source image.
    """
    ary = load_image(options.src)

    cell_size, swaps = cli.process_options(options, shape=ary.shape)

    # Let's avoid "ValueError: assignment destination is read-only"
    ary.flags['WRITEABLE'] = True

    if cell_size[0] != cell_size[1]:
        print('Warning: non-squared cell size not yet supported. Using ({0}, {0})'.format(
            cell_size[0]))
    random_puzzle(ary, cell_size[0], swaps)

    save_image(ary, options.dst)


if __name__ == '__main__':
    main(cli.get_options())
