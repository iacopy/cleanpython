PROJECT_NAME = 'Your Project Name'
AUTHOR = 'Your Name'
DOC_DIRNAME = 'docs'
DOC_LANGUAGE = 'en'
DOC_INIT_VERSION = '0.1'
VIRTUALENVS_DIR = '~/.virtualenvs'

# Quality requirements
MIN_COVERAGE = '100'

# just list available recipes
@welcome:
    just --list
    echo =========================================================================================
    echo NB: Make sure your virtualenv is activated before use recipes.

# just show the Zen of Python, by Tim Peters
@zen:
    python -m this

# bootstrap your project
setup VIRTUALENV:
    @echo Create virtualenv and use it to install requirements
    virtualenv -p python3 {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m pip install -r requirements.txt
    @echo Now please activate the virtualenv, then call \"just doc\".

# statically check the codebase (mypy, flake8, pylint, isort)
@lint:
    mypy --ignore-missing-imports src
    echo "mypy  : OK"
    flake8 src
    echo "flake8: OK"
    pylint src
    echo "pylint: OK"
    isort -c -r . || just _fail "fix imports by calling \'just fix\'"
    echo "isort : OK"

# auto fix imports and pep8 coding style
@fix:
    isort -y -r .
    autopep8 --in-place -r .

# run tests with coverage
@_test-cov:
    pytest --cov --cov-report=html

# test and open resulting coverage html index
@cov: _test-cov
    open htmlcov/index.html || xdg-open htmlcov/index.html

# check if coverage satisfies requirements
@_check-cov:
    coverage report --fail-under {{MIN_COVERAGE}}
    echo "test coverage: OK"

# complete checkup: code analysis, tests and coverage
@checkup:
    just lint
    just _test-cov
    just _check-cov
    echo Quality check OK!

# ensure that working tree is clean
@_working-tree-clean:
    python src/git_status.py clean || just _fail "Your working tree is not clean."

# ensure that git repo is clean for commit
# (contains only stuff in the index, not in the worktree)
@_index-only:
    python src/git_status.py index || just _fail "Your working tree is not clean or you don\'t have changes to commit."
    echo git-staged files and clean worktree.

# require quality and no garbage in the repo worktree
@_committable: _index-only
    just checkup
    echo Your code seems committable.

# git commit (only if your code is committable)
@commit MESSAGE: _committable
    git commit -m "{{MESSAGE}}"
    just clean

# check and git push if everything is OK
@push: _working-tree-clean checkup clean
    git push

# execute benchmarks tests only, in benchmark mode.
@benchmarks K_SELECTOR="test":
    pytest --benchmark-enable --benchmark-only -k {{K_SELECTOR}}

# bootstrap documentation
@_setup-doc:
    echo Setting up documentation...
    sphinx-quickstart -a "{{AUTHOR}}" -p "{{PROJECT_NAME}}" -v {{DOC_INIT_VERSION}} -l {{DOC_LANGUAGE}} --sep --ext-autodoc --ext-coverage --ext-todo --ext-viewcode --no-makefile --no-batchfile ./{{DOC_DIRNAME}}

    # move conf to main doc directory instead of its "source"
    mv ./{{DOC_DIRNAME}}/source/conf.py ./{{DOC_DIRNAME}}
    @echo NB: please uncomment "sys.path.append" line on conf.py and pass "../src" as argument in order to generate the documentation correctly.
    # TODO: automatize this step

# setup or build and open generated documentation
@doc:
    # Check if setup is needed and call _setup-doc in this case.
    ls ./{{DOC_DIRNAME}}/conf.py || (just _setup-doc && just _exit "Now edit conf.py and recall just doc to build the documentation.")

    echo Auto-generate modules documentation...
    # Positional args from seconds (if any) are paths you want to exclude from docs
    # -f overwrite existing .rst, --private include also "_"-starting attributes.
    sphinx-apidoc -f --private -o ./{{DOC_DIRNAME}}/source ./src

    echo Building documentation...
    sphinx-build -b html -c ./{{DOC_DIRNAME}} ./{{DOC_DIRNAME}}/source ./{{DOC_DIRNAME}}/build/html -v

    open {{DOC_DIRNAME}}/build/html/index.html

# remove untracked artifacts (git clean -fdx)
clean:
    # NB: after this, you will need to recompile cython files
    # (\"python setup.py install\" or \"just compile\")
    git clean -fdx

# shortcut to exit with a message and error exit code
@_exit MESSAGE:
    echo {{MESSAGE}} && exit 1

# error exit with fail alert message and error exit code
# TODO: decorate with red
@_fail MESSAGE:
    echo FAIL. {{MESSAGE}} && exit 1
