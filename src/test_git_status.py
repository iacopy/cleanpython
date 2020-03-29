"""
Test git_status module.
"""
# Standard Library
from unittest import mock

# 3rd party
import pytest  # type: ignore

# My stuff
import git_status


@pytest.mark.parametrize('git_output,args,expected', [
    (b'', [], 0),
    (b'', ['clean'], 0),
    (b'', ['index'], 1),
    (b'', ['dirty'], 1),
    (b'M  foo.txt', [], 1),
    (b'A  foo.txt', [], 1),
    (b'D  foo.txt', [], 1),
    (b'M  foo.txt', ['clean'], 1),
    (b'A  foo.txt', ['dirty'], 1),
    (b'D  foo.txt', ['index'], 0),
    (b'MM foo.txt', [], 2),
    (b' M foo.txt', [], 2),
    (b'?? foo.txt', [], 2),
    (b'MM foo.txt', ['dirty'], 0),
    (b'?? foo.txt', ['dirty'], 0),
    (b' M foo.txt', ['dirty'], 0),
    (b'?? foo.txt', ['clean'], 1),
    (b'?? foo.txt', ['index'], 1),
    (b' M foo.txt', ['index'], 1),
])
def test_main_empty(git_output, args, expected):
    """
    Test git status main function.
    """
    with mock.patch('git_status.subprocess.check_output') as check:
        check.return_value = git_output
        exit_code = git_status.main(args)
    assert exit_code == expected
