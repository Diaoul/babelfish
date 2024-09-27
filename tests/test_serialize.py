from babelfish import Language
from cattrs import structure, unstructure


def test_structure():
    language = Language('spa', 'ES', 'Latn')

    s = unstructure(language)
    assert s == {'language': 'spa', 'country': {'country': 'ES'}, 'script': {'script': 'Latn'}}

    rec = structure(s, Language)
    assert rec == language
