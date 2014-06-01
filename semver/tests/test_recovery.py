# -*- coding:utf-8 -*-
def test_it():
    from semver import max_satisfying
    assert max_satisfying(["2.4.3", "2.4.4", "2.5b", "3.0.1-b"], "~2", True) == "2.5b"
