# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from functools import partial
from pkg_resources import resource_stream, iter_entry_points  # @UnresolvedImport
from .converters import ReverseConverter
from .country import Country
from .exceptions import ConvertError
from .script import Script


CONVERTERS = {}
LANGUAGES = set()
f = resource_stream('babelfish', 'data/iso-639-3.tab')
f.readline()
for l in f:
    (alpha3, _, _, _, _, _, _, _) = l.decode('utf-8').split('\t')
    LANGUAGES.add(alpha3)
f.close()


class Language(object):
    """A human language

    A human language is composed of a language part following the ISO-639
    standard and can be country-specific when a :class:`~babelfish.country.Country`
    is specified.

    The :class:`Language` is extensible with custom converters (see :ref:`custom_converters`)

    :param string language: the language as a 3-letter ISO-639-3 code
    :param country: the country (if any) as a 2-letter ISO-3166 code or :class:`~babelfish.country.Country` instance
    :type country: string or :class:`~babelfish.country.Country` or None
    :param script: the script (if any) as a 4-letter ISO-15924 code or :class:`~babelfish.script.Script` instance
    :type script: string or :class:`~babelfish.script.Script` or None

    """
    def __init__(self, language, country=None, script=None):
        if language not in LANGUAGES:
            raise ValueError('%r is not a valid language' % language)
        self.alpha3 = language
        self.country = None
        if isinstance(country, Country):
            self.country = country
        elif country is None:
            self.country = None
        else:
            self.country = Country(country)
        self.script = None
        if isinstance(script, Script):
            self.script = script
        elif script is None:
            self.script = None
        else:
            self.script = Script(script)

    @classmethod
    def fromcode(cls, code, converter):
        return cls(*CONVERTERS[converter].reverse(code))

    @classmethod
    def fromietf(cls, ietf):
        subtags = ietf.split('-')
        language_subtag = subtags.pop(0).lower()
        if len(language_subtag) == 2:
            language = cls.fromalpha2(language_subtag)
        else:
            language = cls(language_subtag)
        while subtags:
            subtag = subtags.pop(0)
            if len(subtag) == 2:
                language.country = Country(subtag.upper())
            else:
                language.script = Script(subtag.capitalize())
            if language.script is not None:
                if subtags:
                    raise ValueError('Wrong IETF format. Unmatched subtags: %r' % subtags)
                break
        return language

    def __getattr__(self, name):
        if name not in CONVERTERS:
            raise AttributeError
        return CONVERTERS[name].convert(self.alpha3, self.country.alpha2 if self.country is not None else None,
                                        self.script.code if self.script is not None else None)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.alpha3 == other.alpha3 and self.country == other.country and self.script == other.script

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<Language [%s]>' % self

    def __str__(self):
        try:
            s = self.alpha2
        except ConvertError:
            s = self.alpha3
        if self.country is not None:
            s += '-' + str(self.country)
        if self.script is not None:
            s += '-' + str(self.script)
        return s


def register_converter(name, converter):
    """Register a :class:`~babelfish.converters.Converter`
    with the given name

    This will add the `name` property to the :class:`Language` class and
    an alternative constructor `fromname` if the `converter` is a
    :class:`~babelfish.converters.ReverseConverter`

    :param string name: name of the converter to register
    :param converter: converter to register
    :type converter: :class:`~babelfish.converters.Converter`

    """
    if name in CONVERTERS:
        raise ValueError('Converter %r already exists' % name)
    CONVERTERS[name] = converter()
    if isinstance(CONVERTERS[name], ReverseConverter):
        setattr(Language, 'from' + name, partial(Language.fromcode, converter=name))


def unregister_converter(name):
    """Unregister a :class:`~babelfish.converters.Converter` by
    name

    :param string name: name of the converter to unregister

    """
    if name not in CONVERTERS:
        raise ValueError('Converter %r does not exist' % name)
    if isinstance(CONVERTERS[name], ReverseConverter):
        delattr(Language, 'from' + name)
    del CONVERTERS[name]


def load_converters():
    """Load converters from the entry point

    Call :func:`register_converter` for each entry of the
    'babelfish.converters' entry point

    """
    for ep in iter_entry_points('babelfish.converters'):
        register_converter(ep.name, ep.load())


def clear_converters():
    """Clear all converters

    Call :func:`unregister_converter` on each registered converter
    in :data:`CONVERTERS`

    """
    for name in set(CONVERTERS.keys()):
        unregister_converter(name)
