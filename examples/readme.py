# -*- coding:utf-8 -*-
from semver import satisfies

assert satisfies("1.2.3-dev.1+abc", ">1.1.0 <2.0.0", include_prerelease=True)
assert not satisfies("1.2.3-dev.1+abc", ">1.1.0 <2.0.0", include_prerelease=False)
assert satisfies("1.2.3", ">1.1 <2.0")


from semver import max_satisfying

versions = ['1.2.3', '1.2.4', '1.2.5', '1.2.6', '2.0.1']
range_ = '~1.2.3'
assert max_satisfying(versions, range_, loose=False) == '1.2.6'


versions = ['1.1.0', '1.2.0', '1.2.1', '1.3.0', '2.0.0b1', '2.0.0b2', '2.0.0b3', '2.0.0', '2.1.0']
range_ = '~2.0.0'
assert max_satisfying(versions, range_, loose=True) == '2.0.0'

try:
    (max_satisfying(versions, range_, loose=False) == '2.0.0')
except ValueError as e:
    assert e.args[0] == "Invalid Version: 2.0.0b1"


versions = ['1.2.3', '1.2.4', '1.2.5', '1.2.6-pre.1', '2.0.1']
range_ = '~1.2.3'
assert max_satisfying(versions, range_, loose=False, include_prerelease=True) == '1.2.6-pre.1'
assert max_satisfying(versions, range_, loose=False, include_prerelease=False) == '1.2.5'
