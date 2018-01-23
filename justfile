PROJECT_NAME = 'Your Project Name'
AUTHOR = 'Your Name'
VIRTUALENV = 'your-venv-name'
DOC_DIRNAME = 'docs'
DOC_LANGUAGE = 'en'
DOC_INIT_VERSION = '0.1'
VIRTUALENVS_DIR = '~/.virtualenvs'

# Quality requirements
MIN_COVERAGE = '100'

# just list available recipes
@welcome:
    just --list

# bootstrap your project
setup:
    @echo Create virtualenv and use it to install requirements
    virtualenv -p python3 {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m pip install -r requirements.txt
    @echo Now please activate the virtualenv, then call "just doc-setup".

# statically check the codebase
@lint:
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m mypy src
    echo "mypy  : OK"
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m flake8 src
    echo "flake8: OK"
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m pylint src
    echo "pylint: OK"
    # Auto-fix imports with isort -> worktree become unclean if needed
    {{VIRTUALENVS_DIR}}/{{VIRTUALENV}}/bin/python -m isort --recursive src
    echo "isort : OK"

# run tests
test:
    pytest

# open coverage html index
coverage: test
    open htmlcov/index.html

# check coverage satisfies requirements
@check-coverage:
    coverage report --fail-under {{MIN_COVERAGE}}
    echo "test coverage: OK"

# Quality Assurance: code analysis, test and coverage
@qa:
    just lint
    just test
    just check-coverage
    echo Quality check OK.

# ensure that git repo is clean for commit
# (contains only stuff in the index, not in the worktree)
@_worktree_clean:
    python src/git_status.py index
    echo git-staged files and clean worktree.

# require quality and no garbage in the repo worktree
@committable: qa
    just _worktree_clean
    echo Your code seems committable.

# git commit if your code is committable
commit MESSAGE: committable
    git commit -m "{{MESSAGE}}"

# execute benchmarks tests only, in benchmark mode
benchmarks:
    pytest --benchmark-enable --benchmark-only

# bootstrap documentation
@doc-setup:
    @echo Setting up documentation...
    sphinx-quickstart -a "{{AUTHOR}}" -p "{{PROJECT_NAME}}" -v {{DOC_INIT_VERSION}} -l {{DOC_LANGUAGE}} --sep --ext-autodoc --ext-coverage --ext-todo --ext-viewcode --no-makefile --no-batchfile ./{{DOC_DIRNAME}}

    # move conf to main doc directory instead of its "source"
    mv ./{{DOC_DIRNAME}}/source/conf.py ./{{DOC_DIRNAME}}
    @echo NB: please uncomment "sys.path.append" line on conf.py and pass "../src" as argument in order to generate the documentation correctly.
    # TODO: automatize this step

# build and open generated documentation
@doc:
    echo Auto-generate modules documentation...
    # Positional args from seconds (if any) are paths you want to exclude from docs
    # -f overwrite existing .rst, --private include also "_"-starting attributes.
    sphinx-apidoc -f --private -o ./{{DOC_DIRNAME}}/source ./src

    echo Building documentation...
    sphinx-build -b html -c ./{{DOC_DIRNAME}} ./{{DOC_DIRNAME}}/source ./{{DOC_DIRNAME}}/build/html -v

    open {{DOC_DIRNAME}}/build/html/index.html

# remove artifacts (pyc, __pycache__, coverage stuff, built docs)
cleanup:
    find . -type d -name __pycache__ | xargs rm -rfv
    rm -rf htmlcov
    coverage erase

    # cleanup built documentation
    rm -rf {{DOC_DIRNAME}}/build
