# CleanPython

[![Testing](https://github.com/iacopy/cleanpython/actions/workflows/ci.yml/badge.svg)](https://github.com/iacopy/cleanpython/actions/workflows/ci.yml)
[![pages-build-deployment](https://github.com/iacopy/cleanpython/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/iacopy/cleanpython/actions/workflows/pages/pages-build-deployment)
[![Maintainability](https://api.codeclimate.com/v1/badges/142fbb415a2d6f66b804/maintainability)](https://codeclimate.com/github/iacopy/cleanpython/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/142fbb415a2d6f66b804/test_coverage)](https://codeclimate.com/github/iacopy/cleanpython/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A [Python3](https://docs.python.org/3/) project model with several useful, standard
and integrated tools to help you write clean, tested code by following
the [Zen of Python](#zen-of-python).

If you start a Python project from scratch and need to write solid, tested, clean code, this repository might help.

What is the *clean* code, and why is this important?
Read [here](https://www.butterfly.com.au/blog/website-development/clean-high-quality-code-a-guide-on-how-to-become-a-better-programmer).

## Integrated tools

- [Pytest](https://docs.pytest.org)
    - useful to write data-driven tests, in a straightforward way and with less boilerplate
    - [pytest-benchmark](http://pytest-benchmark.readthedocs.io/en/latest/) makes easy to compare different functions performances

- [Hypothesis](https://hypothesis.readthedocs.io)
    - \"property based testing\"
    - really useful to find unexpected edge cases to test
    - NB: no test examples, so far, in this repo

- [Mypy](http://mypy.readthedocs.io)
    - static type checker for Python
    - helps to find hidden bugs before they come up

- [Coverage.py](http://coverage.readthedocs.io)
    - tells you which lines and branches are executed
    - a 100% coverage should be the *minimal* quality requirement

- [Pylint](https://www.pylint.org)
    - the most complete Python linter
    - with several complexity metrics, it\'s useful to keep your code clean, simple and readable
    - can catch even duplicate code in different files! 🙌
    - helps you to start refactoring before your code becomes too messy

- [Ruff](https://github.com/astral-sh/ruff): an extremely fast Python linter and code formatter, written in Rust. Ruff can be used to replace Flake8 (plus dozens of plugins), Black, isort, pydocstyle, pyupgrade, autoflake, and more, all while executing tens or hundreds of times faster than any individual tool.
    - ⚡️ 10-100x faster than existing linters (like Flake8) and formatters (like Black)
    - 🐍 Installable via pip
    - 🛠️ pyproject.toml support
    - 🤝 Python 3.13 compatibility
    - ⚖️ Drop-in parity with Flake8, isort, and Black
    - 📦 Built-in caching, to avoid re-analyzing unchanged files
    - 🔧 Fix support, for automatic error correction (e.g., automatically remove unused imports)
    - 📏 Over 800 built-in rules, with native re-implementations of popular Flake8 plugins, like - flake8-bugbear
    - ⌨️ First-party editor integrations for VS Code and more
    - 🌎 Monorepo-friendly, with hierarchical and cascading configuration

- [MkDocs](https://www.mkdocs.org/)
    - generates html documentation

- [Pip-tools](https://github.com/jazzband/pip-tools/)
    - Simplifies updating requirements.
    - `pip-compile requirements.in` generates requirements.txt
    - `pip-sync` installs from requirements.txt
    - You can also have dev-requirements if you want

- [just](https://github.com/casey/just)
    - rules them all together in your workflow
    - `just check` to make sure everything is OK
    - `just cov` creates an HTML coverage report
    - `just doc` generates your documentation

## Requirements

- [Git](https://git-scm.com)
- [Python3](https://docs.python.org/3/)
- [just](https://github.com/casey/just)

## Usage

### Use this template

First method (recommended): click on `Use this template` button to start a new repository with the CleanPython template.
Then rename the project strings to your own name using the `just rename` command:

    just rename <project-name> <author>

Alternatively, you clone the repository or download the archive and extract it in your project. Then initialize the git repo:

    just init <project-name> <author>

It will create the first commit with the skeleton files.

### First step

First installation from scratch (assume python virtualenv active):

    just install  # install dependencies and check everything is ok

Optionally, you can also install the git hooks (further automatic
checks, pedantic):

    just install-hooks

To install hook to check code when commit:

    just ruff-hook

### Badges

If you want to add badges to your project associated with the actions setup in `.github/workflows`, you can use the following command:

    just badges <repo-name> <username>

This adds three badges to the README.md file. Then commit and push the changes.

To setup GitHub Pages, you have to create a branch named `gh-pages` and push it to the remote repository.

### Minimal workflow

1. write tests first
    ([TDD](https://en.wikipedia.org/wiki/Test-driven_development))
2. write code until tests pass
3. add your files to git index (e.g. `git add -u`)
4. `just commit <your commit message>`

When you launch `just commit`, your whole code base is statically checked and tested
before actually committing it. In case of any failure, the commit is aborted.

To embed this check directly in git: `just install-hooks`
(this could be fairly extreme, so these hooks are not installed by default).

For example:

- are there broken tests? Fail.
- are you trying to get away without writing tests? Fail.
- does your function is too long? Fail.
- does your class contain too many methods or attributes? Fail.
- does your code is too complex? Fail.
- does your code follow a random style? Fail.

You don\'t want to waste time committing broken code, isn\'t it?

The time you don't spend writing tests will be lost later when bugs show up, with customer emails, and in the debugging phase.

Prevention is better than cure.

### Recipes

Make a complete code checkup (lint, test, and coverage):

    just check

Run tests without the coverage.py overhead:

    just test

Create and open your HTML test coverage:

    just cov

Static code analysis (included in `just check`):

    just lint

Automatically fix the coding style:

    just fix

Update dependencies and config files:

    just up

Create your HTML documentation:

    just doc

Deploy your documentation online to GitHub Pages:

    just doc-deploy

Run benchmarks (you have to write down them before :) ):

    just benchmarks

Remove build artifacts (i.e. all untracked files, pay attention!):

    just clean

## Zen of Python

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
