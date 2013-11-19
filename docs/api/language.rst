Language
========
.. module:: babelfish.language

.. data:: LANGUAGES

    Available language codes

.. data:: LANGUAGE_MATRIX

    List of languages in the ISO-639-3 as namedtuple of alpha3, alpha3b, alpha3t, alpha2, scope, type, name and comment

.. data:: LANGUAGE_CONVERTERS

    Loaded language converters

.. autoclass:: LanguageMeta

.. autoclass:: Language
    :members:

.. autofunction:: get_language_converter

.. autofunction:: register_language_converter

.. autofunction:: unregister_language_converter

.. autofunction:: load_language_converters

.. autofunction:: clear_language_converters
