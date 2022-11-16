DOC_DIRNAME := 'docs'
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

# rename project and author
@rename project author:
    # replace string "Cleanpython" with {{project}} and "iacopy" with {{author}} in files
    sed -i "" -e s/Cleanpython/"{{project}}"/g -e s/iacopy/"{{author}}"/g docs/conf.py
    sed -i "" s/Cleanpython/"{{project}}"/g docs/index.rst
    sed -i "" s/iacopy/"{{author}}"/g LICENSE

    # Overwrite the default README.md
    echo "# {{project}}\n" > README.md

    # Remove the docs/build directory
    rm -rf docs/build
    # Remove all files from 'docs' directory except index.rst, conf.py, Makefile, and requirements.txt
    find docs -not -name 'index.rst' -not -name 'conf.py' -not -name 'Makefile' -not -name 'requirements.txt' -delete

# add github badges to the readme
@badges username reponame:
    # Generate badges
    echo "[![Testing](https://github.com/{{username}}/{{reponame}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{username}}/{{reponame}}/actions/workflows/ci.yml)" >> README.md
    echo "[![Sphinx build](https://github.com/{{username}}/{{reponame}}/actions/workflows/sphinx.yml/badge.svg)](https://github.com/{{username}}/{{reponame}}/actions/workflows/sphinx.yml)" >> README.md
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

# get the latest versions of the installed libraries and update requirements.txt
up:
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
setenv VIRTUALENV:
    @echo Create virtualenv and use it to install requirements
    virtualenv -p python3 {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m pip install -r requirements.txt
    @echo Now please activate the virtualenv, then call \"just doc\".

@_mypy:
    mypy --ignore-missing-imports src

@_flake8:
    flake8 .

@_pylint:
    pylint src

@_isort:
    isort --check-only --recursive --quiet . || just _fail "Fix imports by calling \'just fix\'."

@_black:
    black --check -q . || just _fail "Fix code formatting by calling \'just fix\'."

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
    isort .
    black .

# run tests with coverage
@_test-cov:
    pytest --cov --cov-report=xml .

# run tests only (with no coverage and no lint)
@test:
    pytest .

# run tests with coverage.py, create html report and open it
@cov:
    just _test-cov
    coverage html  # create an HTML report
    just _open htmlcov/index.html

# check if coverage satisfies requirements
@_check-cov:
    coverage report --fail-under {{MIN_COVERAGE}}
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
    pytest --benchmark-enable --benchmark-only -k {{K_SELECTOR}} .

# bootstrap documentation (to test the recipe, `rm -rf docs`, then `just doc`)
@_setup-doc:
    echo Setting up documentation...
    sphinx-quickstart --no-sep --ext-autodoc --ext-coverage --ext-todo --ext-viewcode --no-makefile --no-batchfile ./{{DOC_DIRNAME}}

    # uncomment "sys.path.append" line on conf.py and pass "../src" as argument in order to generate the documentation correctly.
    # and fix also index.rst (adding "modules" to the toctree, otherwise the build does not work properly)
    python confix.py

# setup or build and open generated documentation
@_build-doc:
    # Check if setup is needed and call _setup-doc in this case.
    ls ./{{DOC_DIRNAME}}/conf.py || just _setup-doc

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
