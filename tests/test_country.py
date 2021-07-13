import pickle
import pytest
from babelfish.country import Country


def test_eq():
    assert Country("US") == Country("US")

def test_ne():
    assert Country("GB") != Country("US")

def test_hash_eq():
    assert hash(Country("US")) == hash("US")

def test_hasattr_name():
    assert hasattr(Country("US"), "name")

def test_hasattr_alpha2():
    assert hasattr(Country("US"), "alpha2")

def test_wrong():
    with pytest.raises(ValueError):
        Country("ZZ")

def test_pickle():
    assert pickle.loads(pickle.dumps(Country("GB"))) == Country("GB")
