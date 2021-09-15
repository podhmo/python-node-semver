# -*- coding:utf-8 -*-
import pytest
# node-semver/test/index.js

cands = [
    ['1.2.3', 'major', '2.0.0', False, None],
    ['1.2.3', 'minor', '1.3.0', False, None],
    ['1.2.3', 'patch', '1.2.4', False, None],
    ['1.2.3tag', 'major', '2.0.0', True, None],
    ['1.2.3-tag', 'major', '2.0.0', False, None],
    ['1.2.3', 'fake', None, False, None],
    ['1.2.0-0', 'patch', '1.2.0', False, None],
    ['fake', 'major', None, False, None],
    ['1.2.3-4', 'major', '2.0.0', False, None],
    ['1.2.3-4', 'minor', '1.3.0', False, None],
    ['1.2.3-4', 'patch', '1.2.3', False, None],
    ['1.2.3-alpha.0.beta', 'major', '2.0.0', False, None],
    ['1.2.3-alpha.0.beta', 'minor', '1.3.0', False, None],
    ['1.2.3-alpha.0.beta', 'patch', '1.2.3', False, None],
    ['1.2.4', 'prerelease', '1.2.5-0', False, None],
    ['1.2.3-0', 'prerelease', '1.2.3-1', False, None],
    ['1.2.3-alpha.0', 'prerelease', '1.2.3-alpha.1', False, None],
    ['1.2.3-alpha.1', 'prerelease', '1.2.3-alpha.2', False, None],
    ['1.2.3-alpha.2', 'prerelease', '1.2.3-alpha.3', False, None],
    ['1.2.3-alpha.0.beta', 'prerelease', '1.2.3-alpha.1.beta', False, None],
    ['1.2.3-alpha.1.beta', 'prerelease', '1.2.3-alpha.2.beta', False, None],
    ['1.2.3-alpha.2.beta', 'prerelease', '1.2.3-alpha.3.beta', False, None],
    ['1.2.3-alpha.10.0.beta', 'prerelease', '1.2.3-alpha.10.1.beta', False, None],
    ['1.2.3-alpha.10.1.beta', 'prerelease', '1.2.3-alpha.10.2.beta', False, None],
    ['1.2.3-alpha.10.2.beta', 'prerelease', '1.2.3-alpha.10.3.beta', False, None],
    ['1.2.3-alpha.10.beta.0', 'prerelease', '1.2.3-alpha.10.beta.1', False, None],
    ['1.2.3-alpha.10.beta.1', 'prerelease', '1.2.3-alpha.10.beta.2', False, None],
    ['1.2.3-alpha.10.beta.2', 'prerelease', '1.2.3-alpha.10.beta.3', False, None],
    ['1.2.3-alpha.9.beta', 'prerelease', '1.2.3-alpha.10.beta', False, None],
    ['1.2.3-alpha.10.beta', 'prerelease', '1.2.3-alpha.11.beta', False, None],
    ['1.2.3-alpha.11.beta', 'prerelease', '1.2.3-alpha.12.beta', False, None],
    ['1.2.0', 'prepatch', '1.2.1-0', False, None],
    ['1.2.0-1', 'prepatch', '1.2.1-0', False, None],
    ['1.2.0', 'preminor', '1.3.0-0', False, None],
    ['1.2.3-1', 'preminor', '1.3.0-0', False, None],
    ['1.2.0', 'premajor', '2.0.0-0', False, None],
    ['1.2.3-1', 'premajor', '2.0.0-0', False, None],
    ['1.2.0-1', 'minor', '1.2.0', False, None],
    ['1.0.0-1', 'major', '1.0.0', False, None],

    ['1.2.3', 'major', '2.0.0', False, 'dev'],
    ['1.2.3', 'minor', '1.3.0', False, 'dev'],
    ['1.2.3', 'patch', '1.2.4', False, 'dev'],
    ['1.2.3tag', 'major', '2.0.0', True, 'dev'],
    ['1.2.3-tag', 'major', '2.0.0', False, 'dev'],
    ['1.2.3', 'fake', None, False, 'dev'],
    ['1.2.0-0', 'patch', '1.2.0', False, 'dev'],
    ['fake', 'major', None, False, 'dev'],
    ['1.2.3-4', 'major', '2.0.0', False, 'dev'],
    ['1.2.3-4', 'minor', '1.3.0', False, 'dev'],
    ['1.2.3-4', 'patch', '1.2.3', False, 'dev'],
    ['1.2.3-alpha.0.beta', 'major', '2.0.0', False, 'dev'],
    ['1.2.3-alpha.0.beta', 'minor', '1.3.0', False, 'dev'],
    ['1.2.3-alpha.0.beta', 'patch', '1.2.3', False, 'dev'],
    ['1.2.4', 'prerelease', '1.2.5-dev.0', False, 'dev'],
    ['1.2.3-0', 'prerelease', '1.2.3-dev.0', False, 'dev'],
    ['1.2.3-alpha.0', 'prerelease', '1.2.3-dev.0', False, 'dev'],
    ['1.2.3-alpha.0', 'prerelease', '1.2.3-alpha.1', False, 'alpha'],
    ['1.2.3-alpha.0.beta', 'prerelease', '1.2.3-dev.0', False, 'dev'],
    ['1.2.3-alpha.0.beta', 'prerelease', '1.2.3-alpha.1.beta', False, 'alpha'],
    ['1.2.3-alpha.10.0.beta', 'prerelease', '1.2.3-dev.0', False, 'dev'],
    ['1.2.3-alpha.10.0.beta', 'prerelease', '1.2.3-alpha.10.1.beta', False, 'alpha'],
    ['1.2.3-alpha.10.1.beta', 'prerelease', '1.2.3-alpha.10.2.beta', False, 'alpha'],
    ['1.2.3-alpha.10.2.beta', 'prerelease', '1.2.3-alpha.10.3.beta', False, 'alpha'],
    ['1.2.3-alpha.10.beta.0', 'prerelease', '1.2.3-dev.0', False, 'dev'],
    ['1.2.3-alpha.10.beta.0', 'prerelease', '1.2.3-alpha.10.beta.1', False, 'alpha'],
    ['1.2.3-alpha.10.beta.1', 'prerelease', '1.2.3-alpha.10.beta.2', False, 'alpha'],
    ['1.2.3-alpha.10.beta.2', 'prerelease', '1.2.3-alpha.10.beta.3', False, 'alpha'],
    ['1.2.3-alpha.9.beta', 'prerelease', '1.2.3-dev.0', False, 'dev'],
    ['1.2.3-alpha.9.beta', 'prerelease', '1.2.3-alpha.10.beta', False, 'alpha'],
    ['1.2.3-alpha.10.beta', 'prerelease', '1.2.3-alpha.11.beta', False, 'alpha'],
    ['1.2.3-alpha.11.beta', 'prerelease', '1.2.3-alpha.12.beta', False, 'alpha'],
    ['1.2.0', 'prepatch', '1.2.1-dev.0', False, 'dev'],
    ['1.2.0-1', 'prepatch', '1.2.1-dev.0', False, 'dev'],
    ['1.2.0', 'preminor', '1.3.0-dev.0', False, 'dev'],
    ['1.2.3-1', 'preminor', '1.3.0-dev.0', False, 'dev'],
    ['1.2.0', 'premajor', '2.0.0-dev.0', False, 'dev'],
    ['1.2.3-1', 'premajor', '2.0.0-dev.0', False, 'dev'],
    ['1.2.0-1', 'minor', '1.2.0', False, 'dev'],
    ['1.0.0-1', 'major', '1.0.0', False, 'dev'],
    ['1.2.3-dev.bar', 'prerelease', '1.2.3-dev.0', False, 'dev']
]


@pytest.mark.parametrize("pre, what, wanted, loose, identifier", cands)
def test_it(pre, what, wanted, loose, identifier):
    from nodesemver import inc
    assert inc(pre, what, loose, identifier=identifier) == wanted