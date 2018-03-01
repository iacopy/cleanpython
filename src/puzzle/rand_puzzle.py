"""
Functions to randomize puzzles
and save them to disk.

Usage::

    python -m src.puzzle.rand_puzzle <image_file_path>
"""
# 3rd party
import numpy as np
from PIL import Image

from .cli import get_options
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


def process_options(options, shape=None):
    """
    Process cli options to get 4 parameters:
        * src -- image source
        * cell_size -- number of cells size in pixel
        * swaps -- number of random cells swaps
        * dst -- destination file
    """
    def parse_size_str(size_str):
        """
        >>> parse_size_str('2x5')
        (2, 5)
        """
        return tuple(map(int, size_str.split('x')))

    def calc_cells_and_cell_size(options):
        """
        Get ``cells`` and ``cell_size`` from options.

        Normally ``cell_size`` is calculated from ``cells``, knowing the image size.
        But if you explicitly set the ``cell_size``, it takes priority.
        """
        if options.cell_size != 'auto':
            assert options.cells == 'auto', 'Error: forbidden to specify both cells and cell_size'
            cell_size = parse_size_str(options.cell_size)
            cells = int(shape[0] / cell_size[0]), int(shape[1] / cell_size[1])
        else:
            cells = options.cells if options.cells != 'auto' else '3x3'
            cells = parse_size_str(cells)
            cell_size = get_cell_size(shape, cells)
        return cells, cell_size

    cells, cell_size = calc_cells_and_cell_size(options)

    if options.pixel:
        # overwrite everything and use a cell per pixel
        cell_size = 1, 1

    swaps = options.swaps if options.swaps else np.prod(cells)
    return cell_size, swaps


def main(options):
    """
    Create a random puzzle from a source image.
    """
    ary = load_image(options.src)

    cell_size, swaps = process_options(options, shape=ary.shape)

    # Let's avoid "ValueError: assignment destination is read-only"
    ary.flags['WRITEABLE'] = True

    if cell_size[0] != cell_size[1]:
        print('Warning: non-squared cell size not yet supported. Using ({0}, {0})'.format(
            cell_size[0]))
    random_puzzle(ary, cell_size[0], swaps)

    save_image(ary, options.dst)


if __name__ == '__main__':
    main(get_options())
