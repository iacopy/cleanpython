cdef int product_cycle(int x, int y):
    """
    Just a sample function in cython.
    """
    cdef int result = 0
    cdef int i, j
    for i in range(y):
        for j in range(x):
            result += 1
    return result
