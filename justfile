PROJECT_NAME := 'Cleanpython'
AUTHOR := 'iacopy'
DOC_DIRNAME := 'docs'
DOC_LANGUAGE := 'en'
DOC_INIT_VERSION := '0.1'
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

# first time installation to get the new versions of libraries and check everything is ok
@start:
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r update-requirements.txt
    echo "Complete checkup of code: lint and test coverage"
    just check
    echo "Creating documentation of current codebase"
    just doc
    echo "Updating requirements.txt"
    pip freeze > requirements.txt
    echo "Done."
    echo =========================================================================================
    echo "You can now run 'just' to get a list of available recipes."

# install stuff: requirements and git hooks (assume virtualenv activated)
install:
    pip install --upgrade pip
    pip install -r requirements.txt

# update requirements.txt
update:
    pip install --upgrade pip
    pip uninstall -y -r requirements.txt
    pip install -r update-requirements.txt
    pip freeze > requirements.txt
    echo "Remember to commit the updated requirements.txt"

# install pre-commit hooks (just lint) and pre-push hooks (just test)
install-hooks:
    # install pre-commit hook
    echo "just lint" > .git/hooks/pre-commit&&chmod +x .git/hooks/pre-commit

    # install pre-push hook
    echo "just test" > .git/hooks/pre-push&&chmod +x .git/hooks/pre-push

# bootstrap your virtualenv
setup-virtualenv VIRTUALENV:
    @echo Create virtualenv and use it to install requirements
    virtualenv -p python3 {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m pip install -r requirements.txt
    @echo Now please activate the virtualenv, then call \"just doc\".

@_mypy:
    mypy --ignore-missing-imports src
    echo "mypy  : OK ✔️"

@_flake8:
    flake8 .
    echo "flake8: OK ✔️"

@_pylint:
    pylint src
    echo "pylint: OK ✔️"

@_isort:
    isort --check-only --recursive --quiet . || just _fail "Fix imports by calling \'just fix\'."
    echo "isort : OK ✔️"

# statically check the codebase (mypy, flake8, pylint, isort)
@lint:
    just _mypy
    just _flake8
    just _pylint
    just _isort

# auto fix imports and pep8 coding style
@fix:
    isort .
    autopep8 --in-place -r .

# run tests with coverage
@_test-cov:
    pytest --cov --cov-report=xml .

# run tests only (with no coverage and no lint)
@test:
    pytest .

# (run test if no coverage.xml found) create html report and open it
@cov:
    ls coverage.xml || just _test-cov
    coverage html  # create an HTML report
    just _open htmlcov/index.html

# check if coverage satisfies requirements
@_check-cov:
    coverage report --fail-under {{MIN_COVERAGE}}
    echo "Test coverage {{MIN_COVERAGE}}%  : OK ✅"

# complete checkup: code analysis, tests and coverage
@check:
    just lint
    just _test-cov
    just _check-cov
    echo Global quality check: OK ✅

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
    pytest --benchmark-enable --benchmark-only -k {{K_SELECTOR}} .

# bootstrap documentation
@_setup-doc:
    echo Setting up documentation...
    sphinx-quickstart -a "{{AUTHOR}}" -p "{{PROJECT_NAME}}" -v {{DOC_INIT_VERSION}} -l {{DOC_LANGUAGE}} --sep --ext-autodoc --ext-coverage --ext-todo --ext-viewcode --no-makefile --no-batchfile ./{{DOC_DIRNAME}}

    # move conf to main doc directory instead of its "source"
    mv ./{{DOC_DIRNAME}}/source/conf.py ./{{DOC_DIRNAME}}
    @echo NB: please uncomment "sys.path.append" line on conf.py and pass "../src" as argument in order to generate the documentation correctly.
    # TODO: automatize the previous step
    echo Please rename PROJECT_NAME and AUTHOR in \'justfile\' to your project name and author name.

# setup or build and open generated documentation
@_build-doc:
    # Check if setup is needed and call _setup-doc in this case.
    ls ./{{DOC_DIRNAME}}/conf.py || (just _setup-doc && just _exit "Now edit conf.py and recall just doc to build the documentation.")

    echo Auto-generate modules documentation...
    # Positional args from seconds (if any) are paths you want to exclude from docs
    # -f overwrite existing .rst, --private include also "_"-starting attributes.
    sphinx-apidoc -f -o ./{{DOC_DIRNAME}}/ ./src

    echo Building documentation...
    sphinx-build -b html -c ./{{DOC_DIRNAME}} ./{{DOC_DIRNAME}}/ ./{{DOC_DIRNAME}}/build/html -v

# build and open HTML documentation
@doc: _build-doc
    # Open generated doc if possible but without fail otherwise
    just _open {{DOC_DIRNAME}}/build/html/index.html

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
