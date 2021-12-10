"""
By counting the number of differences between two homologous DNA strands
taken from different genomes with a common ancestor, we get a measure of
the minimum number of point mutations that could have occurred on the
evolutionary path between the two strands.

This is called the 'Hamming distance'.
"""

from cpython cimport array
import array


def calculate_pure(seq_1, seq_2):
    """
    Calculate Hamming distance between `seq_1` and `seq_2`.

    Non-pythonic implementation, without type annotation.
    """
    result = 0
    length = len(seq_1)
    for i in range(length):
        el_1 = seq_1[i]
        el_2 = seq_2[i]
        if el_1 != el_2:
            result += 1
    return result


def calculate_c_1(seq_1, seq_2):
    """
    Calculate Hamming distance between `seq_1` and `seq_2`.

    Not really optimized (range(len(seq_1))).
    """
    cdef int result = 0
    cdef int i
    # cdef int length = len(seq_1)
    for i in range(len(seq_1)):
        el_1 = seq_1[i]
        el_2 = seq_2[i]
        if el_1 != el_2:
            result += 1
    return result

def calculate_c_2(list seq_1, list seq_2):
    """
    Calculate Hamming distance between `seq_1` and `seq_2`.

    c-style, with annotation (however, not completely optimized).
    """
    cdef int result = 0
    cdef int i = 0
    cdef int length = len(seq_1)
    while i < length:
        el_1 = seq_1[i]
        el_2 = seq_2[i]
        if el_1 != el_2:
            result += 1
        i += 1
    return result
