# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import LanguageReverseConverter
from ..exceptions import LanguageConvertError, LanguageReverseError
from ..language import LANGUAGE_MATRIX


class Alpha3BConverter(LanguageReverseConverter):
    def __init__(self):
        self.codes = set()
        self.to_alpha3b = {}
        self.from_alpha3b = {}
        for alpha3, alpha3b, alpha2, name in LANGUAGE_MATRIX:
            if alpha3b != '':
                self.codes.add(alpha3b)
                self.to_alpha3b[alpha3] = alpha3b
                self.from_alpha3b[alpha3b] = alpha3

    def convert(self, alpha3, country=None, script=None):
        if alpha3 not in self.to_alpha3b:
            raise LanguageConvertError(alpha3, country, script)
        return self.to_alpha3b[alpha3]

    def reverse(self, alpha3b):
        if alpha3b not in self.from_alpha3b:
            raise LanguageReverseError(alpha3b)
        return (self.from_alpha3b[alpha3b],)
