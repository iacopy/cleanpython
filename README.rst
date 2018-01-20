Kooality
========

A python project template with useful batteries included to
help you to write clean, tested, quality code with best practices.

Quality code has to be working and easy to mantain.

- working ⇨ ~no bugs ⇨ tested ("untested code is broken code")
    - → pytest, hypothesis, coverage, mypy
- easy to mantain
    - clean
        - simple → pylint, flake8
        - readable → pylint, flake8, mypy
        - predictable → mypy
        - standard → flake8, pylint
    - well tested → pytest, hypothesis, coverage, mypy
    - well documented
        - → sphinx
        - → mypy
        - → pylint
        - → flake8
- fast
    - → pytest-benchmark
    - → Cython

Tools
^^^^^

- pytest → no bugs
    - useful to write data driven tests
- mypy → no bugs
    - helps to find hidden bugs before they come up
    - make code more clear and understandable
- hypothesis → no bugs
    - really useful to find unexpected edge cases to test
- coverage → no bugs
    - which lines are not covered by tests?
- pylint → clean and documented code
    - with several complexity metrics it's useful to keep your code clean, simple and readable
    - helps you to start refactor before your code become too complex
    - a must if you want to keep clean
- flake8 → clean and documented code
    - pep8, pyflakes, McCabe Complexity analysis
    - suports plugins
- sphinx → documented code
- just
    - rules them all together in your workflow
    - `just commit MESSAGE` allows you to commit only clean and tested code
