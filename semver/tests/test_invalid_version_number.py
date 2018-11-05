# -*- coding:utf-8 -*-
import pytest
# node-semver/test/index.js

cands = [
    ('1.2.3.4', False, ValueError),
    ('NOT VALID', False, ValueError),
    (1.2, False, ValueError),
    ("1.2", False, ValueError),
    ("1.a.2", False, ValueError),
    (None, False, ValueError),
    ('X.2', False, ValueError),
    ('Infinity.NaN.Infinity', False, ValueError),
    ('1.2.3.4', True, None),
    ('NOT VALID', True, ValueError),
    (1.2, True, ValueError),
    ("1.2", True, None),
    ("1.a.2", True, ValueError),
    (None, True, ValueError),
    ('Infinity.NaN.Infinity', True, ValueError),
    ('X.2', True, ValueError),
]


@pytest.mark.parametrize("v, loose, exc", cands)
def test_it(v, loose, exc):
    import pytest
    from semver import make_semver
    if exc is not None:
        with pytest.raises(exc):
            make_semver(v, loose)
    else:
        make_semver(v, loose)
