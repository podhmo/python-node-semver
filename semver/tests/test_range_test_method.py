# -*- coding:utf-8 -*-
import pytest

cands = [
    ['>=1.2.3', '2.0.0-pre', False, False],
]


@pytest.mark.parametrize("range_, version, loose, expected", cands)
def test_it(range_, version, loose, expected):
    from semver import make_semver, satisfies
    # assert expected == make_semver(range_, loose=loose).test(version)
    assert expected == satisfies(version, range_, loose=loose)
