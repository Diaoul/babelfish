.. babelfish documentation master file, created by
   sphinx-quickstart on Mon Sep 23 21:53:51 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BabelFish
=========
Release v\ |version|

BabelFish is a Python library to work with countries and languages.


Country
-------
Simple country representation from two-letters code (ISO-3166)::

    >>> country = babelfish.Country('GB')
    >>> country
    <Country UNITED KINGDOM>


Language
--------
Simple language representation from three-letters code (ISO-639-3)::

    >>> language = babelfish.Language('eng')
    >>> language
    <Language English>

Country specific language::

    >>> language = babelfish.Language('por', 'BR')
    >>> language
    <Language Portuguese, country=BRAZIL>

Built-in converters (alpha2, alpha3b, name and opensubtitles)::

    >>> language.alpha2
    'pt'
    >>> language.opensubtitles
    'pob'
    >>> babelfish.Language.fromalpha3b('fre')
    <Language French>


.. _custom_converters:

Custom Converters
-----------------
Build your own converter::

    class MyCodeConverter(babelfish.ReverseConverter):
        def __init__(self):
            self.to_mycode = {'fra': 'mycode1', 'eng': 'mycode2'}
            self.from_mycode = {'mycode1': 'fra', 'mycode2': 'eng'}
        def convert(self, alpha3, country=None):
            if alpha3 not in self.to_mycode:
                raise babelfish.NoConversionError
            return self.to_mycode[alpha3]
        def reverse(self, mycode):
            if mycode not in self.from_mycode:
                raise babelfish.NoConversionError
            return (self.from_mycode[mycode], None)

Use it::

    >>> babelfish.register_converter('mycode', MyCodeConverter)
    >>> babelfish.Language.frommycode('mycode2')
    <Language English>
    >>> babelfish.Language('fra').mycode
    'mycode1'


API Documentation
-----------------
If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
    :maxdepth: 2
    
    api/country
    api/language
    api/converter_bases
    api/exceptions



.. include:: ../HISTORY.rst
