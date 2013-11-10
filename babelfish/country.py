# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from functools import partial
from pkg_resources import resource_stream, iter_entry_points  # @UnresolvedImport
from .converters import CountryReverseConverter


COUNTRY_CONVERTERS = {}
COUNTRIES = {}
COUNTRY_MATRIX = []

f = resource_stream('babelfish', 'data/iso-3166-1.txt')
f.readline()
for l in f:
    (name, alpha2) = l.decode('utf-8').strip().split(';')
    COUNTRIES[alpha2] = name
    COUNTRY_MATRIX.append((alpha2, name))
f.close()


class Country(object):
    """A country on Earth

    A country is represented by a 2-letter code from the ISO-3166 standard

    :param string country: 2-letter ISO-3166 country code

    """
    def __init__(self, country):
        if country not in COUNTRIES:
            raise ValueError('%r is not a valid country' % country)

        #: ISO-3166 2-letter country code
        self.alpha2 = country

    @classmethod
    def fromcode(cls, code, converter):
        return cls(COUNTRY_CONVERTERS[converter].reverse(code))

    def __getattr__(self, name):
        if name not in COUNTRY_CONVERTERS:
            raise AttributeError(name)
        return COUNTRY_CONVERTERS[name].convert(self.alpha2)

    def __hash__(self):
        return hash(self.alpha2)

    def __eq__(self, other):
        if other is None:
            return False
        return self.alpha2 == other.alpha2

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<Country [%s]>' % self

    def __str__(self):
        return self.alpha2


def register_country_converter(name, converter):
    """Register a :class:`~babelfish.converters.CountryConverter`
    with the given name

    This will add the `name` property to the :class:`Country` class and
    an alternative constructor `fromname` if the `converter` is a
    :class:`~babelfish.converters.CountryReverseConverter`

    :param string name: name of the converter to register
    :param converter: converter to register
    :type converter: :class:`~babelfish.converters.CountryConverter`

    """
    if name in COUNTRY_CONVERTERS:
        raise ValueError('Converter %r already exists' % name)
    COUNTRY_CONVERTERS[name] = converter()
    if isinstance(COUNTRY_CONVERTERS[name], CountryReverseConverter):
        setattr(Country, 'from' + name, partial(Country.fromcode, converter=name))


def unregister_country_converter(name):
    """Unregister a :class:`~babelfish.converters.CountryConverter` by
    name

    :param string name: name of the converter to unregister

    """
    if name not in COUNTRY_CONVERTERS:
        raise ValueError('Converter %r does not exist' % name)
    if isinstance(COUNTRY_CONVERTERS[name], CountryReverseConverter):
        delattr(Country, 'from' + name)
    del COUNTRY_CONVERTERS[name]


def load_country_converters():
    """Load converters from the entry point

    Call :func:`register_country_converter` for each entry of the
    'babelfish.country_converters' entry point

    """
    for ep in iter_entry_points('babelfish.country_converters'):
        register_country_converter(ep.name, ep.load())


def clear_country_converters():
    """Clear all country converters

    Call :func:`unregister_country_converter` on each registered converter
    in :data:`COUNTRY_CONVERTERS`

    """
    for name in set(COUNTRY_CONVERTERS.keys()):
        unregister_country_converter(name)
