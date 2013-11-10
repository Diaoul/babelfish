# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import ReverseConverter
from ..exceptions import ConvertError, ReverseError
from ..language import LANGUAGE_MATRIX

class Alpha2Converter(ReverseConverter):
    def __init__(self):
        self.codes = set()
        self.to_alpha2 = {}
        self.from_alpha2 = {}
        for alpha3, alpha3b, alpha2, name in LANGUAGE_MATRIX:
            if alpha2 != '':
                self.codes.add(alpha2)
                self.to_alpha2[alpha3] = alpha2
                self.from_alpha2[alpha2] = alpha3

    def convert(self, alpha3, country=None, script=None):
        if alpha3 not in self.to_alpha2:
            raise ConvertError(alpha3, country, script)
        return self.to_alpha2[alpha3]

    def reverse(self, alpha2):
        if alpha2 not in self.from_alpha2:
            raise ReverseError(alpha2)
        return (self.from_alpha2[alpha2],)
