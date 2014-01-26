.. babelfish documentation master file, created by
   sphinx-quickstart on Mon Sep 23 21:53:51 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BabelFish
=========
Release v\ |version|

BabelFish is a Python library to work with countries and languages.


Script
------
Simple script representation from 4-letter code (ISO-15924)::

    >>> script = babelfish.Script('Hira')
    >>> script
    <Script [Hira]>


Country
-------
Simple country representation from 2-letter code (ISO-3166)::

    >>> country = babelfish.Country('GB')
    >>> country
    <Country [GB]>

Built-in country converters (name)::

    >>> country.name
    'UNITED KINGDOM'

Language
--------
Simple language representation from 3-letter code (ISO-639-3)::

    >>> language = babelfish.Language('eng')
    >>> language
    <Language [en]>

Country specific language::

    >>> language = babelfish.Language('por', 'BR')
    >>> language
    <Language [pt-BR]>

Language with specific script::

    >>> language = babelfish.Language.fromalpha2('sr')
    >>> language.script = babelfish.Script('Cyrl')
    >>> language
    <Language [sr-Cyrl]>

Built-in language converters (alpha2, alpha3b, alpha3t, name, scope, type and opensubtitles)::

    >>> language = babelfish.Language('por', 'BR')
    >>> language.alpha2
    'pt'
    >>> language.scope
    'individual'
    >>> language.type
    'living'
    >>> language.opensubtitles
    'pob'
    >>> babelfish.Language.fromalpha3b('fre')
    <Language [fr]>


.. _custom_converters:

Custom Converters
-----------------
Build your own Language/Country converter::

    class MyCodeConverter(babelfish.LanguageReverseConverter):
        def __init__(self):
            self.to_mycode = {'fra': 'mycode1', 'eng': 'mycode2'}
            self.from_mycode = {'mycode1': 'fra', 'mycode2': 'eng'}
        def convert(self, alpha3, country=None, script=None):
            if alpha3 not in self.to_mycode:
                raise babelfish.LanguageConvertError(alpha3, country, script)
            return self.to_mycode[alpha3]
        def reverse(self, mycode):
            if mycode not in self.from_mycode:
                raise babelfish.LanguageReverseError(mycode)
            return (self.from_mycode[mycode],)

You can also use the :class:`~babelfish.converters.LanguageEquivalenceConverter`
utility class if your mapping is a simple one-to-one mapping::

    class MyCodeConverter(babelfish.LanguageEquivalenceConverter):
        SYMBOLS = {'fra': 'mycode1', 'eng': 'mycode2'}

Use it directly (no lazy loading)::

    >>> babelfish.LANGUAGE_CONVERTERS['mycode'] = MyCodeConverter()
    >>> babelfish.Language.frommycode('mycode2')
    <Language [en]>
    >>> babelfish.Language('fra').mycode
    'mycode1'

Or make it available in your application by using the entry point (lazy loading)::

    setup([...],
          entry_points={'babelfish.language_converters': ['mycode = mymodule.converter:MyCodeConverter']},
          [...])

Or if you don't want to use the entry point (lazy loading)::

    >>> babelfish.language_converters.register('mycode = mymodule.converter:MyCodeConverter')


API Documentation
-----------------
If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
    :maxdepth: 2

    api/script
    api/country
    api/language
    api/converter_bases
    api/exceptions



.. include:: ../HISTORY.rst
