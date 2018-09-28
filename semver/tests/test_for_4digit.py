# https://github.com/podhmo/python-semver/issues/15
import pytest

cands = [
    (
        "4.1.3", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": [],
            "build": [],
            "micro_versions": [],
        }
    ),
    (
        "4.1.3+jenkins", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": [],
            "build": ["jenkins"],
            "micro_versions": [],
        }
    ),
    (
        "4.1.3-pre", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": ["pre"],
            "build": [],
            "micro_versions": [],
        }
    ),
    # 4-digit
    (
        "4.1.3.2", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": [],
            "build": [],
            "micro_versions": [2],
        }
    ),
    (
        "4.1.3.2+jenkins", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": [],
            "build": ["jenkins"],
            "micro_versions": [2],
        }
    ),
    (
        "4.1.3.2-pre", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": ["pre"],
            "build": [],
            "micro_versions": [2],
        }
    ),
    (
        "4.1.3.2-pre2", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": ["pre2"],
            "build": [],
            "micro_versions": [2],
        }
    ),
    (
        "4.1.3.2-pre.2", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": ["pre"],
            "build": [],
            "micro_versions": [2, 2],
        }
    ),
    (
        "4.1.3.2-pre.2+xxx", True, {
            "major": 4,
            "minor": 1,
            "patch": 3,
            "prerelease": ["pre"],
            "build": ["xxx"],
            "micro_versions": [2, 2],
        }
    ),
]


@pytest.mark.parametrize("v, loose, expected", cands)
def test_parse(v, loose, expected):
    from semver import make_semver
    got = make_semver(v, loose=loose)
    assert got.raw == v
    assert got.major == expected["major"]
    assert got.minor == expected["minor"]
    assert got.patch == expected["patch"]
    assert got.prerelease == expected["prerelease"]
    assert got.build == expected["build"]
    assert got.micro_versions == expected["micro_versions"]
