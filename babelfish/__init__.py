# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
__title__ = 'babelfish'
__version__ = '0.4.1'
__author__ = 'Antoine Bertin'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 the BabelFish authors'

from .converters import (LanguageConverter, LanguageReverseConverter, LanguageEquivalenceConverter, CountryConverter,
    CountryReverseConverter)
from .country import country_converters, countries, country_matrix, Country
from .exceptions import Error, LanguageConvertError, LanguageReverseError, CountryConvertError, CountryReverseError
from .language import language_converters, languages, language_matrix, Language
from .script import scripts, Script
