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


class NameConverter(LanguageReverseConverter):
    def __init__(self):
        self.codes = set()
        self.to_name = {}
        self.from_lower = {}
        for alpha3, alpha3b, alpha2, name in LANGUAGE_MATRIX:
            self.codes.add(name)
            self.to_name[alpha3] = name
            self.from_lower[name.lower()] = alpha3

    def convert(self, alpha3, country=None, script=None):
        if alpha3 not in self.to_name:
            raise LanguageConvertError(alpha3, country, script)
        return self.to_name[alpha3]

    def reverse(self, name):
        lname = name.lower()
        if lname not in self.from_lower:
            raise LanguageReverseError(name)
        return (self.from_lower[lname],)
