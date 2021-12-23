CleanPython
===========

[![image](https://travis-ci.org/iacopy/cleanpython.svg?branch=master)](https://travis-ci.org/iacopy/cleanpython)
[![Maintainability](https://api.codeclimate.com/v1/badges/142fbb415a2d6f66b804/maintainability)](https://codeclimate.com/github/iacopy/cleanpython/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/142fbb415a2d6f66b804/test_coverage)](https://codeclimate.com/github/iacopy/cleanpython/test_coverage)

A [Python3](https://docs.python.org/3/) project template with several
useful, standard, integrated batteries included to help you to write
clean, tested, quality code, following the [Zen of
Python](#zen-of-python).

If you are starting a Python3 project from scratch, and you need to
write robust and clean code, this repository could help you.

What is and why *clean code* matters? Read
[here](https://www.butterfly.com.au/blog/website-development/clean-high-quality-code-a-guide-on-how-to-become-a-better-programmer).

Requirements
------------

- [Git](https://git-scm.com)
- [Python3](https://docs.python.org/3/)
- [just](https://github.com/casey/just)

Usage
-----

### Setup

For development of CleanPython:

    $ git clone git@github.com:iacopy/cleanpython.git
    $ mv cleanpython yourprojectname

For a normal use for a custom project, just download the zip and use it
as a skeleton.

Create a virtualenv. I suggest to use the fish console with virtualfish.
Otherwise, manually:

    $ virtualenv -p python3 ~/.virtualenvs/yourprojectname
    $ source ~/.virtualenvs/yourprojectname/bin/activate

First installation from scratch (assume to be on the repository root):

    $ just start  # install last versions of requirements and check everything is ok

If something fails, try:

    $ just install  # use freezed requirements that are already checked

Optionally, you can also install the git hooks (further automatic
checks):

    $ just install-hooks

### Minimal workflow

1. write test first
    ([TDD](https://en.wikipedia.org/wiki/Test-driven_development))
2. write code until test pass
3. add your files to git index (e.g. `git add -u`)
4. `just commit <your commit message>`

When you launch `just commit`, all your codebase is linted and tested
before actually commit it.

In case of any fail, the commit is aborted.

For example:

- are there broken tests? Fail.
- are you trying to escape by avoiding to write tests? Fail.
- your function is too long? Fail.
- your class contains too much methods or attributes? Fail.
- your code is too complex? Fail.
- your code follows random style? Fail.

You don\'t want waste time committing broken code, isn\'t it?

Remember: prevention is better than cure.

### Recipes

Make a complete code checkup (lint, test and coverage):

    just check

The following are `just` recipes that are *not* called automatically
when you call `just commit` or `just checkup`.

Run tests without coverage.py overhead:

    just test

Create and open your HTML test coverage:

    just cov

Create your HTML documentation:

    just doc

Run benchmarks (you have to write down them before :) ):

    just benchmarks

Remove build artifacts (i.e. all untracked files, pay attention!):

    just clean

Just integrated tools
---------------------

- [Pytest](https://docs.pytest.org)
  - useful to write data driven tests
  - [pytest-benchmark](http://pytest-benchmark.readthedocs.io/en/latest/) makes easy to compare different functions performances
- [Hypothesis](https://hypothesis.readthedocs.io)
  - \"property based testing\"
  - really useful to find unexpected edge cases to test

- [Mypy](http://mypy.readthedocs.io)
  - tests typing annotations
  - helps to find hidden bugs before they come up
  - NB: still experimental

- [Coverage.py](http://coverage.readthedocs.io)
  - tells you which lines and branches are executed
  - a 100% coverage should be the *minimal* quality requirement

- [Pylint](https://www.pylint.org)
  - the most complete python linter
  - with several complexity metrics it\'s useful to keep your code clean, simple and readable
  - helps you to start refactor before your code become too complex

- [Flake8](http://flake8.readthedocs.io)
  - helps to write standard, clean and documented code
  - wraps pep8, pyflakes, McCabe Complexity analysis
  - supports plugins

- [Sphinx](http://www.sphinx-doc.org/en/stable/)
  - produce html documentation
  - can auto-extract documentation from your codebase

- [just](https://github.com/casey/just)
  - rules them all together in your workflow
  - `just commit MESSAGE` allows you to commit only clean and tested code

Zen of Python
-------------

The highlighted lines are the ones that, mostly, `CleanPython`
(**explicitly** or *implicitly*) tries to help to reach.

1. **Beautiful is better than ugly.**
2. **Explicit is better than implicit.**
3. **Simple is better than complex.**
4. *Complex is better than complicated.*
5. Flat is better than nested.
6. Sparse is better than dense.
7. **Readability counts.**
8. **Special cases aren\'t special enough to break the rules.**
9. *Although practicality beats purity.*
10. **Errors should never pass silently.**
11. *Unless explicitly silenced.*
12. *In the face of ambiguity, refuse the temptation to guess.*
13. *There should be one\-- and preferably only one \--obvious way to do
    it.*
14. Although that way may not be obvious at first unless you\'re Dutch.
15. **Now is better than never.**
16. Although never is often better than *right* now.
17. If the implementation is hard to explain, it\'s a bad idea.
18. If the implementation is easy to explain, it may be a good idea.
19. Namespaces are one honking great idea \-- let\'s do more of those!

### Legend

**bold**: explicitly, strongly targeted by `CleanPython`

*italic*: implicitly or indirectly or weakly targeted by `CleanPython`
