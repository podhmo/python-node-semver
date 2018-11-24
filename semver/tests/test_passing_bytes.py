import pytest


def test_max_satisfying():
    def _callFUT(versions, range_):
        from semver import max_satisfying
        max_satisfying(versions, range_)

    from semver import InvalidTypeIncluded
    with pytest.raises(InvalidTypeIncluded):
        _callFUT([b"1.0.0"], "1.0.0")
    with pytest.raises(InvalidTypeIncluded):
        _callFUT(["1.0.0"], b"1.0.0")
    with pytest.raises(InvalidTypeIncluded):
        _callFUT("1.0.0", [b"1.0.0"])  # mistakes
    with pytest.raises(InvalidTypeIncluded):
        _callFUT(b"1.0.0", ["1.0.0"])  # mistakes
    _callFUT(["1.0.0"], "1.0.0")


def test_satisfies():
    def _callFUT(version, range_):
        from semver import satisfies
        satisfies(version, range_)

    from semver import InvalidTypeIncluded
    with pytest.raises(InvalidTypeIncluded):
        _callFUT(b"1.0.0", "1.0.0")
    with pytest.raises(InvalidTypeIncluded):
        _callFUT("1.0.0", b"1.0.0")
