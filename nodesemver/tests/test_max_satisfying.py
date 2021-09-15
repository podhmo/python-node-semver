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
     True, True],

    [['1.0.1-beta'], '1.x', None, False, False],
    [['1.0.1-beta'], '1.x', '1.0.1-beta', False, True],
    [['1.0.0-beta'], '1.x', '1.0.0-beta', False, True],
    [['1.1.0-beta'], '1.0.x', None, False, True],
    [['1.0.0-beta', '1.1.0-beta', '1.1.0'], '1.0.x', None, False, False],
    [['1.0.0-beta', '1.1.0-beta', '1.1.0'], '1.0.x', '1.0.0-beta', False, True],

    # testing with range '>' and '<'
    [['1.0.0-beta', '1.0.0', '1.0.1-beta', '1.0.2-beta'], '>1.0.0 <1.0.2', None, False, False],
    [['1.0.0-beta', '1.0.0', '1.0.1-beta', '1.0.2-beta'], '>1.0.0 <1.0.2', '1.0.1-beta', False, True],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta', '1.1.0'], '>1.0.0 <1.1.0', '1.0.1', False, False],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta', '1.1.0'], '>1.0.0 <1.1.0', '1.0.1', False, True],
    [['1.0.0-beta', '1.1.0-beta'], '>1.0.0 <1.1.0', None, False, True],

    # testing with range '>=' and '<=' and '<'
    [['1.0.0-beta', '1.1.0-beta', '1.0.0'], '>=1.0.0 <=1.0.1', '1.0.0', False, False],
    [['1.0.0-beta', '1.1.0-beta', '1.0.0'], '>=1.0.0 <=1.0.1', '1.0.0', False, True],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta'], '>=1.0.0 <=1.1.0', '1.0.1', False, False],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta'], '>=1.0.0 <=1.1.0', '1.1.0-beta', False, True],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta'], '>=1.0.0 <1.1.0', '1.0.1', False, False],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta'], '>=1.0.0 <1.1.0', '1.0.1', False, True],
    [['1.0.0-beta', '1.1.0-beta'], '>=1.0.0 <=1.1.0', None, False, False],
    [['1.0.0-beta', '1.1.0-beta'], '>=1.0.0 <=1.1.0', '1.1.0-beta', False, True],

    # explicitly specifying range begin/end with prerelease
    [['1.0.0-beta', '1.1.0-beta', '1.0.0'], '>=1.0.0-0 <1.0.1', '1.0.0', False, True],
    [['1.0.0-beta', '1.1.0-beta', '1.1.0'], '>=1.0.0-0 <1.1.0-0', '1.0.0-beta', False, True],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta', '1.1.0'], '>=1.0.0-0 <1.1.0-0', '1.0.1', False, False],
    [['1.0.0-beta', '1.0.0', '1.0.1', '1.1.0-beta', '1.1.0'], '>=1.0.0-0 <1.1.0-0', '1.0.1', False, True],
    [['1.0.0-beta', '1.1.0-beta'], '>=1.0.0-0 <1.1.0', '1.0.0-beta', False, True],

    [['1.0.0-pre'],   '1.0.x', '1.0.0-pre', False, True],
    [['1.0.0-pre'], '>=1.0.x', '1.0.0-pre', False, True],

    [['1.1.0-pre'], '>=1.0.0 <1.1.1-z', None, False, False],
    # Note: This test would fail with `node-semver`, see also https://github.com/npm/node-semver/issues/317
    [['1.1.1-pre'], '>=1.0.0 <1.1.1-z', '1.1.1-pre', False, False],
    # While this one would succeed with `node-semver`
#    [['1.0.0-pre'], '>=1.0.0 <=1.1.0', None, False, True],

]


@pytest.mark.parametrize("versions, range_, expect, loose, include_prerelease", cands)
def test_it(versions, range_, expect, loose, include_prerelease):
    from nodesemver import max_satisfying
    if isinstance(expect, type) and issubclass(expect, Exception):
        with pytest.raises(expect):
            max_satisfying(versions, range_, loose, include_prerelease)
    else:
        assert max_satisfying(versions, range_, loose, include_prerelease) == expect
