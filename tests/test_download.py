"""
Webtests for the download module.
"""
# Standard Library
import os

# 3rd party
import pytest

# My stuff
import download

TEST_CASES = [
    ("https://en.wikipedia.org/wiki/Wikipedia", "Wikipedia - Wikipedia"),
    (
        "https://en.wikipedia.org/wiki/Ideological_bias_on_Wikipedia",
        "Ideological bias on Wikipedia - Wikipedia",
    ),
]


@pytest.mark.webtest
@pytest.mark.parametrize("url,title", TEST_CASES)
def test_download(tmp_path, url, title):
    """
    Test download function.
    """
    actual_title, dest = download.download(url, tmp_path)
    assert actual_title == title, f"Expected {title}, got {actual_title}"
    assert os.path.exists(dest), f"File {dest} does not exist"
