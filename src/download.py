"""
Utility module.
"""
# Standard Library
import logging
import os
import re
import urllib.request


def get_title(path: str) -> str:
    """
    Get title from file.

    >>> get_title("tests/data/Wojciech_Fibak")
    'Wojciech Fibak - Wikipedia'
    """
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return match[1] if (match := re.search("<title>(.*)</title>", content)) else ""


def download(url: str, path: str) -> tuple:
    """
    Download file from url to path.
    """
    dest = os.path.join(path, url.split("/")[-1])
    logging.debug("Downloading %s to %s", url, dest)
    urllib.request.urlretrieve(url, dest)
    logging.info("Downloaded %s to %s", url, dest)

    title = get_title(dest)
    logging.debug("Title: %s", repr(title))
    return title, dest
