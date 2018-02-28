"""
Handles cli.
"""
# Standard Library
import argparse

DESCRIPTION = """Create a random puzzle from an image.
Subdivides the image in rectangles than swaps them randomly.
"""
EPILOG = 'NB: if `pixel` is active it has the priority'


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
