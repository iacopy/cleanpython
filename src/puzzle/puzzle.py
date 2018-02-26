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
    row_0 = range(cell_0[0] * size, cell_0[0] * size + size)
    col_0 = range(cell_0[1] * size, cell_0[1] * size + size)
    row_1 = range(cell_1[0] * size, cell_1[0] * size + size)
    col_1 = range(cell_1[1] * size, cell_1[1] * size + size)

    for y_0, y_1 in zip(row_0, row_1):
        for (x_0, x_1) in zip(col_0, col_1):
            # could not managed to do it without tmp
            tmp = copy(ary[y_0][x_0])
            ary[y_0][x_0] = ary[y_1][x_1]
            ary[y_1][x_1] = tmp
