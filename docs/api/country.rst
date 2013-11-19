Country
=======
.. module:: babelfish.country

.. data:: COUNTRIES

    Country code to country name mapping

.. data:: COUNTRY_MATRIX

    List of countries in the ISO-3166-1 as namedtuple of alpha2 and name

.. data:: COUNTRY_CONVERTERS

    Loaded country converters

.. autoclass:: CountryMeta

.. autoclass:: Country
    :members:

.. autofunction:: get_country_converter

.. autofunction:: register_country_converter

.. autofunction:: unregister_country_converter

.. autofunction:: load_country_converters

.. autofunction:: clear_country_converters
