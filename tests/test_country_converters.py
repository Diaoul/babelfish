import pytest
from babelfish import Country, country_converters, CountryReverseError, CountryReverseConverter, CountryConvertError


def test_country_converters():
    assert len(country_converters['name'].codes) == 249


@pytest.mark.parametrize('alpha2, name', [
    ('BR', 'BRAZIL'),
    ('FR', 'FRANCE'),
    ('GB', 'UNITED KINGDOM'),
])
def test_converter_name(alpha2: str, name: str):
    assert Country(alpha2).name == name
    assert Country.fromname(name) == Country(alpha2)
    assert Country.fromcode(name, 'name') == Country(alpha2)
    with pytest.raises(CountryReverseError):
        Country.fromname(name + '_123')


@pytest.mark.parametrize('alpha2, unm49', [
    ('BR', '076'),
    ('FR', '250'),
    ('GB', '826'),
])
def test_converter_unm49(alpha2: str, unm49: str):
    assert Country(alpha2).unm49 == unm49
    assert Country.fromunm49(unm49) == Country(alpha2)
    assert Country.fromcode(unm49, 'unm49') == Country(alpha2)
    with pytest.raises(CountryReverseError):
        Country.fromunm49(unm49 + '1')


def test_register_converter():
    class TestConverter(CountryReverseConverter):
        def __init__(self):
            self.to_test = {'FR': 'alpha1', 'BR': 'beta2'}
            self.from_test = {'alpha2': 'FR', 'beta2': 'BR'}

        def convert(self, alpha2):
            if alpha2 not in self.to_test:
                raise CountryConvertError(alpha2)
            return self.to_test[alpha2]

        def reverse(self, test):
            if test not in self.from_test:
                raise CountryReverseError(test)
            return self.from_test[test]

    country = Country('FR')
    assert not hasattr(country, 'test')
    country_converters['test'] = TestConverter()
    assert hasattr(country, 'test')
    assert 'test' in country_converters
    assert Country('FR').test == 'alpha1'
    assert Country.fromtest('beta2').alpha2 == 'BR'
    del country_converters['test']
    assert 'test' not in country_converters
    with pytest.raises(KeyError):
        Country.fromtest('alpha1')
    with pytest.raises(AttributeError):
        Country('FR').test

