# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from collections import namedtuple
from dataclasses import InitVar, dataclass
from functools import partial
from typing import Any, ClassVar

from .compat import resource_stream
from .converters import ConverterManager, LanguageReverseConverter
from .country import Country
from .exceptions import LanguageConvertError
from .script import Script

#: The namedtuple used in the :data:`LANGUAGE_MATRIX`
IsoLanguage = namedtuple('IsoLanguage', ['alpha3', 'alpha3b', 'alpha3t', 'alpha2', 'scope', 'type', 'name', 'comment'])

#: Language code set
LANGUAGES = set()

#: List of languages in the ISO-639-3 as namedtuple of alpha3, alpha3b, alpha3t, alpha2, scope, type, name and comment
LANGUAGE_MATRIX = []


with resource_stream('babelfish', 'data/iso-639-3.tab') as f:
    f.readline()
    for line in f:
        iso_language = IsoLanguage(*line.decode('utf-8').split('\t'))
        LANGUAGES.add(iso_language.alpha3)
        LANGUAGE_MATRIX.append(iso_language)


class LanguageConverterManager(ConverterManager[LanguageReverseConverter]):
    """:class:`~babelfish.converters.ConverterManager` for language converters."""

    entry_point: ClassVar[str] = 'babelfish.language_converters'
    internal_converters: ClassVar[list[str]] = [
        'alpha2 = babelfish.converters.alpha2:Alpha2Converter',
        'alpha3b = babelfish.converters.alpha3b:Alpha3BConverter',
        'alpha3t = babelfish.converters.alpha3t:Alpha3TConverter',
        'name = babelfish.converters.name:NameConverter',
        'scope = babelfish.converters.scope:ScopeConverter',
        'type = babelfish.converters.type:LanguageTypeConverter',
        'opensubtitles = babelfish.converters.opensubtitles:OpenSubtitlesConverter',
    ]


language_converters = LanguageConverterManager()


def to_country(country: str | Country | None) -> Country | None:
    """Convert to Country or None."""
    if isinstance(country, Country):
        return country
    if country is None:
        return None
    return Country(country)


def to_script(script: str | Script | None) -> Script | None:
    """Convert to Script or None."""
    if isinstance(script, Script):
        return script
    if script is None:
        return None
    return Script(script)


class LanguageMeta(type):
    """The :class:`Language` metaclass.

    Dynamically redirect :meth:`Language.frommycode` to :meth:`Language.fromcode` with the ``mycode`` `converter`

    """

    def __getattr__(cls, name: str) -> Any:
        if name.startswith('from'):
            return partial(cls.fromcode, converter=name[4:])
        return type.__getattribute__(cls, name)


@dataclass(frozen=True)
class Language(metaclass=LanguageMeta):
    """A human language.

    A human language is composed of a language part following the ISO-639
    standard and can be country-specific when a :class:`~babelfish.country.Country`
    is specified.

    The :class:`Language` is extensible with custom converters (see :ref:`custom_converters`)

    :param string language: the language as a 3-letter ISO-639-3 code
    :param country: the country (if any) as a 2-letter ISO-3166 code or :class:`~babelfish.country.Country` instance
    :type country: string or :class:`~babelfish.country.Country` or None
    :param script: the script (if any) as a 4-letter ISO-15924 code or :class:`~babelfish.script.Script` instance
    :type script: string or :class:`~babelfish.script.Script` or None
    :param unknown: the unknown language as a three-letters ISO-639-3 code to use as fallback
    :type unknown: string or None
    :raise: ValueError if the language could not be recognized and `unknown` is ``None``

    """

    language: str
    country: Country | None
    script: Script | None
    unknown: InitVar[str | None] = None

    def __init__(
        self,
        language: str,
        country: str | Country | None = None,
        script: str | Script | None = None,
        unknown: str | None = None,
    ) -> None:
        if unknown is not None and language not in LANGUAGES:
            language = unknown

        if language not in LANGUAGES:
            msg = f'{language!r} is not a valid language'
            raise ValueError(msg)
        country = to_country(country)
        script = to_script(script)

        object.__setattr__(self, 'language', language)
        object.__setattr__(self, 'country', country)
        object.__setattr__(self, 'script', script)

    @classmethod
    def fromcode(cls, code: str, converter: str) -> Language:
        """Create a :class:`Language` by its `code` using `converter` to
        :meth:`~babelfish.converters.LanguageReverseConverter.reverse` it.

        :param string code: the code to reverse
        :param string converter: name of the :class:`~babelfish.converters.LanguageReverseConverter` to use
        :return: the corresponding :class:`Language` instance
        :rtype: :class:`Language`

        """
        return cls(*language_converters[converter].reverse(code))

    @classmethod
    def fromietf(cls, ietf: str) -> Language:
        """Create a :class:`Language` by from an IETF language code.

        :param string ietf: the ietf code
        :return: the corresponding :class:`Language` instance
        :rtype: :class:`Language`

        """
        subtags = ietf.split('-')
        # Parse language from the first subtags
        language_subtag = subtags.pop(0).lower()
        if len(language_subtag) == 2:
            simple_language = cls.fromalpha2(language_subtag)
            language_subtag = simple_language.alpha3

        # Parse country and script from the rest of subtags
        country_subtag: Country | None = None
        script_subtag: Script | None = None
        while subtags:
            subtag = subtags.pop(0)
            if len(subtag) == 2:
                country_subtag = Country(subtag.upper())
            else:
                script_subtag = Script(subtag.capitalize())
            if script_subtag is not None:
                if subtags:
                    msg = f'Wrong IETF format. Unmatched subtags: {subtags!r}'
                    raise ValueError(msg)
                break

        return cls(language_subtag, country_subtag, script_subtag)

    @property
    def alpha3(self) -> str:
        return self.language

    def __getattr__(self, name: str) -> str:
        # Handle private attributes by raising AttributeError
        # so the class is pickable, see: https://stackoverflow.com/a/50888571
        if name.startswith('_'):
            raise AttributeError

        try:
            alpha3 = self.alpha3
            country = self.country.alpha2 if self.country is not None else None
            script = self.script.code if self.script is not None else None
            return language_converters[name].convert(alpha3, country, script)
        except KeyError as err:
            raise AttributeError(name) from err

    def __bool__(self) -> bool:
        return self.language != 'und'

    __nonzero__ = __bool__

    def __repr__(self) -> str:
        return f'<Language [{self}]>'

    def __str__(self) -> str:
        try:
            s = self.alpha2
        except LanguageConvertError:
            s = self.alpha3
        if self.country is not None:
            s += '-' + str(self.country)
        if self.script is not None:
            s += '-' + str(self.script)
        return s
