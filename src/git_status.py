#!/usr/bin/env python
"""
With arguments ask if git status is exactly mathes the query,
else prints status and returns 0 exit code only in case of
no files in index nor untracked.
"""
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List

ST_CLEAN = 'clean'
ST_INDEX = 'index'
ST_DIRTY = 'dirty'
EXIT_DICT = {ST_CLEAN: 0, ST_INDEX: 1, ST_DIRTY: 2}


def get_git_status() -> Dict[str, List[str]]:
    """
    Call git status and parse results in a dictionary.
    """
    result = defaultdict(list)  # type: dict
    output_lines = subprocess.check_output(
        ['git', 'status', '--porcelain']).decode('utf-8').splitlines()
    for line in output_lines:
        index, worktree, filename = line[0].strip(), line[1].strip(), line[3:]
        if index:
            result['index'].append(filename)
        if worktree:
            result['worktree'].append(filename)
    return dict(result)


def str_status(git_status: Dict[str, List[str]]) -> str:
    """
    Return a string ('clean', 'index' or 'dirty') as a
    syntesis of git status.

    >>> str_status({})
    'clean'
    >>> str_status({'worktree': ['foo']})
    'dirty'
    >>> str_status({'index': ['a', 'b', 'c']})
    'index'

    """
    if not git_status:
        return ST_CLEAN

    worktree = git_status.get('worktree')
    index = git_status.get('index')
    if worktree:
        return ST_DIRTY
    assert index, 'Programming error: index should be not empty but it is'
    return ST_INDEX


def main(args: List[str]) -> int:
    """
    Call git status and convert it as an exit code.

    0 = clean: worktree and index both empty
    1 = index: index not empty and worktree empty
    2 = dirty: worktree not empty

    With arguments, return 0 only in case of status matches the query.
    Allowed queries: 'clean', 'index' or 'dirty'.
    """
    status = str_status(get_git_status())
    query = args[0] if args else ''
    if query:
        # Return 0 if status matches the query, 1 otherwise
        return int(query != status)

    # print status and return the exit code related to the status
    # Handle verbosity?
    print(status)
    return EXIT_DICT[status]


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
