===========
CleanPython
===========

A Python3_ project template with several useful, standard, integrated
batteries included to help you to write clean, tested, quality code.

If you are starting a Python3 project from scratch,
and you need to write robust and clean code,
this repository could help you.

What is and why clean code matters? Read `here`__.

__ CleanCodeArticle_

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

When you launch ``just commit``, all your codebase is linted and tested before actually commit it.

In case of any fail, the commit is aborted.

For example:

* are there broken tests? Fail.
* are you trying to escape by avoiding to write tests? Fail.
* your function is too long? Fail.
* your class contains too much methods or attributes? Fail.
* your code is too complex? Fail.
* your code follows random style? Fail.

You don't want waste time committing broken code, isn't it?

Remember: prevention is better than cure.

Recipes
~~~~~~~

Here are ``just`` recipes that are *not* called automatically
when you call ``just commit`` or ``just qa``.


Run tests without coverage.py overhead::

    just test

Create and open your HTML test coverage::

    just coverage

Create your HTML documentation::

    just doc

Run benchmarks (you have to write down them before :) )::

    just benchmarks

Remove build artifacts::

    just cleanup


Just integrated tools
---------------------

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


.. _CleanCodeArticle: https://www.butterfly.com.au/blog/website-development/clean-high-quality-code-a-guide-on-how-to-become-a-better-programmer
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
