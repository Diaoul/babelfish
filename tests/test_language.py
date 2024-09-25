import pickle

import pytest
from babelfish.country import Country
from babelfish.language import LANGUAGES, Language
from babelfish.script import Script


def test_languages():
    assert len(LANGUAGES) == 7874

def test_eq():
    assert Language("eng") == Language("eng")

def test_ne():
    assert Language("eng") != Language("fra")

def test_hasattr_alpha3():
    assert hasattr(Language("fra"), "alpha3")

def test_hasattr_alpha2():
    assert hasattr(Language("eng"), "alpha2")

def test_not_hasattr_alpha2():
    assert not hasattr(Language("bej"), "alpha2")

def test_bool_casting_is_true():
    assert bool(Language("eng"))

def test_bool_casting_und_is_false():
    assert not bool(Language("und"))

def test_wrong():
    with pytest.raises(ValueError):
        Language("xyz")

def test_wrong_as_unknown():
    assert Language("zzzz", unknown="und") == Language("und")

def test_eq_with_country():
    assert Language("eng", "US") == Language("eng", Country("US"))

def test_ne_with_country():
    assert Language("fra", "FR") != Language("fra", "CA")

def test_ne_with_country_and_none():
    assert Language("fra", "FR") != Language("fra")

def test_eq_with_script():
    assert Language("srp", script="Latn") == Language("srp", script=Script("Latn"))

def test_ne_with_script():
    assert Language("srp", script="Latn") != Language("srp", script="Cyrl")

def test_ne_with_script_and_none():
    assert Language("srp", script="Latn") != Language("srp")

def test_hash():
    assert hash(Language("fra")) == hash("fr")
    assert hash(Language("ace")) == hash("ace")
    assert hash(Language("por", "BR")) == hash("pt-BR")
    assert hash(Language("srp", script="Cyrl")) == hash("sr-Cyrl")
    assert hash(Language("eng", country="US", script="Latn")) == hash("en-US-Latn")

@pytest.mark.parametrize("language", [
    Language('fra'),
    Language('eng', 'US'),
    Language('srp', script='Latn'),
    Language('eng', 'US', 'Latn')
])
def test_pickle(language):
    assert pickle.loads(pickle.dumps(language)) == language

def test_str_ietf_format():
    assert str(Language("eng", "US", "Latn")) == "en-US-Latn"
    assert str(Language("fra", "FR")) == "fr-FR"
    assert str(Language("srp", script="Cyrl")) == "sr-Cyrl"
    assert str(Language("bel")) == "be"

def test_fromietf_with_country_and_script():
    assert Language.fromietf("fra-FR-Latn") == Language("fra", "FR", "Latn")

def test_fromietf_with_country_and_no_script():
    assert Language.fromietf("fr-FR") == Language("fra", "FR")

def test_fromietf_with_script_and_no_country():
    assert Language.fromietf("eng-Latn") == Language("eng", script="Latn")

def test_fromietf_wrong_language_raises_valueerror():
    with pytest.raises(ValueError):
        Language.fromietf("xyz-FR")

def test_fromietf_wrong_country_raises_valueerror():
    with pytest.raises(ValueError):
        Language.fromietf("eng-XY")

def test_fromietf_wrong_script_raises_valueerror():
    with pytest.raises(ValueError):
        Language.fromietf("fra-FR-Wxyz")

