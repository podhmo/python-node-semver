
versions = [
    '0.0.0-foo',
    '0.0.0',
    '0.0.0',
    '0.0.1', 
    '0.9.0',
    '0.9.9',
    '0.10.0',
    '0.10.0',
    '0.10.0',
    '0.99.0',
    '0.99.0',
    '1.0.0',
    '1.0.0',
    '1.2.3-4',
    '1.2.3-4',
    '1.2.3-5',
    '1.2.3-5',
    '1.2.3-4-foo',
    '1.2.3-5-Foo',
    '1.2.3-5-foo',
    '1.2.3-5-foo',
    '1.2.3-R2',
    '1.2.3-a',
    '1.2.3-a.5',
    '1.2.3-a.5',
    '1.2.3-a.10',
    '1.2.3-a.b',
    '1.2.3-a.b',
    '1.2.3-a.b.c.5.d.100',
    '1.2.3-a.b.c.10.d.5',
    '1.2.3-asdf',
    '1.2.3-r100',
    '1.2.3-r100',
    '1.2.3-r2',
    '1.2.3',
    '1.2.3',
    '2.0.0',
    '2.0.0',
    '2.7.2+asdf',
    '3.0.0',
]


spec_prerelease_examples = [
    '1.0.0-alpha',
    '1.0.0-alpha.1',
    '1.0.0-alpha.beta',
    '1.0.0-beta',
    '1.0.0-beta.2',
    '1.0.0-beta.11',
    '1.0.0-rc.1',
    '1.0.0',
]


def _shuffled_copy(source, seed=0):
    import random
    random.seed(seed)
    _copy = source[:]
    random.shuffle(_copy)
    # assert _copy != source
    return _copy


def test_sort():
    from semver import sort
    to_sort = _shuffled_copy(versions)
    sort(to_sort, True)
    assert versions == to_sort


def test_prerelease_sort():
    from semver import sort
    to_sort = _shuffled_copy(spec_prerelease_examples)
    sort(to_sort, False)
    assert spec_prerelease_examples == to_sort


def test_rsort():
    from semver import rsort
    to_sort = _shuffled_copy(versions)
    rsort(to_sort, True)
    assert list(reversed(versions)) == to_sort


def test_prerelease_rsort():
    from semver import rsort
    to_sort = _shuffled_copy(spec_prerelease_examples)
    rsort(to_sort, False)
    assert list(reversed(spec_prerelease_examples)) == to_sort
