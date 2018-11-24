# -*- coding:utf-8 -*-
import pytest
# node-semver/test/index.js

cands = [
    [['1.2.4', '1.2.3', '1.2.5-beta'], '~1.2.3', '1.2.5-beta', False, True],
    [['1.2.4', '1.2.3', '1.2.5-beta'], '~1.2.3', '1.2.4', False, False],
    [['1.2.3', '1.2.4'], '1.2', '1.2.4', False, False],
    [['1.2.4', '1.2.3'], '1.2', '1.2.4', False, False],
    [['1.2.3', '1.2.4', '1.2.5', '1.2.6'], '~1.2.3', '1.2.6', False, False],
    [['1.1.0', '1.2.0', '1.2.1', '1.3.0', '2.0.0b1', '2.0.0b2', '2.0.0b3', '2.0.0', '2.1.0'], '~2.0.0', '2.0.0',
     True, False],
    [['1.1.0', '1.2.0', '1.2.1', '1.3.0', '2.0.0b1', '2.0.0b2', '2.0.0b3', '2.0.0', '2.1.0'], '~2.0.0', ValueError,
     False, False],
    [['1.1.0', '1.2.0', '1.2.1', '1.3.0', '2.0.0b1', '2.0.0b2', '2.0.0', '2.0.1b1', '2.1.0'], '~2.0.0', '2.0.0',
     True, False],
    [['1.1.0', '1.2.0', '1.2.1', '1.3.0', '2.0.0b1', '2.0.0b2', '2.0.0', '2.0.1b1', '2.1.0'], '~2.0.0', '2.0.1b1',
     True, True]

]


@pytest.mark.parametrize("versions, range_, expect, loose, include_prerelease", cands)
def test_it(versions, range_, expect, loose, include_prerelease):
    from semver import max_satisfying
    if isinstance(expect, type) and issubclass(expect, Exception):
        with pytest.raises(expect):
            max_satisfying(versions, range_, loose, include_prerelease)
    else:
        assert max_satisfying(versions, range_, loose, include_prerelease) == expect
