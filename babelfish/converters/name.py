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


class NameConverter(ReverseConverter):
    def __init__(self):
        self.to_name = {}
        self.from_name = {}
        with resource_stream('babelfish', 'data/iso-639-3.tab') as f:
            f.readline()
            for l in f:
                (alpha3, _, _, _, _, _, name, _) = l.decode('utf-8').split('\t')
                self.to_name[alpha3] = name
                self.from_name[name] = alpha3

    def convert(self, alpha3, country=None):
        if alpha3 not in self.to_name:
            raise NoConversionError
        return self.to_name[alpha3]

    def reverse(self, name):
        if name not in self.from_name:
            raise NoConversionError
        return (self.from_name[name], None)
