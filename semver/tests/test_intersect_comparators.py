# -*- coding:utf-8 -*-
import pytest
# node-semver/test/index.js

cands = [
    # One is a Version
    ['1.3.0', '>=1.3.0', True],
    ['1.3.0', '>1.3.0', False, False],
    ['>=1.3.0', '1.3.0', True],
    ['>1.3.0', '1.3.0', False, False],
    # Same direction increasing
    ['>1.3.0', '>1.2.0', True],
    ['>1.2.0', '>1.3.0', True],
    ['>=1.2.0', '>1.3.0', True],
    ['>1.2.0', '>=1.3.0', True],
    # Same direction decreasing
    ['<1.3.0', '<1.2.0', True],
    ['<1.2.0', '<1.3.0', True],
    ['<=1.2.0', '<1.3.0', True],
    ['<1.2.0', '<=1.3.0', True],
    # Different directions, same semver and inclusive operator
    ['>=1.3.0', '<=1.3.0', True],
    ['>=v1.3.0', '<=1.3.0', True],
    ['>=1.3.0', '>=1.3.0', True],
    ['<=1.3.0', '<=1.3.0', True],
    ['<=1.3.0', '<=v1.3.0', True],
    ['>1.3.0', '<=1.3.0', False, False],
    ['>=1.3.0', '<1.3.0', False, False],
    # Opposite matching directions
    ['>1.0.0', '<2.0.0', True],
    ['>=1.0.0', '<2.0.0', True],
    ['>=1.0.0', '<=2.0.0', True],
    ['>1.0.0', '<=2.0.0', True],
    ['<=2.0.0', '>1.0.0', True],
    ['<=1.0.0', '>=2.0.0', False, False]
]


@pytest.mark.skip(reason="not implemented yet")
# @pytest.mark.parametrize("v0, v1, expect, loose", cands)
def test_it(v0, v1, expect, loose):
    from semver import make_comparator, intersects
    comparator1 = make_comparator(v0)
    comparator2 = make_comparator(v1)
    actual1 = comparator1.intersects(comparator2)
    actual2 = comparator2.intersects(comparator1)
    actual3 = intersects(comparator1, comparator2)
    actual4 = intersects(comparator2, comparator1)
    actual4 = intersects(comparator1, comparator2, True)
    actual5 = intersects(comparator2, comparator1, True)
    actual6 = intersects(v0, v1)
    actual7 = intersects(v1, v0)
    actual8 = intersects(v0, v1, True)
    actual9 = intersects(v1, v0, True)
    assert actual1 == expect
    assert actual2 == expect
    assert actual3 == expect
    assert actual4 == expect
    assert actual5 == expect
    assert actual6 == expect
    assert actual7 == expect
    assert actual8 == expect
    assert actual9 == expect
