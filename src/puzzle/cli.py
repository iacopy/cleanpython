"""
Handles cli.
"""
# Standard Library
import argparse

# 3rd party
import numpy as np

DESCRIPTION = """Create a random puzzle from an image.
Subdivides the image in rectangles than swaps them randomly.
"""
EPILOG = 'NB: if `pixel` is active it has the priority'


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


def parse_size_str(size_str):
    """
    >>> parse_size_str('2x5')
    (2, 5)
    """
    return tuple(map(int, size_str.split('x')))


def calc_cells_and_cell_size(options, shape):
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


def process_options(options, shape=None):
    """
    Process cli options to get 4 parameters:
        * src -- image source
        * cell_size -- number of cells size in pixel
        * swaps -- number of random cells swaps
        * dst -- destination file
    """
    cells, cell_size = calc_cells_and_cell_size(options, shape)

    if options.pixel:
        # overwrite everything and use a cell per pixel
        cell_size = 1, 1

    swaps = options.swaps if options.swaps else np.prod(cells)
    return cell_size, swaps


def get_options():  # pragma: no cover
    """
    Parse arguments from command line.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument('src', help='src image path')
    parser.add_argument('-o', '--dst', default='outputzzle.png',
                        help='output image path [default: %(default)s]')
    parser.add_argument('-c', '--cells', default='auto',
                        help='number of cells (e.g. "3x3") [default: %(default)s]')
    parser.add_argument('--swaps', default=0,
                        help='number of swaps (0 = auto) [default=%(default)s]')
    parser.add_argument('--cell-size', type=str, default='auto',
                        help='cell size in pixel (e.g. "1x1") [default: %(default)s]')
    parser.add_argument('--pixel', action='store_true',
                        help='treat each pixel as a cell [default: %(default)s]')
    options = parser.parse_args()
    return options
