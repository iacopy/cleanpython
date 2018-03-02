# Standard Library
from types import SimpleNamespace

# 3rd party
import pytest

# My stuff
from puzzle import cli


@pytest.mark.parametrize('case', [
    {
        'description': 'all auto',
        'options': dict(src='x', cells='auto', cell_size='auto', swaps=0, pixel=False, dst='o'),
        'shape': (10, 10),
        'expected': ((3, 3), 9),
    },
    {
        'description': 'cell_size calculation',
        'options': dict(src='x', cells='4x4', cell_size='auto', swaps=0, pixel=False, dst='o'),
        'shape': (10, 10),
        'expected': ((2, 2), 16),
    },
    {
        'description': 'cells calculation',
        'options': dict(src='x', cells='auto', cell_size='4x4', swaps=0, pixel=False, dst='o'),
        'shape': (10, 10),
        'expected': ((4, 4), 4),
    },
    {
        'description': 'cell_size calculation with given swaps',
        'options': dict(src='x', cells='1x6', cell_size='auto', swaps=1, pixel=False, dst='o'),
        'shape': (12, 12),
        'expected': ((12, 2), 1),
    },
    {
        'description': 'pixel option takes the priority',
        'options': dict(src='x', cells='auto', cell_size='12x34', swaps=3, pixel=True, dst='o'),
        'shape': (400, 600),
        'expected': ((1, 1), 3),
    },
    {
        'description': 'incompatible options',
        'options': dict(src='x', cells='1x6', cell_size='2x2', swaps=1, pixel=False, dst='o'),
        'shape': (1, 1),
        'expected': 'Error: forbidden to specify both cells and cell_size',
    }
], ids=lambda case: case['description'])
def test_process_options(case):
    """
    Test ``process_options`` function.
    """
    options = SimpleNamespace(**case['options'])
    try:
        res = cli.process_options(options, shape=case['shape'])
    except AssertionError as err:
        assert str(err) == case['expected']
    else:
        assert res == case['expected']
