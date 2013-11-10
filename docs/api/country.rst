Country
=======
.. module:: babelfish.country

.. data:: COUNTRIES

    Dictionary of country ISO-3166 codes to English names

.. autoclass:: Country
    :members:

.. data:: COUNTRY_CONVERTERS

    Registered converters

.. data:: COUNTRY_MATRIX

    Matrix of tuple (alpha2, name) as specified by ISO standard

.. autofunction:: register_country_converter
.. autofunction:: unregister_country_converter
.. autofunction:: load_country_converters
.. autofunction:: clear_country_converters
