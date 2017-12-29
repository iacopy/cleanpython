# just list available recipes
@welcome:
    just --list

# run tests
test:
    pytest

# open coverage html index
coverage: test
    open htmlcov/index.html

# remove artifacts (pyc, __pycache__, coverage stuff)
cleanup:
    rm -rf src/__pycache__
    rm -rf htmlcov
    coverage erase

    # cleanup built documentation
    rm -rf {{DOC_DIRNAME}}/build
