========
Kooality
========

A python project template with useful batteries included to
help you to write clean, tested, quality code with best practices.

Based on Python3_, Git_ and just_.


Usage
-----

Setup:

- git clone this repository
- setup the virtualenv
    - ``virtualenv -p python3 ~/.virtualenvs/yourprojectname``
    - ``source ~/.virtualenvs/yourprojectname/bin/activate``
    - ``pip install -r requirements.txt``

Minimal workflow:

1. write test first (TDD_)
2. write code until test pass
3. add your files to git index
4. ``just commit "your commit message"``

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

- Pytest_
    - useful to write data driven tests
    - pytest-benchmark_ makes easy to compare different functions performances
- Hypothesis_
    - "property based testing"
    - really useful to find unexpected edge cases to test
- Mypy_
    - tests typing annotations
    - helps to find hidden bugs before they come up
    - NB: still experimental
- Coverage.py_
    - tells you which lines and branches are executed
    - a 100% coverage should be the *minimal* quality requirement
- Pylint_
    - the most complete python linter
    - with several complexity metrics it's useful to keep your code clean, simple and readable
    - helps you to start refactor before your code become too complex
- Flake8_
    - helps to write standard, clean and documented code
    - wraps pep8, pyflakes, McCabe Complexity analysis
    - suports plugins
- Sphinx_
    - produce html documentation
    - can auto-extract documentation from yout codebase
- just_
    - rules them all together in your workflow
    - `just commit MESSAGE` allows you to commit only clean and tested code
- Cython_
    - improve performance by compiling Python code in C


.. _Coverage.py: http://coverage.readthedocs.io
.. _Cython: http://cython.readthedocs.io
.. _Flake8: http://flake8.readthedocs.io
.. _Git: https://git-scm.com
.. _Hypothesis: https://hypothesis.readthedocs.io
.. _just: https://github.com/casey/just
.. _Mypy: http://mypy.readthedocs.io
.. _Pylint: https://www.pylint.org
.. _Pytest-benchmark: http://pytest-benchmark.readthedocs.io/en/latest/
.. _Pytest: https://docs.pytest.org
.. _Python3: https://docs.python.org/3/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _TDD: https://en.wikipedia.org/wiki/Test-driven_development
