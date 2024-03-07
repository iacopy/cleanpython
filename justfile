DOC_DIRNAME := 'site'
VIRTUALENVS_DIR := '~/.virtualenvs'

# Quality requirements
MIN_COVERAGE := '100'

# just list available recipes
@welcome:
    just --list
    echo =========================================================================================
    echo NB: Make sure your virtualenv is activated before using recipes.

# just show the Zen of Python, by Tim Peters
@zen:
    python -m this

# just show the help
@help:
    echo "# INSTALL\n"
    echo "## Install using poetry\n"
    echo "    poetry install"
    echo
    echo "If you only want to install the project’s runtime dependencies:\n"
    echo "    poetry install --only main"
    echo
    echo "Ensure that the locked dependencies in the poetry.lock file are the only ones present in the environment, removing anything that’s not necessary."
    echo "    poetry install --sync"
    echo
    echo "Add dependencies to the current project:\n"
    echo "    poetry add <dependency>"
    echo
    echo "Add a development dependency:\n"
    echo "    poetry add <dependency> --group dev"
    echo
    echo "## Testing and code quality"
    echo
    echo "### Type check and quality check of your code\n"
    echo "    just lint"
    echo
    echo "### Run tests\n"
    echo "    just test"
    echo
    echo "### Run tests with coverage\n"
    echo "    just cov"
    echo
    echo "### Perform a complete checkup\n"
    echo "    just check"
    echo
    echo "### Run benchmarks\n"
    echo "    just benchmarks"
    echo
    echo "### Build documentation\n"
    echo "    just doc"
    echo

# rename project and author (please use lowercase for project name)
@rename project author:
    mv src/cleanpython src/{{project}}
    # replace string "Cleanpython" with {{project}} and "iacopy" with {{author}} in files
    sed -i "" -e s/cleanpython/"{{project}}"/g tests/test_app.py
    sed -i "" -e s/cleanpython/"{{project}}"/g tests/test_foobar.py
    sed -i "" -e s/Cleanpython/"{{project}}"/g -e s/cleanpython/"{{project}}"/g -e s/iacopy/"{{author}}"/g pyproject.toml
    sed -i "" s/"Clean code with batteries included."/"Project description placeholder"/g pyproject.toml
    sed -i "" s/iacopy/"{{author}}"/g LICENSE

    # Overwrite the default docs/index.md
    echo "# {{project}}\n" > docs/index.md
    # Overwrite the default README.md
    echo "# {{project}}\n" > README.md

    # Stage all changes and show them
    git add -u  # add modified files
    git add src/{{project}}  # add renamed folder
    git diff --cached --stat  # show staged files

    echo
    echo 'Suggestion: git commit -m "Rename project to {{project}}"'

# add github badges to the readme
@badges username reponame:
    # Generate badges
    echo "[![Testing](https://github.com/{{username}}/{{reponame}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{username}}/{{reponame}}/actions/workflows/ci.yml)" >> README.md
    echo "[![pages-build-deployment](https://github.com/{{username}}/{{reponame}}/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/{{username}}/{{reponame}}/actions/workflows/pages/pages-build-deployment)" >> README.md

# WARNING! Reset git history, add all files and make initial commit
@ginit:
    # Reset git repo (remove all commits)
    # this is useful when Cleanpython is cloned
    rm -rf .git
    git init
    git branch -m main
    git add .
    git commit -m "Initial commit (based on CleanPython template)"

# first time installation to get the new versions of libraries and check everything is ok
@startup:
    poetry self update
    echo "Get the new versions of libraries and check everything is ok"
    just up
    poetry install
    echo "Complete checkup of code: lint and test coverage"
    just check
    echo "Creating documentation of current codebase"
    just doc
    echo "Done."
    echo "Remember to commit changes."
    echo =========================================================================================
    echo "You can now run 'just' to get a list of available recipes, or 'just help' to get more info."

# install stuff: dependencies (using poetry) and git hooks
install:
    poetry install

# get the latest versions of the installed libraries
up:
    poetry update
    poetry run pylint --generate-rcfile > pylintrc
    @echo "Now you can call `just install`"

# (beta) for VirtualFish: like 'up' but recreate vf virtualenv to remove also old dependencies
vfup projectenv:
    vf deactivate
    vf new {{projectenv}}
    just startup

# install pre-commit hooks (just lint) and pre-push hooks (just test)
install-hooks:
    # install pre-commit hook
    echo "just lint" > .git/hooks/pre-commit&&chmod +x .git/hooks/pre-commit

    # install pre-push hook
    echo "just test" > .git/hooks/pre-push&&chmod +x .git/hooks/pre-push

# bootstrap your virtualenv (deprecated)
setenv VIRTUALENV:
    @echo Create virtualenv and use it to install requirements
    virtualenv -p python3 {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m pip install -r requirements-dev.txt
    @echo Now please activate the virtualenv, then call \"just doc\".

@_mypy:
    poetry run mypy --ignore-missing-imports src

@_flake8:
    poetry run flake8 .

@_pylint:
    poetry run pylint $(git ls-files '*.py') --ignore conf.py

@_isort:
    poetry run isort --check-only --recursive --quiet . || just _fail "Fix imports by calling \'just fix\'."

@_black:
    poetry run black --check -q . || just _fail "Fix code formatting by calling \'just fix\'."

# statically check the codebase (mypy, flake8, pylint, isort)
@lint:
    just _mypy
    echo "mypy  : OK ✅"
    just _flake8
    echo "flake8: OK ✅✅"
    just _pylint
    echo "pylint: OK ✅✅✅"
    just _isort
    echo "isort : OK ✅✅✅ 🍰"
    just _black
    echo "black : OK ✅✅✅ 🍒"

# auto fix imports and pep8 coding style
@fix:
    poetry run isort .
    poetry run black .
    # Re-check code quality
    just lint

# run tests with coverage
@_test-cov:
    poetry run pytest --cov --cov-report=xml .

# run tests only (with no coverage and no lint)
@test:
    poetry run pytest
    echo "Tests: OK ✅✅✅✅"

# run tests with coverage.py, create html report and open it
@cov:
    just _test-cov
    poetry run coverage html  # create an HTML report
    just _open-nofail htmlcov/index.html

# check if coverage satisfies requirements
@_check-cov:
    poetry run coverage report --fail-under {{MIN_COVERAGE}}
    echo "\nTest coverage {{MIN_COVERAGE}}%  : OK ✅✅✅✅✅"

# complete checkup: code analysis, tests and coverage
@check:
    just lint
    just _test-cov
    echo "Tests: OK ✅✅✅✅"
    just _check-cov
    echo Global quality check: OK ⭐️⭐️⭐️⭐️⭐️

# ensure that working tree is clean
@_working-tree-clean:
    git diff-index --quiet HEAD -- || just _fail "The working tree is not clean."

# ensure that git repo is clean for commit
# (contains only staged files in the index, not in the worktree)
@_index-only:
    # Fail if there are untracked files
    git diff-files --quiet --ignore-submodules -- || just _fail "Unstaged changes in index."
    # Fail if the worktree is totally clean (nothing to commit)
    git status -s | grep '^' || just _fail "Nothing to commit."
    echo git-staged files and clean worktree.

# require quality and no garbage in the repo worktree
@_committable: _index-only
    just check
    echo Your code seems committable.

# git commit (only if your code is committable)
@commit MESSAGE: _committable
    git commit -m "{{MESSAGE}}"
    just clean

# check and git push if everything is OK
@push: _working-tree-clean check clean
    git push

# execute benchmarks tests only, in benchmark mode.
@benchmarks K_SELECTOR="test":
    poetry run pytest --benchmark-enable --benchmark-only -k {{K_SELECTOR}} .

# serve HTML documentation
@doc:
    poetry run mkdocs serve

# deploy HTML documentation to github pages
@doc-deploy:
    poetry run mkdocs gh-deploy

# WARNING! Remove untracked stuff (git clean -idx)! Useful to clean artifacts.
clean:
    # NB: after this, you will need to recompile cython files
    # (\"python setup.py install\" or \"just compile\")
    git clean -idx  # '-i' list untracked files and ask for confirmation

# open a file if possible, else print an alert but do NOT fail
@_open-nofail FILE:
    open {{FILE}} || xdg-open {{FILE}} || just _info "Could not open {{FILE}}"

# open a file if possible, else exit with a fail
@_open FILE:
    open {{FILE}} || xdg-open {{FILE}}

# shortcut to exit with a message and error exit code
@_exit MESSAGE:
    echo {{MESSAGE}} && exit 1

# error exit with fail alert message and error exit code
# TODO: decorate with red
@_fail MESSAGE:
    echo FAIL. {{MESSAGE}} && exit 1

@_info MESSAGE:
    echo {{MESSAGE}} && exit 0
