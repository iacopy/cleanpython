"""
Benchmark tests.
"""
# Standard Library
import string

# 3rd party
import pytest  # type: ignore

# My stuff
from samples import sample_module


@pytest.mark.benchmark(group='product')
def test_nested_for_benchmarks(benchmark):
    """
    Benchmark a product performance made by using a nested for.
    """
    result = benchmark(sample_module.product_nested_for, 100, 10000)
    assert result == 1e6


@pytest.mark.benchmark(group='product')
def test_comprehension_benchmarks(benchmark):
    """
    Benchmarch a product by using list comprehension.
    """
    result = benchmark(sample_module.product_comprehension, 100, 10000)
    assert result == 1e6


@pytest.mark.benchmark(group='reverse')
def test_reverse_manually(benchmark):
    """
    Just launch benchmark on the manual reverse function.
    """
    benchmark(sample_module.reverse_manually, string.printable * 100)


@pytest.mark.benchmark(group='reverse')
def test_reverse_builtin(benchmark):
    """
    Just launch benchmark on the builtin reverse function.

    Do not check that result is correct! In general that's no good.
    """
    benchmark(sample_module.reverse_builtin, string.printable * 100)
