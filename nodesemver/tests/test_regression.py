import pytest

cands = [
    # https://github.com/podhmo/python-node-semver/issues/5
    ["<=1.2", "1.2.0", ["1.1.1", "1.2.0-pre", "1.2.0", "1.1.1-111", "1.1.1-21"]],
    ["<=1.2", "1.2", ["1.1.1", "1.2.0-pre", "1.2", "1.1.1-111", "1.1.1-21"]],
    ["<=1.2.0", "1.2.0", ["1.1.1", "1.2.0-pre", "1.2.0", "1.1.1-111", "1.1.1-21"]],
    ["<=1.2.0", "1.2", ["1.1.1", "1.2.0-pre", "1.2", "1.1.1-111", "1.1.1-21"]],
]


@pytest.mark.parametrize("op, wanted, cands", cands)
def test_it(op, wanted, cands):
    from nodesemver import max_satisfying
    got = max_satisfying(cands, op, loose=True)
    assert got == wanted
