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


class NameConverter(ReverseConverter):
    def __init__(self):
        self.codes = set()
        self.to_name = {}
        self.from_name = {}
        for alpha3, alpha3b, alpha2, name in LANGUAGE_MATRIX:
            self.codes.add(name)
            self.to_name[alpha3] = name
            self.from_name[name] = alpha3

    def convert(self, alpha3, country=None, script=None):
        if alpha3 not in self.to_name:
            raise ConvertError(alpha3, country, script)
        return self.to_name[alpha3]

    def reverse(self, name):
        if name not in self.from_name:
            raise ReverseError(name)
        return (self.from_name[name],)
