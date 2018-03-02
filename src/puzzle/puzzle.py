"""
Puzzle functions.
"""

# Standard Library
from copy import copy


def swap(ary, size, cell_0, cell_1):
    """
    Given an array `ary`, swap `cell_0` with `cell_1`.
    Each cell is `size` x `size`.
    """
    def iter_row(cell):
        """Return the `cell` row iterator (implicit cell size).
        """
        return range(cell[0] * size, cell[0] * size + size)

    def iter_col(cell):
        """Return the `cell` column iterator (implicit cell size).
        """
        return range(cell[1] * size, cell[1] * size + size)

    for y_0, y_1 in zip(iter_row(cell_0), iter_row(cell_1)):
        for (x_0, x_1) in zip(iter_col(cell_0), iter_col(cell_1)):
            # could not managed to do it without tmp
            tmp = copy(ary[y_0][x_0])
            ary[y_0][x_0] = ary[y_1][x_1]
            ary[y_1][x_1] = tmp
