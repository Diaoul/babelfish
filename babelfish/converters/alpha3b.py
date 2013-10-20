# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from pkg_resources import resource_stream  # @UnresolvedImport
from . import ReverseConverter
from ..exceptions import NoConversionError


class Alpha3BConverter(ReverseConverter):
    def __init__(self):
        self.to_alpha3b = {}
        self.from_alpha3b = {}
        with resource_stream('babelfish', 'data/iso-639-3.tab') as f:
            f.readline()
            for l in f:
                (alpha3, alpha3b, _, _, _, _, _, _) = l.decode('utf-8').split('\t')
                if alpha3b != '':
                    self.to_alpha3b[alpha3] = alpha3b
                    self.from_alpha3b[alpha3b] = alpha3

    def convert(self, alpha3, country=None):
        if alpha3 not in self.to_alpha3b:
            raise NoConversionError
        return self.to_alpha3b[alpha3]

    def reverse(self, alpha3b):
        if alpha3b not in self.from_alpha3b:
            raise NoConversionError
        return (self.from_alpha3b[alpha3b], None)
