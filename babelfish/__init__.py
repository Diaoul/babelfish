# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
__title__ = 'babelfish'
__version__ = '0.3.0'
__author__ = 'Antoine Bertin'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 the BabelFish authors'

from .converters import (LanguageConverter, LanguageReverseConverter,
                         CountryConverter, CountryReverseConverter)
from .script import SCRIPTS, Script
from .exceptions import (Error, LanguageConvertError, LanguageReverseError,
                         CountryConvertError, CountryReverseError)
from .language import (LANGUAGE_CONVERTERS, LANGUAGES, LANGUAGE_MATRIX, Language,
                       register_language_converter, unregister_language_converter,
                       load_language_converters, clear_language_converters)
from .country import (COUNTRY_CONVERTERS, COUNTRIES, COUNTRY_MATRIX, Country,
                      register_country_converter, unregister_country_converter,
                      load_country_converters, clear_country_converters)

load_language_converters()
load_country_converters()