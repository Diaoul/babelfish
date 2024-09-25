import pickle

import pytest
from babelfish.script import Script


def test_wrong_script():
    with pytest.raises(ValueError):
        Script("Qwerty")

def test_eq():
    assert Script("Latn") == Script("Latn")

def test_ne():
    assert Script("Cyrl") != Script("Latn")

def test_hash_eq():
    assert hash(Script("Hira")) == hash(Script("Hira"))

def test_pickle():
    assert pickle.loads(pickle.dumps(Script("Latn"))) == Script("Latn")

