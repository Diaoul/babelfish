#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from unittest import TestCase, TestSuite, TestLoader, TextTestRunner
from babelfish import (LANGUAGES, Language, Country, CONVERTERS, ReverseConverter, load_converters, clear_converters,
    register_converter, unregister_converter, ConvertError, ReverseError)


class TestCountry(TestCase):
    def test_wrong_country(self):
        with self.assertRaises(ValueError):
            Country('ZZ')

    def test_eq(self):
        self.assertTrue(Country('US') == Country('US'))

    def test_ne(self):
        self.assertTrue(Country('GB') != Country('US'))

    def test_hash(self):
        self.assertTrue(hash(Country('US')) == hash('US'))


class TestLanguage(TestCase):
    def test_languages(self):
        self.assertTrue(len(LANGUAGES) == 7874)

    def test_wrong_language(self):
        with self.assertRaises(ValueError):
            Language('zzz')

    def test_converter_alpha2(self):
        self.assertTrue(Language('eng').alpha2 == 'en')
        self.assertTrue(Language.fromalpha2('en') == Language('eng'))
        self.assertTrue(Language.fromcode('en', 'alpha2') == Language('eng'))
        with self.assertRaises(ReverseError):
            Language.fromalpha2('zz')
        with self.assertRaises(ConvertError):
            Language('aaa').alpha2
        self.assertTrue(len(CONVERTERS['alpha2'].codes) == 184)

    def test_converter_alpha3b(self):
        self.assertTrue(Language('fra').alpha3b == 'fre')
        self.assertTrue(Language.fromalpha3b('fre') == Language('fra'))
        self.assertTrue(Language.fromcode('fre', 'alpha3b') == Language('fra'))
        with self.assertRaises(ReverseError):
            Language.fromalpha3b('zzz')
        with self.assertRaises(ConvertError):
            Language('aaa').alpha3b
        self.assertTrue(len(CONVERTERS['alpha3b'].codes) == 418)

    def test_converter_name(self):
        self.assertTrue(Language('eng').name == 'English')
        self.assertTrue(Language.fromname('English') == Language('eng'))
        self.assertTrue(Language.fromcode('English', 'name') == Language('eng'))
        with self.assertRaises(ReverseError):
            Language.fromname('Zzzzzzzzz')
        self.assertTrue(len(CONVERTERS['name'].codes) == 7874)

    def test_converter_opensubtitles(self):
        self.assertTrue(Language('fra').opensubtitles == Language('fra').alpha3b)
        self.assertTrue(Language('por', 'BR').opensubtitles == 'pob')
        self.assertTrue(Language.fromopensubtitles('fre') == Language('fra'))
        self.assertTrue(Language.fromopensubtitles('pob') == Language('por', 'BR'))
        self.assertTrue(Language.fromcode('pob', 'opensubtitles') == Language('por', 'BR'))
        with self.assertRaises(ReverseError):
            Language.fromopensubtitles('zzz')
        with self.assertRaises(ConvertError):
            Language('aaa').opensubtitles
        self.assertTrue(len(CONVERTERS['opensubtitles'].codes) == 419)

    def test_country(self):
        self.assertTrue(Language('por', 'BR').country == Country('BR'))
        self.assertTrue(Language('eng', Country('US')).country == Country('US'))

    def test_eq(self):
        self.assertTrue(Language('eng') == Language('eng'))

    def test_eq_with_country(self):
        self.assertTrue(Language('eng', 'US') == Language('eng', Country('US')))

    def test_ne(self):
        self.assertTrue(Language('fra') != Language('eng'))

    def test_ne_with_country(self):
        self.assertTrue(Language('eng', 'US') != Language('eng', Country('GB')))

    def test_hash(self):
        self.assertTrue(hash(Language('fra')) == hash('fra'))

    def test_register_converter(self):
        class TestConverter(ReverseConverter):
            def __init__(self):
                self.to_test = {'fra': 'test1', 'eng': 'test2'}
                self.from_test = {'test1': 'fra', 'test2': 'eng'}

            def convert(self, alpha3, country=None):
                if alpha3 not in self.to_test:
                    raise ConvertError(alpha3, country)
                return self.to_test[alpha3]

            def reverse(self, test):
                if test not in self.from_test:
                    raise ReverseError(test)
                return (self.from_test[test], None)
        language = Language('fra')
        self.assertTrue(not hasattr(language, 'test'))
        register_converter('test', TestConverter)
        self.assertTrue(hasattr(language, 'test'))
        self.assertTrue('test' in CONVERTERS)
        self.assertTrue(Language('fra').test == 'test1')
        self.assertTrue(Language.fromtest('test2').alpha3 == 'eng')
        unregister_converter('test')
        self.assertTrue('test' not in CONVERTERS)
        self.assertTrue(not hasattr(Language, 'fromtest'))
        with self.assertRaises(AttributeError):
            Language('fra').test
        clear_converters()
        load_converters()


def suite():
    suite = TestSuite()
    suite.addTest(TestLoader().loadTestsFromTestCase(TestCountry))
    suite.addTest(TestLoader().loadTestsFromTestCase(TestLanguage))
    return suite


if __name__ == '__main__':
    TextTestRunner().run(suite())
