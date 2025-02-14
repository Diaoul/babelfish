# ruff: noqa: B018
import pytest
from babelfish import language_converters
from babelfish.compat import resource_stream
from babelfish.converters import LanguageReverseConverter
from babelfish.exceptions import LanguageConvertError, LanguageReverseError
from babelfish.language import Language


def test_converter_alpha2():
    assert Language('eng').alpha2 == 'en'
    assert Language.fromalpha2('en') == Language('eng')
    assert Language.fromcode('en', 'alpha2') == Language('eng')
    with pytest.raises(LanguageReverseError):
        Language.fromalpha2('zz')
    with pytest.raises(LanguageConvertError):
        Language('aaa').alpha2
    assert len(language_converters['alpha2'].codes) == 184


def test_converter_alpha3b():
    assert Language('fra').alpha3b == 'fre'
    assert Language.fromalpha3b('fre') == Language('fra')
    assert Language.fromcode('fre', 'alpha3b') == Language('fra')
    with pytest.raises(LanguageReverseError):
        Language.fromalpha3b('zzz')
    with pytest.raises(LanguageConvertError):
        Language('aaa').alpha3b
    assert len(language_converters['alpha3b'].codes) == 418


def test_converter_alpha3t():
    assert Language('fra').alpha3t == 'fra'
    assert Language.fromalpha3t('fra') == Language('fra')
    assert Language.fromcode('fra', 'alpha3t') == Language('fra')
    with pytest.raises(LanguageReverseError):
        Language.fromalpha3t('zzz')
    with pytest.raises(LanguageConvertError):
        Language('aaa').alpha3t
    assert len(language_converters['alpha3t'].codes) == 418


def test_converter_name():
    assert Language('eng').name == 'English'
    assert Language.fromname('English') == Language('eng')
    assert Language.fromcode('English', 'name') == Language('eng')
    with pytest.raises(LanguageReverseError):
        Language.fromname('Zzzzzzzzz')
    assert len(language_converters['name'].codes) == 7874


def test_converter_scope():
    assert language_converters['scope'].codes == {'I', 'S', 'M'}
    assert Language('eng').scope == 'individual'
    assert Language('und').scope == 'special'


def test_converter_type():
    assert language_converters['type'].codes == {'A', 'C', 'E', 'H', 'L', 'S'}
    assert Language('eng').type == 'living'
    assert Language('und').type == 'special'


def test_converter_opensubtitles():
    assert Language('fra').opensubtitles == Language('fra').alpha3b
    assert Language('por', 'BR').opensubtitles == 'pob'
    assert Language('zho', 'TW').opensubtitles == 'zht'
    assert Language.fromopensubtitles('fre') == Language('fra')
    assert Language.fromopensubtitles('pob') == Language('por', 'BR')
    assert Language.fromopensubtitles('zht') == Language('zho', 'TW')
    assert Language.fromopensubtitles('pb') == Language('por', 'BR')
    # Montenegrin is not recognized as an ISO language (yet?) but for now it is
    # unofficially accepted as Serbian from Montenegro
    assert Language.fromopensubtitles('mne') == Language('srp', 'ME')
    assert Language.fromcode('pob', 'opensubtitles') == Language('por', 'BR')
    with pytest.raises(LanguageReverseError):
        Language.fromopensubtitles('zzz')
    with pytest.raises(LanguageConvertError):
        Language('aaa').opensubtitles
    assert len(language_converters['opensubtitles'].codes) == 608

    # test with all the LANGUAGES from the opensubtitles api
    # downloaded from: http://www.opensubtitles.org/addons/export_languages.php
    with resource_stream('babelfish', 'data/opensubtitles_languages.txt') as f:
        f.readline()
        for raw_line in f:
            idlang, alpha2, _, upload_enabled, web_enabled = raw_line.decode('utf-8').strip().split('\t')
            if not int(upload_enabled) and not int(web_enabled):
                # do not test LANGUAGES that are too esoteric / not widely available
                continue
            assert Language.fromopensubtitles(idlang).opensubtitles == idlang
            if alpha2:
                assert Language.fromopensubtitles(idlang) == Language.fromopensubtitles(alpha2)


def test_converter_opensubtitles_codes():
    for code in language_converters['opensubtitles'].from_opensubtitles:
        assert code in language_converters['opensubtitles'].codes


def test_register_converter():
    class TestConverter(LanguageReverseConverter):
        def __init__(self):
            self.to_test = {'fra': 'test1', 'eng': 'test2'}
            self.from_test = {'test1': 'fra', 'test2': 'eng'}

        def convert(self, alpha3, country=None, script=None):
            if alpha3 not in self.to_test:
                raise LanguageConvertError(alpha3, country, script)
            return self.to_test[alpha3]

        def reverse(self, test):
            if test not in self.from_test:
                raise LanguageReverseError(test)
            return (self.from_test[test], None)

    language = Language('fra')
    assert not hasattr(language, 'test')
    language_converters['test'] = TestConverter()
    assert hasattr(language, 'test')
    assert 'test' in language_converters
    assert Language('fra').test == 'test1'
    assert Language.fromtest('test2').alpha3 == 'eng'
    del language_converters['test']
    assert 'test' not in language_converters
    with pytest.raises(KeyError):
        Language.fromtest('test1')
    with pytest.raises(AttributeError):
        Language('fra').test
