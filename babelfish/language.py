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

    :param string language: the language as a three-letters ISO-639-3 code
    :param country: the country (if any) as a two-letters ISO-3166 code or :class:`~babelfish.country.Country` instance
    :type country: string or :class:`~babelfish.country.Country` or None

    """
    def __init__(self, language, country=None):
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

    @classmethod
    def fromcode(cls, code, converter):
        return cls(*CONVERTERS[converter].reverse(code))

    def __getattr__(self, name):
        if name not in CONVERTERS:
            raise AttributeError
        return CONVERTERS[name].convert(self.alpha3, self.country.alpha2 if self.country is not None else None)

    def __hash__(self):
        if self.country is None:
            return hash(self.alpha3)
        return hash(self.alpha3 + '-' + self.country.alpha2)

    def __eq__(self, other):
        return self.alpha3 == other.alpha3 and self.country == other.country

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<Language [%s]>' % self

    def __str__(self):
        if self.country is not None:
            return '%s-%s' % (self.alpha3, self.country)
        return self.alpha3


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
