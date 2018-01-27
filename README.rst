===========
CleanPython
===========

A Python3_ project template with several useful, standard, integrated
batteries included to help you to write clean, tested, quality code.


Requirements
------------

* Git_
* Python3_
* just_


Usage
-----

Setup
~~~~~

::

    $ git clone git@github.com:iacopy/cleanpython.git
    $ mv cleanpython yourprojectname
    $ virtualenv -p python3 ~/.virtualenvs/yourprojectname
    $ source ~/.virtualenvs/yourprojectname/bin/activate
    $ cd yourprojectname
    $ pip install -r requirements.txt

Test setup::

    $ just     # list recipes
    $ just qa  # complete code quality assurance check

Minimal workflow
~~~~~~~~~~~~~~~~

1. write test first (TDD_)
2. write code until test pass
3. add your files to git index
4. ``just commit <your commit message>``

When you ``just commit``, all your codebase is linted and tested before actually commit it.
If any check fail, the commit is aborted. You don't want to commit broken code, isn't it?


Recipes
~~~~~~~

Here are ``just`` recipes that are *not* called automatically
when you call ``just commit`` or ``just qa``.


Create and open your HTML test coverage::

    just coverage

Create your HTML documentation::

    just doc

Run benchmarks (you have to write down them before :) )::

    just benchmarks

Run tests without coverage.py overhead::

    just test

Remove build artifacts::

    just cleanup


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
    - supports plugins
- Sphinx_
    - produce html documentation
    - can auto-extract documentation from your codebase
- just_
    - rules them all together in your workflow
    - `just commit MESSAGE` allows you to commit only clean and tested code


.. _Coverage.py: http://coverage.readthedocs.io
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
