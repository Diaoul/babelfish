
from babelfish import Language
from cattrs import structure, unstructure


def test_structure():
    language = Language('spa', 'ES', 'Latn')

    s = unstructure(language)
    assert s == {'alpha3': 'spa', 'country': {'alpha2': 'ES'}, 'script': {'code': 'Latn'}}

    rec = structure(s, Language)
    assert rec == language
