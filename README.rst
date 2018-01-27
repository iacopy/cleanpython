========
Kooality
========

A python project template with useful batteries included to
help you to write clean, tested, quality code with best practices.

Based on ``python3``, ``git`` and ``just``.


Usage
-----

Setup:

- git clone this repository
- setup the virtualenv
    - ``virtualenv -p python3 ~/.virtualenvs/yourprojectname``
    - ``source ~/.virtualenvs/yourprojectname/bin/activate``
    - ``pip install -r requirements.txt``

Minimal workflow:

- coding
- add your files to git index
- ``just commit "your commit message"``

When you ``just commit``, all your codebase is linted and tested before actually commit it.
If any check fail, the commit is aborted. You don't want to commit broken code, isn't it?

Create and open your HTML test coverage::

    just coverage

Create your HTML documentation::

    just doc

Run benchmarks (you have to write down them before :) )::

    just benchmarks


Tools
-----

- pytest
    - useful to write data driven tests
    - pytest-benchmark makes easy to compare different functions performances
- hypothesis
    - "property based testing"
    - really useful to find unexpected edge cases to test
- mypy
    - tests typing annotations
    - helps to find hidden bugs before they come up
    - NB: still experimental
- coverage
    - tells you which lines and branches are executed
    - a 100% coverage should be the *minimal* quality requirement
- pylint
    - the most complete python linter
    - with several complexity metrics it's useful to keep your code clean, simple and readable
    - helps you to start refactor before your code become too complex
- flake8
    - helps to write standard, clean and documented code
    - wraps pep8, pyflakes, McCabe Complexity analysis
    - suports plugins
- sphinx
    - produce html documentation
    - can auto-extract documentation from yout codebase
- just
    - rules them all together in your workflow
    - `just commit MESSAGE` allows you to commit only clean and tested code
- cython
    - improve performance by compiling Python code in C
