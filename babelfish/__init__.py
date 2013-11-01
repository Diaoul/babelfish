# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
__title__ = 'babelfish'
__version__ = '0.2.1'
__author__ = 'Antoine Bertin'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 the BabelFish authors'

from .converters import Converter, ReverseConverter
from .country import COUNTRIES, Country
from .exceptions import Error, ConvertError, ReverseError
from .language import (CONVERTERS, LANGUAGES, Language, register_converter, unregister_converter, load_converters,
    clear_converters)


load_converters()
