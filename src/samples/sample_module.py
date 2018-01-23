"""
Module example to show doctests and documentation results.
"""


def reverse_manually(input_string):
    """Reverse a string slowly
    """
    result = ''
    for char in input_string:
        result = char + result
    return result


def reverse_builtin(input_string):
    """Reverse a string the right way.
    """
    return ''.join(reversed(input_string))


def product_nested_for(dimension_1, dimension_2):
    """
    >>> product_nested_for(3, 6)
    18
    """
    result = 0
    for _ in range(dimension_1):
        for __ in range(dimension_2):
            result += 1
    return result


def product_comprehension(dimension_1, dimension_2):
    """
    >>> product_comprehension(3, 6)
    18
    """
    return sum([1 for _ in range(dimension_1) for __ in range(dimension_2)])
