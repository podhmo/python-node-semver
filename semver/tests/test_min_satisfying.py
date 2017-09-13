# -*- coding:utf-8 -*-
import pytest
# node-semver/test/index.js

cands = [
    [['1.2.3', '1.2.4'], '1.2', '1.2.3', False],
    [['1.2.4', '1.2.3'], '1.2', '1.2.3', False],
    [['1.2.3', '1.2.4', '1.2.5', '1.2.6'], '~1.2.3', '1.2.3', False],
    [['1.1.0', '1.2.0', '1.2.1', '1.3.0', '2.0.0b1', '2.0.0b2', '2.0.0b3', '2.0.0', '2.1.0'], '~2.0.0', '2.0.0', True]
]


@pytest.mark.skip(reason="not implemented yet")
# @pytest.mark.parametrize("versions, range_, expect, loose", cands)
def test_it(versions, range_, expect, loose):
    from semver import min_satisfying
    assert min_satisfying(versions, range_, loose) == expect
