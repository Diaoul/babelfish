import pickle
import typing

import pytest
from babelfish.region import Region


@pytest.mark.parametrize('value', [
    1, 22, 419, 4444, '1', '22', '199', '719', '999', '4444', 3.14, True, False
])
def test_wrong_region(value: typing.Any):
    with pytest.raises(ValueError):
        Region(value)


@pytest.mark.parametrize('value', [
    '001', '002', '015', '419', '729'
])
def test_eq(value: str):
    assert Region(value) == Region(value)


def test_ne():
    assert Region('001') != Region('419')


def test_hash_eq():
    assert hash(Region('002')) == hash(Region('002'))


def test_pickle():
    assert pickle.loads(pickle.dumps(Region('419'))) == Region('419')

