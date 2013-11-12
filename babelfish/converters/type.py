# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from ..exceptions import LanguageConvertError
from . import LanguageConverter
from ..language import LANGUAGE_MATRIX

class LanguageTypeConverter(LanguageConverter):
    FULLNAME = { 'A': 'ancient',
                 'C': 'constructed',
                 'E': 'extinct',
                 'H': 'historical',
                 'L': 'living',
                 'S': 'special'
    }
    SYMBOLS = { alpha3: ltype
                for (alpha3, _, _, _, _, ltype, _, _) in LANGUAGE_MATRIX }
    codes = set(SYMBOLS.values())

    def convert(self, alpha3, country=None, script=None):
        try:
            return self.FULLNAME[self.SYMBOLS[alpha3]]
        except KeyError:
            raise LanguageConvertError(alpha3, country, script)