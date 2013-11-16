# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import LanguageEquivalenceConverter
from ..language import LANGUAGE_MATRIX

class NameConverter(LanguageEquivalenceConverter):
    CASE_SENSITIVE = False
    SYMBOLS = { lang.alpha3: lang.name
                for lang in LANGUAGE_MATRIX }
