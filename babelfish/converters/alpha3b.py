# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from pkg_resources import resource_stream  # @UnresolvedImport
from . import ReverseConverter
from ..exceptions import ConvertError, ReverseError


class Alpha3BConverter(ReverseConverter):
    def __init__(self):
        self.codes = set()
        self.to_alpha3b = {}
        self.from_alpha3b = {}
        f = resource_stream('babelfish', 'data/iso-639-3.tab')
        f.readline()
        for l in f:
            (alpha3, alpha3b, _, _, _, _, _, _) = l.decode('utf-8').split('\t')
            if alpha3b != '':
                self.codes.add(alpha3b)
                self.to_alpha3b[alpha3] = alpha3b
                self.from_alpha3b[alpha3b] = alpha3
        f.close()

    def convert(self, alpha3, country=None):
        if alpha3 not in self.to_alpha3b:
            raise ConvertError(alpha3, country)
        return self.to_alpha3b[alpha3]

    def reverse(self, alpha3b):
        if alpha3b not in self.from_alpha3b:
            raise ReverseError(alpha3b)
        return (self.from_alpha3b[alpha3b], None)
