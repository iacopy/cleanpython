"""
Basic test.
"""
# Standard Library
import os

# 3rd party
import pytest

# My stuff
import foobar


@pytest.mark.integration
@pytest.mark.webtest
def test_main(tmp_path):
    """
    Test main function.
    """
    res = foobar.main(["https://en.wikipedia.org/wiki/Wikipedia"], tmp_path)
    assert len(res) == 1
    title, dest = res[0]
    assert title == "Wikipedia - Wikipedia"
    assert os.path.exists(dest)
