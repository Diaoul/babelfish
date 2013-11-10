Language
========
.. module:: babelfish.language

.. data:: LANGUAGES

    Set of ISO-639-3 3-letter code

.. autoclass:: Language

.. data:: LANGUAGE_CONVERTERS

    Registered converters

.. data:: LANGUAGE_MATRIX

    Matrix of tuple (alpha3, alpha3b, alpha2, name) as specified by ISO standard

.. autofunction:: register_language_converter
.. autofunction:: unregister_language_converter
.. autofunction:: load_language_converters
.. autofunction:: clear_language_converters
