# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from collections import namedtuple
from functools import partial
from typing import Any, ClassVar

from .compat import resource_stream
from .converters import ConverterManager, CountryConverter

#: The namedtuple used in the :data:`COUNTRY_MATRIX`
IsoCountry = namedtuple('IsoCountry', ['name', 'alpha2'])

#: Country code to country name mapping
COUNTRIES: dict[str, str] = {}

#: List of countries in the ISO-3166-1 as namedtuple of name, code
COUNTRY_MATRIX: list[IsoCountry] = []


with resource_stream('babelfish', 'data/iso-3166-1.txt') as f:
    f.readline()
    for line in f:
        iso_country = IsoCountry(*line.decode('utf-8').strip().split(';'))
        COUNTRIES[iso_country.alpha2] = iso_country.name
        COUNTRY_MATRIX.append(iso_country)


class CountryConverterManager(ConverterManager[CountryConverter]):
    """:class:`~babelfish.converters.ConverterManager` for country converters."""

    entry_point: ClassVar[str] = 'babelfish.country_converters'
    internal_converters: ClassVar[list[str]] = ['name = babelfish.converters.countryname:CountryNameConverter']

country_converters = CountryConverterManager()


class CountryMeta(type):
    """The :class:`Country` metaclass.

    Dynamically redirect :meth:`Country.frommycode` to :meth:`Country.fromcode` with the ``mycode`` `converter`

    """

    def __getattr__(cls, name: str) -> Any:
        if name.startswith('from'):
            return partial(cls.fromcode, converter=name[4:])
        return type.__getattribute__(cls, name)


class Country(metaclass=CountryMeta):
    """A country on Earth.

    A country is represented by a 2-letter code from the ISO-3166 standard

    :param string country: 2-letter ISO-3166 country code

    """

    def __init__(self, country: str) -> None:
        if country not in COUNTRIES:
            msg = f'{country!r} is not a valid country'
            raise ValueError(msg)

        #: ISO-3166 2-letter country code
        self.alpha2 = country

    @classmethod
    def fromcode(cls, code: str, converter: str) -> Country:
        """Create a :class:`Country` by its `code` using `converter` to
        :meth:`~babelfish.converters.CountryReverseConverter.reverse` it.

        :param string code: the code to reverse
        :param string converter: name of the :class:`~babelfish.converters.CountryReverseConverter` to use
        :return: the corresponding :class:`Country` instance
        :rtype: :class:`Country`

        """
        return cls(country_converters[converter].reverse(code))

    def __getstate__(self) -> str:
        return self.alpha2

    def __setstate__(self, state: str) -> None:
        self.alpha2 = state

    def __getattr__(self, name: str) -> str:
        try:
            return country_converters[name].convert(self.alpha2)
        except KeyError as err:
            raise AttributeError(name) from err

    def __hash__(self) -> int:
        return hash(self.alpha2)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return str(self) == other
        if not isinstance(other, Country):
            return False
        return self.alpha2 == other.alpha2

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return f'<Country [{self}]>'

    def __str__(self) -> str:
        return self.alpha2
